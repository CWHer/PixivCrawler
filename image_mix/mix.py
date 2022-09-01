"""
Credit to https://github.com/NoisyWinds/puzzle/blob/master/puzzle.py

Procedure:
    1. transfer each image in image library into a color block
        NOTE: a color block can be seen as a huge pixel
            i.e. a color block only represents a single color (average color)
    2. split target image into blocks of the same size
        for each target block, choose the color block with minimum distance, and paste on the target

The above algorithm is apparently sub-optimal
Some possible improvements:
  1. construct a priority queue with global distance (n x m) as key
     choose minimum global distance pair, remove, and repeat
     this is just another greedy algorithm, but I believe this works better

  2. MCMF (exact algorithm)
     construct the following graph:
          S                 === (capacity=REPEAT_TIMES, cost=0)  ===>      blocks(n)
          blocks(n)         === (capacity=1, cost=dist)          ===>      target_block(m)
          target_block(m)   === (capacity=1, cost=0)             ===>      T
     the above graph is large, which contains O(nm) edges
     a tradeoff between accuracy and running time:
        1. each block only connects k closest target_blocks
        2. each target_block only connects k closest blocks
        when image library is large, I believe K = 5 ~ 10 can yield a relatively good solution
"""

import argparse
import os
from colorsys import rgb_to_hsv
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
from PIL import Image, ImageOps
from tqdm import tqdm

from bvh import BVH, Point
from utils import checkDir, printError, printInfo, printWarn, timeLog


class ImageLib():
    @timeLog
    def __init__(self, im_dir: str, config: Dict,
                 input_dir: Optional[str] = None) -> None:
        checkDir(im_dir)
        self.im_dir = im_dir
        self.config = config

        if input_dir is not None:
            self.construct(input_dir)
        self.load()

    @staticmethod
    def resizeImage(im_path: str,
                    width, height=None):
        if height is None:
            height = width
        return ImageOps.fit(
            Image.open(im_path).convert("RGB"),
            (width, height), Image.Resampling.LANCZOS)

    @staticmethod
    def calcAvgColor(img: Image.Image) -> str:
        pixels = img.load()
        width, height = img.size
        rgb_colors: Iterable[Tuple[float, float, float]] = \
            map(lambda rgb: (rgb[0] / 255, rgb[1] / 255, rgb[2] / 255),
                [pixels[i, j] for i in range(width) for j in range(height)])
        hsv_colors = list(map(lambda rgb: rgb_to_hsv(*rgb), rgb_colors))
        hsv_colors = np.array(hsv_colors)

        hsv_average = hsv_colors.mean(axis=0)
        hsv_average = map(lambda x: round(x, 3), hsv_average)
        return "{}_{}_{}".format(*hsv_average)

    @staticmethod
    def loadInput(input_dir: str) -> List[str]:
        im_paths: List[str] = []
        suffixes = set(["jpg", "png"])
        for file_name in os.listdir(input_dir):
            suffix = file_name[file_name.rfind(".") + 1:]
            if suffix not in suffixes:
                printWarn(True, f"non-image file {file_name}")
                continue
            im_paths.append(input_dir + file_name)

        if not im_paths:
            raise RuntimeError("no input")
        printInfo(f"images found: {len(im_paths)}")
        return im_paths

    def construct(self, input_dir):
        im_paths = self.loadInput(input_dir)
        for im_path in tqdm(
                im_paths, desc="constructing image library"):
            try:
                im_block = self.resizeImage(
                    im_path, self.config["BLOCK_SIZE"])
                block_color = self.calcAvgColor(im_block)
                im_block.save("".join(
                    [self.im_dir, str(block_color), ".png"]))
            except Exception as e:
                printWarn(True, e)
                printWarn(True, f"skip {im_path}")

    def load(self) -> None:
        points = []
        for file_name in os.listdir(self.im_dir):
            prefix = file_name[:file_name.rfind(".")]
            values = map(float, prefix.split("_"))
            points.append(Point(*values))

        self.bvh_tree = BVH(
            MAX_TIMES=self.config["MAX_TIMES"])
        self.bvh_tree.build(father=None, points=points)

    def loadImage(self, im_name) -> Image.Image:
        return Image.open(self.im_dir + im_name)

    def findClosest(self, target: Point) -> str:
        self.bvh_tree.reset()
        self.bvh_tree.query(target)
        printError(
            self.bvh_tree.ans is None,
            "run out of image library, please increase MAX_TIMES")

        node = self.bvh_tree.ans
        node.used_times += 1
        block_color = node.box.max_p.pos
        if node.used_times >= \
                self.bvh_tree.MAX_TIMES:
            self.bvh_tree.remove(node)
        return "{}_{}_{}".format(*block_color)


@timeLog
def createPuzzle(image_lib: ImageLib, config: Dict,
                 target_image: Image.Image) -> Image.Image:
    width, height = target_image.size
    printInfo(f"output: width = {width}, height = {height}")
    result = Image.new("RGB", target_image.size, (255, 255, 255))
    BLOCK_SIZE = config["BLOCK_SIZE"]
    width, height = width // BLOCK_SIZE, height // BLOCK_SIZE

    with tqdm(total=width * height,
              desc="creating puzzle") as pbar:
        for j in range(0, height):
            for i in range(0, width):
                try:
                    x, y = i * BLOCK_SIZE, j * BLOCK_SIZE
                    target_block = target_image.crop(
                        (x, y, x + BLOCK_SIZE, y + BLOCK_SIZE))
                    target_color = map(
                        float, ImageLib.calcAvgColor(target_block).split("_"))
                    im_name = image_lib.findClosest(
                        Point(*target_color)) + ".png"
                    result.paste(image_lib.loadImage(im_name), (x, y))
                    pbar.update()
                except Exception as e:
                    printWarn(True, e)
                    printError(True, f"creating ({i},{j}) failed")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "-l", "--lib_dir", type=str, required=True,
        help="image lib directory (e.g., ./image_lib/)")
    parser.add_argument(
        "-t", "--target_image", type=str, required=True,
        help="target image path (e.g. ./images/44873217_p0.jpg)")
    parser.add_argument(
        "-i", "--input_dir", type=str, default=None,
        help="raw image directory (e.g., ./images/). "
        "NOTE: set to None if image lib is already constructed")
    parser.add_argument(
        "-b", "--block_size", type=int,
        default=50, help="target image are divided into blocks")
    parser.add_argument(
        "-width", "--output_width", type=int,
        default=4000, help="width of output image")
    parser.add_argument(
        "-height", "--output_height", type=int,
        default=2000, help="height of output image")
    parser.add_argument(
        "-m", "--max_times", type=int, default=1,
        help="max repeating times of lib blocks")
    args = parser.parse_args()

    config = {
        "BLOCK_SIZE": args.block_size,
        "OUTPUT_WIDTH": args.output_width,
        "OUTPUT_HEIGHT": args.output_height,

        "INPUT_DIR": args.input_dir,  # raw input directory
        "LIB_DIR": args.lib_dir,  # image lib directory
        "MAX_TIMES": args.max_times,  # max repeating times of lib blocks

        "TARGET_IMAGE": args.target_image
    }

    image_lib = ImageLib(
        im_dir=config["LIB_DIR"], config=config,
        input_dir=config["INPUT_DIR"])
    image = config["TARGET_IMAGE"]
    target_image = ImageLib.resizeImage(
        image, config["OUTPUT_WIDTH"], config["OUTPUT_HEIGHT"])

    # HACK: soften result
    result = createPuzzle(image_lib, config, target_image)
    target_image = Image.blend(result, target_image, 0.5)
    target_image.save("result.png")
    printInfo("Done")

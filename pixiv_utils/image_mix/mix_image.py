"""
Credit to https://github.com/NoisyWinds/puzzle/blob/master/puzzle.py

### Procedure:
1. **Transform each image in the image library into a color block**
   - A color block can be seen as a large pixel, representing a single color (the average color of the image).

2. **Split the target image into blocks of the same size**
   - For each target block, choose the color block with the minimum distance and paste it onto the target.

### The Algorithm's Limitations:
The described algorithm is sub-optimal. Here are some possible improvements:

1. **Priority Queue with Global Distance (Greedy Algorithm)**
   - Construct a priority queue where the key is the global distance (n x m).
   - Choose the pair with the minimum global distance, remove it from the queue, and repeat.
   - Although this is another greedy algorithm, it is likely to yield better results.

2. **Minimum Cost Maximum Flow (MCMF) Algorithm**
   - Construct the following graph:
     - **Source (S)** connects to **blocks (n)** with edges of capacity equal to REPEAT_TIMES and cost of 0.
     - **Blocks (n)** connect to **target blocks (m)** with edges of capacity 1 and cost equal to the distance.
     - **Target blocks (m)** connect to **Sink (T)** with edges of capacity 1 and cost of 0.
   - This graph is large, containing O(nm) edges. To balance accuracy and running time:
     - Each block only connects to the k closest target blocks.
     - Each target block only connects to the k closest blocks.
   - When the image library is large, a value of k between 5 and 10 can yield relatively good solutions.
"""

import argparse
import os
from typing import List, Optional, Set

import numpy as np
import tqdm
from bvh_tree import BVHTree, Point
from PIL import Image, ImageOps
from utils import assertError, assertWarn, checkDir, logTime, printInfo


class ImageLib:
    @logTime
    def __init__(
        self, im_dir: str, block_size: int, max_times: int, input_dir: Optional[str] = None
    ) -> None:
        """
        Initialize the ImageLib object.

        Args:
            im_dir (str): The directory where the image library is stored.
            block_size (int): The size of the blocks to divide the target image into.
            max_times (int): The maximum number of times a image block can be used.
            input_dir (Optional[str]): The directory where the raw input images are stored. Defaults to None.
        """
        checkDir(im_dir)
        self.im_dir = im_dir
        self.block_size = block_size
        self.max_times = max_times

        if input_dir is not None:
            self._construct(input_dir)
        self._load()

    @staticmethod
    def resizeImage(im_path: str, width: int, height: Optional[int] = None):
        if height is None:
            height = width
        return ImageOps.fit(
            Image.open(im_path).convert("RGB"), (width, height), Image.Resampling.LANCZOS
        )

    @staticmethod
    def calcAvgColor(img: Image.Image) -> str:
        """
        Calculate the average color of an image.

        Args:
            img (Image.Image): The image.

        Returns:
            The average color in the format "h_s_v".
        """
        hsv_colors = np.array(img.convert("HSV"), dtype=np.float32) / 255.0
        hsv_colors = hsv_colors.reshape(-1, hsv_colors.shape[-1])
        hsv_average = np.mean(hsv_colors, axis=0)
        hsv_average = map(lambda x: round(x, 3), hsv_average)
        return "{}_{}_{}".format(*hsv_average)

    @staticmethod
    def _loadInput(input_dir: str, suffixes: Set = set(["jpg", "png"])) -> List[str]:
        """
        Load input images from a directory.

        Args:
            input_dir (str): The directory where the input images are stored.
            suffixes (Set): A set of valid file suffixes. Defaults to set(["jpg", "png"]).

        Returns:
            A list of paths to the input images.
        """
        im_paths: List[str] = []
        for file_name in os.listdir(input_dir):
            suffix = file_name[file_name.rfind(".") + 1 :]
            if suffix not in suffixes:
                assertWarn(False, f"Non-image file {file_name}")
                continue
            im_paths.append(os.path.join(input_dir, file_name))

        assertError(len(im_paths) > 0, "No inputs!")
        printInfo(f"Number of images found: {len(im_paths)}")
        return im_paths

    def _construct(self, input_dir: str, suffix: str = ".png"):
        """
        Construct the image library from input images.

        Args:
            input_dir (str): The directory where the input images are stored.
            suffix (str): The suffix to be added to the saved image files. Defaults to ".png".
        """
        im_paths = self._loadInput(input_dir)
        for im_path in tqdm.tqdm(im_paths, desc="Constructing image library"):
            try:
                im_block = self.resizeImage(im_path, self.block_size)
                block_color = self.calcAvgColor(im_block)
                im_block.save(os.path.join(self.im_dir, block_color + suffix))
            except Exception as e:
                assertWarn(False, e)
                assertWarn(False, f"Skip {im_path}")

    def _load(self) -> None:
        points = []
        for file_name in os.listdir(self.im_dir):
            prefix = file_name[: file_name.rfind(".")]
            values = map(float, prefix.split("_"))
            points.append(Point(*values))

        self.bvh_tree = BVHTree(MAX_TIMES=self.max_times)
        self.bvh_tree.build(father=None, points=points)

    def loadImage(self, im_name: str, suffix: str = ".png") -> Image.Image:
        return Image.open(os.path.join(self.im_dir, im_name + suffix))

    def findClosest(self, target: Point) -> str:
        self.bvh_tree.reset()
        self.bvh_tree.query(target)
        assertError(
            self.bvh_tree.closest_node is not None, "Run out of images, please increase MAX_TIMES"
        )

        node = self.bvh_tree.closest_node
        node.used_times += 1
        block_color = node.box.max_p
        if node.used_times >= self.bvh_tree.MAX_TIMES:
            self.bvh_tree.remove(node)
        return "{}_{}_{}".format(*block_color)


@logTime
def createPuzzle(image_lib: ImageLib, block_size: int, target_image: Image.Image) -> Image.Image:
    """
    Create a puzzle image by mixing smaller images from the image library.

    Args:
        image_lib (ImageLib): An instance of the ImageLib class containing the image library.
        block_size (int): The size of the blocks to divide the target image into.
        target_image (Image.Image): The target image to create the puzzle from.

    Returns:
        Image.Image: The resulting puzzle image.

    """
    width, height = target_image.size
    printInfo(f"Output: width = {width}, height = {height}")
    result = Image.new("RGB", target_image.size, (255, 255, 255))
    width, height = width // block_size, height // block_size

    with tqdm.trange(width * height, desc="Creating puzzle") as pbar:
        for j in range(0, height):
            for i in range(0, width):
                try:
                    x, y = i * block_size, j * block_size
                    target_block = target_image.crop((x, y, x + block_size, y + block_size))
                    target_color = map(float, ImageLib.calcAvgColor(target_block).split("_"))
                    im_name = image_lib.findClosest(Point(*target_color))
                    result.paste(image_lib.loadImage(im_name), (x, y))
                    pbar.update()
                except Exception as e:
                    assertWarn(False, e)
                    assertError(False, f"Creating ({i},{j}) failed!")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "-l", "--lib-dir", type=str, required=True, help="image lib directory (e.g., ./image_lib/)"
    )
    parser.add_argument(
        "-t",
        "--target-image",
        type=str,
        required=True,
        help="target image path (e.g. ./images/44873217_p0.jpg)",
    )
    parser.add_argument(
        "-i",
        "--input-dir",
        type=str,
        default=None,
        help="raw image directory (e.g., ./images/). "
        "NOTE: set to None if image lib is already constructed",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        type=str,
        default="result.png",
        help="output file path (e.g., ./result.png)",
    )
    parser.add_argument(
        "-b", "--block-size", type=int, default=50, help="target image are divided into blocks"
    )
    parser.add_argument(
        "-width", "--output-width", type=int, default=4000, help="width of output image"
    )
    parser.add_argument(
        "-height", "--output-height", type=int, default=2000, help="height of output image"
    )
    parser.add_argument(
        "-m", "--max-times", type=int, default=1, help="max repeating times of lib blocks"
    )
    parser.add_argument(
        "--soften",
        action="store_true",
        help="blend the result with the target image to soften the result",
    )
    args = parser.parse_args()

    image_lib = ImageLib(
        im_dir=args.lib_dir,
        block_size=args.block_size,
        max_times=args.max_times,
        input_dir=args.input_dir,
    )
    target_image = ImageLib.resizeImage(args.target_image, args.output_width, args.output_height)

    result = createPuzzle(image_lib, args.block_size, target_image)
    target_image = Image.blend(result, target_image, 0.5) if args.soften else result
    target_image.save(args.output_file)
    printInfo(f"Saved result to {os.path.abspath(args.output_file)}")

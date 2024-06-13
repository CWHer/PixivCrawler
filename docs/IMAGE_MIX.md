# Mosaic Puzzles

The Chinese version of README can be found [here](./IMAGE_MIX_CN.md).

## Getting Started

### Parameters

```bash
$ python -m pixiv_utils.image_mix.mix_image --help
usage: mix_image.py [-h] -l LIB_DIR -t TARGET_IMAGE [-i INPUT_DIR] [-o OUTPUT_FILE] [-b BLOCK_SIZE] [-width OUTPUT_WIDTH] [-height OUTPUT_HEIGHT] [-m MAX_TIMES] [--soften]

options:
  -h, --help            show this help message and exit
  -l LIB_DIR, --lib-dir LIB_DIR
                        image lib directory (e.g., ./image_lib/) (default: None)
  -t TARGET_IMAGE, --target-image TARGET_IMAGE
                        target image path (e.g. ./images/44873217_p0.jpg) (default: None)
  -i INPUT_DIR, --input-dir INPUT_DIR
                        raw image directory (e.g., ./images/). NOTE: set to None if image lib is already constructed (default: None)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        output file path (e.g., ./result.png) (default: result.png)
  -b BLOCK_SIZE, --block-size BLOCK_SIZE
                        target image are divided into blocks (default: 50)
  -width OUTPUT_WIDTH, --output-width OUTPUT_WIDTH
                        width of output image (default: 4000)
  -height OUTPUT_HEIGHT, --output-height OUTPUT_HEIGHT
                        height of output image (default: 2000)
  -m MAX_TIMES, --max-times MAX_TIMES
                        max repeating times of lib blocks (default: 1)
  --soften              blend the result with the target image to soften the result (default: False)
```

- `-l LIB_DIR, --lib-dir LIB_DIR`: image lib directory

- `-t TARGET_IMAGE, --target-image TARGET_IMAGE`: target image path

- `-i INPUT_DIR, --input-dir INPUT_DIR`: raw image directory

- `-o OUTPUT_FILE, --output-file OUTPUT_FILE`: output file path

- `-b BLOCK_SIZE, --block-size BLOCK_SIZE`: target image are divided into blocks / size of each block in the image lib

- `-width OUTPUT_WIDTH, --output-width OUTPUT_WIDTH`: width of output image

- `-height OUTPUT_HEIGHT, --output-height OUTPUT_HEIGHT`: height of output image

- `-m MAX_TIMES, --max-times MAX_TIMES`: max repeating times of lib blocks

- `--soften`: blend the result with the target image to soften the result

### Usage

:warning: Construct the image lib based on raw images for the first time, and no need to rebuild for subsequent use

- First-time usage example

  ```bash
  python -m pixiv_utils.image_mix.mix_image \
      -l ../image_lib/ \
      -t ../images/44873217_p0.jpg \
      -i ../images/ \
      -b 100 \
      -width 2000 \
      -height 1000 \
      -m 2
  ```

- Subsequent usage example

  No need to add `-i INPUT_DIR, --input-dir INPUT_DIR` parameter

  ```bash
  python -m pixiv_utils.image_mix.mix_image \
      -l ../image_lib/ \
      -t ../images/44873217_p0.jpg \
      -b 100 \
      -width 2000 \
      -height 1000 \
      -m 2
  ```

## Algorithm

Please refer to the comments in [`mix_image.py`](../pixiv_utils/image_mix/mix_image.py)

1. Convert the original image into color blocks and create a color block library.

2. For each color block of the target image, select the closest color block in the color block library for replacement.

set -xue

# Run the tests
python -m unittest discover -s test_image_mix
python -m unittest discover -s test_pixiv_crawler

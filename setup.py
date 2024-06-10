from typing import List

import setuptools


def fetchRequirements(path: str) -> List[str]:
    """
    This function reads the requirements file.

    Args:
        path (str): the path to the requirements file.

    Returns:
        The lines in the requirements file.
    """
    with open(path, "r") as fd:
        return [r.strip() for r in fd.readlines()]


setuptools.setup(
    name="pixiv_utils",
    version="1.0.0",
    author="Wenhao Chen",
    author_email="cwher@outlook.com",
    description="Pixiv Utils implemented in Python, including Pixiv crawler and mosaic puzzles, support for rankings, personal favorites, artist works, keyword search and other filtering functions, and provide high-performance multi-threaded parallel download.",
    url="https://github.com/CWHer/PixivCrawler",
    packages=setuptools.find_packages(),
    install_requires=fetchRequirements("requirements/requirements.txt"),
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

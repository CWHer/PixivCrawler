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
    with open(path, "r") as f:
        return [r.strip() for r in f.readlines()]


def fetchReadme(path: str) -> str:
    """
    This function reads the README file.

    Args:
        path (str): the path to the README file.

    Returns:
        The content in the README file.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


setuptools.setup(
    name="pixiv_utils",
    version="1.0.2",
    author="Wenhao Chen",
    author_email="cwher@outlook.com",
    description="Pixiv Utils implemented in Python, including Pixiv crawler and mosaic puzzles, support for rankings, personal favorites, artist works, keyword search and other filtering functions, and provide high-performance multi-threaded parallel download.",
    long_description=fetchReadme("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/CWHer/PixivCrawler",
    packages=setuptools.find_packages(
        exclude=(
            "docs",
            "tests",
            "requirements",
            "*.egg-info",
        ),
    ),
    py_modules=["tutorial"],
    install_requires=fetchRequirements("requirements/requirements.txt"),
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

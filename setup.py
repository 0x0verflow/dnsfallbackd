import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dnsfallbackd",
    version="0.0.1",
    author="0x0verflow",
    description="Always keep your sevices online using some trickery with DNS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0x0verflow/dnsfallbackd",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Linux",
    ],
    python_requires='>=3.6',
)

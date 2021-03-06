import setuptools

with open("README.md", "rt") as f:
    long_description = f.read()

requirements = ["numpy", "gym", "tensorflow", "keras-rl", "wandb"]

setuptools.setup(
    name="playtest",
    license="MIT",
    version="0.0.10",
    description="A library for rapid prototyping of boardgames.",
    author="Boris Lau",
    author_email="boris@techie.im",
    url="https://github.com/dat-boris/py-playtest",
    packages=setuptools.find_namespace_packages(include=["playtest", "playtest.*"]),
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
)

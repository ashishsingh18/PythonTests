import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="InvertImage",
    version="1.0.0",
    author="Ashish Singh",
    author_email="Ashish.Singh@pennmedicine.upenn.edu",
    description="A utility to invert gray scale image intensity",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    # entry_points={
        # 'console_scripts': [
            # 'pyhydra = pyhydra.main:main',
        # ],
    # },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ),
)


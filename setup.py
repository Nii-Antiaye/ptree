from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ptree",
    version="0.1.0",
    author="nii-antiaye",
    description="A colorful directory tree utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nii-Antiaye/ptree",
    packages=find_packages(),
    package_data={"ptree": ["icons-sample.yaml"]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "colorama>=0.4.0",
        "pyyaml>=5.0",
    ],
    entry_points={"console_scripts": ["ptree=ptree.main:main"]},
)

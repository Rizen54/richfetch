import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = []
for line in open("requirements.txt").readlines():
    req = line.strip()
    if req.startswith("#") or req == "":
        continue
    requirements.append(req)


setuptools.setup(
    name="richfetch",
    version="0.1.0",
    description="A minimal and colorful fetch utility.",
    author="Satvik Pandey (Rizen54)",
    author_email="psatvik54@proton.me",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rizen54/richfetch/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
)

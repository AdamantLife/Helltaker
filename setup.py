import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Helltaker",
    version="0.0.1",
    author="AdamantLife",
    author_email="",
    description="Backend code to replicate Helltaker gameplay",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        
        ],
    entry_points = {
        'console_scripts': [
            
        ]
    }
)
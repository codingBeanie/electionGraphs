from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.1.3'
DESCRIPTION = 'Create graphs for displaying the result of a election based on a csv-inputfile.'

# Setting up
setup(
    name="electionGraphs",
    version=VERSION,
    author="ricochan (alpakaFred)",
    author_email="<mico.chan@mailbox.org>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pandas', 'plotly', 'kaleido', 'pillow'],
    keywords=['python', 'elections', 'voting', 'graphs', 'charts'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)

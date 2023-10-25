from setuptools import setup, find_packages

VERSION = '1.0'
DESCRIPTION = 'Create graphs for displaying the result of a election based on a csv-inputfile.'
LONG_DESCRIPTION = 'With ElectionResultGraphs you can create either four different graph types or all graphs as one chart for displaying the result of a election based on a csv-inputfile.'

# Setting up
setup(
    name="ElectionResultGraphs",
    version=VERSION,
    author="ricochan (alpakaFred)",
    author_email="<mico.chan@mailbox.org>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas', 'plotly', 'kaleido', 'pillow'],
    keywords=['python', 'elections', 'voting', 'graphs', 'charts'],
    classifiers=[
        "Development Status :: Finished",
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ]
)

# Voting Graph Portfolio
**The Voting Graph Portfolio** creates four different graphs for displaying the result of an election. The graphs can either be created seperately or combined into one chart.
As input a ´pandas´ ´dataFrame´ needs to be provided. In the initialization the provided ´dataFrame´ will be processed. Relative votings, as well as a seat distribution for a parliament will be calculated and later be displayed.
This tool is loosly based on german elections. Some rulesets may differ from the reality (e.g. not considering first vote, second vote). This is just a hobby project for practicing data processing and data visualization.

## Quickstart

## Example Code

## Example Graph
###  One Pager with multiple different graphs
![Example Chart](https://github.com/ricochan/VotingGraphPortfolio/blob/main/output/ElectionResults_2021.png "Example Chart")

## VotingGraphs

For the initialization the mandatory parameters must be given.

```python
from votingGraphPortfolio import VotingGraphs

votingGraphs = VotingGraphs(
    "data/exampleData.csv",
    "YEAR",
    "VOTINGS",
    "PARTY_SHORT",
    "PARTY_SPEC",
    "PARTY_COLOR",
)
```

After initialization different aspects of logic and styling can be configured by setting the optional parameters:

```python
votingGraphs.titleMain = "My other Title"
votingGraphs.colors["background"] = "#000000"
votingGraphs.fontsize["titleMain"] = 58
```

### mandatory parameters

`csvFile` = *(str)* csv file to read in -- [For example of the structure of csv see example file](data/exampleData.csv)

`columnYear` = *(str)* name of column in csv in which the year is recorded

`columnVotings` = *(str)* name of column in csv in which the absolute number of votings per party is recorded

`columnParty` = *(str)* name of column in csv in which party name is recorded 

`columnSpectrum` = *(str)* name of column in csv in which the political orientation of the party is recorded

`columnColor` = *(str)* name of column in csv in which the color code of the party is recorded

### optional parameters

`colors` = *(dict)* hex-color for different elements of the graphs. The value must be a *str* of hex-color (e.g. `"#F2EAD3"`) with following keys: 
   `background`
   `diagram`
   `title`
   `subtitle` 
   `yaxis` 
   `xaxis` 
   `grid` 
   `values` 
   `threshold` 

`excludeParties` = *(list, default = ["Sonstiges", "Sonstige", "Other"])* list of party names which will not be included in the seat allocation

`parliamentSeats` = *(int, default = 120)* number of seats in parliament

`percentageLimit` = *(int, default = 5)* threshold at which a party will not be considered when calculting seat distribution

`height` = *(int, default = 800)* height of a single graph, the onePager will be around two times larger

`seperator` = *(str, default = ";")* type of seperator in csv

`width` = *(int, default = 1200)* width of a single graph, the onePager will be around two times larger





# Project Management
## Goals
* :white_check_mark: done / implemented 
* :large_orange_diamond: in developement / not ready
* :red_circle: open
* :no_entry: cancelled/dismissed

### Data Processing
* :white_check_mark:  import CSV-file with voting results (as absolute numbers) for multiple years
* :white_check_mark:  calculating the relative voting numbers
* :white_check_mark: compare the percentage difference to last year votings
* :white_check_mark:  calculating a seat distribution for a parliament according to the relative results
* :white_check_mark:  take into account a 5%-restriction (or user defined) for minimum vote count 
* :white_check_mark:   calculate possible coalitions 


### Data Visualization
* :white_check_mark:  create a bar graph with results
* :white_check_mark:  create a bar graph with results compared to last year
* :white_check_mark:  create a bar graph with seat distribution in parliament
* :white_check_mark:  create a visulisation for possible coalitions
* :white_check_mark: create a pdf/png with all graphs combined

### Extra Goals
* :white_check_mark:  add styling options/method for customization (color and font-sizes can be changed)

### Finish Touch
* :large_orange_diamond: review code and optimize
* :large_orange_diamond:create documentation
* :red_circle: create and publish as package

### Bugs
* :white_check_mark: rounding error/problems where more seats are allocated than the defined maximum
* :white_check_mark:  error when party is new and there are no previous years
* :white_check_mark:  exclude user specific parties (e.g. sum of smaller parties that should not get parliament seats)

## Dependencies
* pandas
* plotly
* kaleido
* pillow
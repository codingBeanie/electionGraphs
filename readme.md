# Voting Graph Portfolio
**The Voting Graph Portfolio** creates four different graphs for displaying the result of an election. The graphs can either be created seperately or combined into one chart.
As input a `csv-file` needs to be provided. In the initialization the data will be processed as `pandas` `dataframe` and graphs from `plotly` can be exported as image-files.

## Features
* data from the csv-file will be processed and more data points will be calculated (initialization)
* a `.getGraph()` function can create different types of graphs
* a bar graph showing the results in relative votes can be displayed
* a bar graph showing a comparision of relative votes to last voting period
* a pie chart shows the seat allocation of the parliament
* a stacked bar chart shows possible coalitions
* `.createOnePager()` creates all graph options and combines them into one chart

### Seat Allocation (Parliament)
* seats of a parliament will be allocated based on relative voting results
* a threshold is implemented, so that a party needs to reach a certain relative voting result in order to be considered in the seat allocation (this feature can be adjusted by parameters)
* a list of parties can be excluded from the seat allocation (e.g. a "other" category)
* for the seat allocation the relative results (excluding parties that are defined by the `excludeParties` parameters or by the `percentageLimit`) will be multiplied by `parliamentSeats`, the result will be floored. Not allocated seats will then be allocated each party ordered by the highest modulus (decimal rest from the division) until all seats are allocated

### Coalitions
* coalitions will be calculated based on total seats. The political spectrum will be considered as a threshold
* for every possible coaltion the distance based on the delivered information of `columnSpectrum` will be calculated. Reaches the overall distance the `thresholdPoliticalDistance` the coalition will not be included in the final graph


## Disclaimer
*This tool is loosly based on german elections. Some rulesets may differ from the reality (e.g. not considering first vote, second vote). This is just a hobby project for practicing data processing and data visualization.*

## Example Graph
###  One Pager with multiple different graphs
![Example One Pager](https://github.com/ricochan/VotingGraphPortfolio/blob/main/output/ElectionResults_2021.png "Example One Pager")

###  One Pager with multiple different graphs
![Example Bar Resulr](https://github.com/ricochan/VotingGraphPortfolio/blob/main/output/barResult.png "Example Bar Result")

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

`colors` = *(dict{str:str})* hex-color for different elements of the graphs. The value must be a *str* of hex-color (e.g. `"#F2EAD3"`) with following keys: 
   `background`
   `diagram`
   `title`
   `subtitle` 
   `yaxis` 
   `xaxis` 
   `grid` 
   `values` 
   `threshold` 

`excludeParties` = *(list[str], default = ["Sonstiges", "Sonstige", "Other"])* list of party names which will not be included in the seat allocation

`filenameBarCompare` = *(str, default =  "barDifference.png")* filename of export graph. Must be a .png file

`filenameBarResult` = *(str, default =  "barResult.png")* filename of export graph. Must be a .png file

`filenameBarCoalitions` = *(str, default =  "barCoalition.png")* filename of export graph. Must be a .png file

`filenameOnePager` = *(str, default =  "ElectionResults")* filename of export graph. Must be a .png file

`filenamePieParliament` = *(str, default =  "pieParliament.png")* filename of export graph. Must be a .png file

`fontfamily` = *(str, default = "Futura")* font family of all graphs

`fontsize` = *(dict{str:int})* font sizes of different elements. Each key represent a text type with following options: 
   `title`
   `subtitle`
   `values`
   `yaxis`
   `xaxis`

`height` = *(int, default = 800)* height of a single graph, the onePager will be around two times larger

`parliamentSeats` = *(int, default = 120)* number of seats in parliament

`percentageLimit` = *(int, default = 5)* threshold at which a party will not be considered when calculting seat distribution

`thresholdPolitcalDistance` = *(int, default = 300)* defines a threshold for displaying possible coalitions. When the politcal distance in a mathmatical possible coalition is too high, it can be filtered

`titleBarCoalitions` = *(str, default="Koalitionen")* adjusts title of bar graph with possible coalitions

`titleBarCompare` = *(str, default="Veränderung der Wählerstimmen")* adjusts title of bar graph with comparision to last voting

`titleBarResult` = *(str, default="Wählerstimmen")* adjusts title of bar graph with results

`titleMain` = *(str, default="Wahlergebnisse")* adjusts main title of one pager

`titlePieParliament` = *(str, default="Sitzverteilung")* adjusts  title of parliament graph

`seperator` = *(str, default = ";")* type of seperator in csv

`subtitleBarCoalitions`= *(str, default="Anzahl Sitze für mögliche Koalitionen")* adjusts a subtitle of corresponding graph

`subtitleBarCompare` = *(str, default="Prozentpunkte im Vergleich zur letzten Wahl")* adjusts a subtitle of corresponding graph

`subtitleBarResult` = *(str, default="Anteil der Wählerstimmen in Prozent")* adjusts a subtitle of corresponding graph

`subtitlePieParliament` = *(str, default="Anzahl Sitze im Parlament")* adjusts a subtitle of corresponding graph

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
# Voting Graph Portfolio
**The Voting Graph Portfolio** is a python class that allows to create different voting charts/graphs. This class takes a pandas dataframe as input and processes the data in order to display the graphs accordingly.
This tool is loosly based on german elections. Some rulesets may differ from the reality. This is just a hobby project for practicing data processing and data visualization.

## Example Graph
###  One Pager with multiple different graphs
![Example Chart](https://github.com/ricochan/VotingGraphPortfolio/blob/main/output/ElectionResult_2021.png "Example Chart")


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
* :red_circle: review code and optimize
* :red_circle: create documentation
* :red_circle: create and publish as package

### Known Bugs
* :red_circle: rounding error/problems where more seats are allocated than the defined maximum

## Dependencies
* pandas
* plotly
* kaleido
* pillow
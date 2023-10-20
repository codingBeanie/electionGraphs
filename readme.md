# Voting Graph Portfolio
Create a nice one-page portfolio of the most relevant graphs for a democratic election (parliament elections). This tool is loosly based on german elections. Some rulesets may differ from the reality. This is just a hobby project for practicing data handling and data visualization.

# Examples
![Example Chart](https://github.com/ricochan/VotingGraphPortfolio/blob/main/output/barResult.png "Example Chart")

# Goals
:white_check_mark: done / implemented 
:large_orange_diamond: in developement / not ready
:red_circle: open
:no_entry: cancelled/dismissed

## Data Processing
* :white_check_mark:  import CSV-file with voting results (as absolute numbers) for multiple years
* :white_check_mark:  calculating the relative voting numbers
* :white_check_mark::  compare the percentage difference to last year votings
* :white_check_mark:  calculating a seat distribution for a parliament according to the relative results
* :white_check_mark:  take into account a 5%-restriction (or user defined) for minimum vote count 
* :white_check_mark:   calculate possible coalitions 


## Data Visualization
* :white_check_mark:  create a bar graph with results
* :large_orange_diamond:  create a bar graph with results compared to last year
* :large_orange_diamond:  create a bar graph with seat distribution in parliament
* :large_orange_diamond:  create a visulisation for possible coalitions
* :red_circle: create a pdf/png with all graphs combined


## Dependencies
* pandas
* plotly
* kaleido
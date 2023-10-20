###########################################################
# Class for processing voting data
###########################################################
import pandas as pd
from itertools import combinations
import plotly.express as plotly
from plotly.io import to_image


class VotingData:
    def __init__(self, csvFile,  columnYear, columnVotings, columnParty, columnSpectrum, columnColor, parliamentSeats, seperator=";", percentageLimit=5):

        # read the csv and create the base dataFrame
        self.dataFrame = pd.read_csv(csvFile, sep=seperator)

        ###########################################################
        # Input Variables
        ###########################################################

        self.parliamentSeats = parliamentSeats
        self.columnYear = columnYear
        self.columnParty = columnParty
        self.columnSpectrum = columnSpectrum
        self.columnColor = columnColor
        self.percentageLimit = percentageLimit

        ###########################################################
        # Styling Variable
        ##########################################################
        self.colors = {"background": "#F2EAD3",
                       "diagram": "#F5F5F5",
                       "title": "#3F2305",
                       "subtitle": "#3F2305",
                       "yaxis": "#3F2305",
                       "xaxis": "#3F2305",
                       "grid": "#DFD7BF",
                       "values": "#3F2305",
                       "threshold": "#DFD7BF"}

        yearsInDataFrame = sorted(
            self.dataFrame[self.columnYear].unique())

        ###########################################################
        # data processing
        ###########################################################

        # calculate the total and relative votes for each year in dataFrame
        for year in yearsInDataFrame:
            totalVotes = self.dataFrame.loc[self.dataFrame[self.columnYear]
                                            == year, columnVotings].sum()
            self.dataFrame.loc[self.dataFrame[self.columnYear] == year, "VOTINGS_RELATIVE"] = round(
                self.dataFrame[columnVotings] / totalVotes * 100, 3
            )
            # sum of all votes that are above 5%
            totalVotesAboveLimit = self.dataFrame.loc[
                (self.dataFrame[self.columnYear] == year) & (
                    self.dataFrame["VOTINGS_RELATIVE"] >= percentageLimit), columnVotings
            ].sum()

            # calculate the number of seats for each party which is above the percentage limit
            self.dataFrame.loc[
                (self.dataFrame[self.columnYear] == year) & (
                    self.dataFrame["VOTINGS_RELATIVE"] >= 5), ["SEATS"]
            ] = round(parliamentSeats * self.dataFrame[columnVotings] / totalVotesAboveLimit)
            self.dataFrame["SEATS"] = self.dataFrame["SEATS"].fillna(0)
            self.dataFrame["SEATS"] = self.dataFrame["SEATS"].astype(int)

        # Calculate the difference of REL to the previous year
            for party in self.dataFrame[self.columnParty].unique():
                for i, year in enumerate(yearsInDataFrame):
                    if i != 0:
                        # filter the dataFrame by year and party and calculate the difference
                        currentRel = self.dataFrame.loc[
                            (self.dataFrame[self.columnYear] == year) & (
                                self.dataFrame[self.columnParty] == party), "VOTINGS_RELATIVE"
                        ].values[0]
                        previousRel = self.dataFrame.loc[
                            (self.dataFrame[self.columnYear]
                             == yearsInDataFrame[i - 1])
                            & (self.dataFrame[self.columnParty] == party),
                            "VOTINGS_RELATIVE",
                        ].values[0]
                        difference = round(currentRel - previousRel, 3)

                        # add the difference to the dataFrame
                        self.dataFrame.loc[
                            (self.dataFrame[self.columnYear] == year) & (
                                self.dataFrame[self.columnParty] == party),
                            "VOTINGS_RELATIVE_DIFF",
                        ] = difference
                    else:
                        self.dataFrame.loc[
                            (self.dataFrame[self.columnYear] == year) & (
                                self.dataFrame[self.columnParty] == party),
                            "VOTINGS_RELATIVE_DIFF",
                        ] = None

##############################################################################################################################
##### getCoalitions #########################################################################################################
##############################################################################################################################

    def getCoalitions(self, year, thresholdPolitcalDistance=300, deleteSubsets=True):
        dataParties = self.dataFrame.loc[(
            self.dataFrame[self.columnYear] == year) & (self.dataFrame["SEATS"] > 0)]

        arrayParties = dataParties[self.columnParty].to_list()

        # get all possible combinations of coalitions
        # create an empty dataframe
        dataCoalitions = pd.DataFrame(
            columns=["PARTIES", "SEATS", "MAJORITY", "POLITCAL_DISTANCE"])

        # iterate through all possible combinations
        for i in range(2, len(arrayParties) + 1):
            for combination in list(combinations(arrayParties, i)):

                # calculate the number of seats for each coalition
                coalitionSeats = 0
                politcalOrientation = []
                for party in combination:
                    coalitionSeats += self.dataFrame.loc[(self.dataFrame[self.columnYear] == year) & (
                        self.dataFrame[self.columnParty] == party), "SEATS"].values[0]
                    politcalOrientation.append(self.dataFrame.loc[(self.dataFrame[self.columnYear] == year) & (
                        self.dataFrame[self.columnParty] == party), self.columnSpectrum].values[0])

                # calculate the politcal distance between the parties
                politcalDistance = []
                for i in range(len(politcalOrientation) - 1):
                    baseValue = politcalOrientation[i]
                    for j in range(i + 1, len(politcalOrientation)):
                        politcalDistance.append(
                            abs(baseValue - politcalOrientation[j]))
                politcalDistance = int(sum(
                    politcalDistance))
                # check if the coalition has the majority
                if coalitionSeats >= self.parliamentSeats / 2:
                    majority = True
                else:
                    majority = False

                # add the coalition to the dataFrame
                dataCoalitions = dataCoalitions._append(
                    {"PARTIES": combination, "SEATS": coalitionSeats, "MAJORITY": majority, "POLITCAL_DISTANCE": politcalDistance}, ignore_index=True)
                # filter the dataFrame by majority and threshold of politcal distance

                dataCoalitions = dataCoalitions.loc[(dataCoalitions["MAJORITY"] == True) & (
                    dataCoalitions["POLITCAL_DISTANCE"] <= thresholdPolitcalDistance)]
        # end for
        if deleteSubsets:
            # loop through dataframe and find coalitions that are a subset of other coalitions (which have less parties involved)
            deleteRows = []
            for i in range(len(dataCoalitions)):
                for ii in range(i + 1, len(dataCoalitions)):
                    if set(dataCoalitions.loc[i, "PARTIES"]).issubset(set(dataCoalitions.loc[ii, "PARTIES"])):
                        if ii not in deleteRows:
                            deleteRows.append(ii)

                    elif set(dataCoalitions.loc[ii, "PARTIES"]).issubset(set(dataCoalitions.loc[i, "PARTIES"])):
                        if i not in deleteRows:
                            deleteRows.append(i)

            # delete indeces from dataframe that are a subset of other coalitions
            dataCoalitions = dataCoalitions.drop(deleteRows)

        # sort by politcal distance
        dataCoalitions = dataCoalitions.sort_values(
            by="POLITCAL_DISTANCE", ascending=True)
        return dataCoalitions

##############################################################################################################################
##### getGraph ##############################################################################################################
##############################################################################################################################

    def getGraph(self, year, type, outputfile, title="VOTING", subtitle=""):

        # set up a dedicated dataframe for the graph
        printData = self.dataFrame[self.dataFrame[self.columnYear] == year].sort_values(
            by=["VOTINGS_RELATIVE"], ascending=False
        )

        # format the column votings_relative to 1 decimal place
        printData["VOTINGS_RELATIVE"] = printData["VOTINGS_RELATIVE"].apply(
            lambda x: round(x, 1))
        printData["VOTINGS_RELATIVE_DIFF"] = printData["VOTINGS_RELATIVE_DIFF"].apply(
            lambda x: round(x, 1))

        # for displaying purposes
        partyColors = printData[self.columnColor].tolist()
        titleText = title + " " + str(year)

        # for a mostly uniform look, the yaxis range is set based on the maximum value
        maxValue = printData["VOTINGS_RELATIVE"].max()
        if maxValue > 80:
            yRange = [0, 100]
        elif maxValue > 60:
            yRange = [0, 85]
        elif maxValue > 40:
            yRange = [0, 65]
        elif maxValue > 20:
            yRange = [0, 45]

        ############################################################################################
        # BAR_RESULT
        ############################################################################################

        if type == "BAR_RESULT":
            # Creating the main bar graph
            barResult = plotly.bar(
                printData,
                x=self.columnParty,
                y="VOTINGS_RELATIVE",
                color=self.columnParty,
                color_discrete_sequence=partyColors,
                text="VOTINGS_RELATIVE",
            )

            # configure layout and other visuals
            barResult.update_layout(
                title={"text": "<b>" + titleText +
                       "</b>", "font": {"size": 31, "color": self.colors["title"]},  "x": 0.06, "y": 0.97},
                paper_bgcolor=self.colors["background"],
                plot_bgcolor=self.colors["diagram"],

                showlegend=False,
                margin={"t": 70, "b": 0, "l": 0, "r": 20},
                yaxis=dict(range=yRange, gridcolor=self.colors["grid"]),
                annotations=[
                    dict(
                        x=0,
                        y=1.08,
                        xref="paper",
                        yref="paper",
                        text="<i>"+subtitle+"</i>",
                        showarrow=False,
                        font=dict(size=16, color=self.colors["subtitle"])
                    )
                ],
            )
            barResult.update_xaxes(title="", tickfont=dict(
                size=18, color=self.colors["xaxis"]))
            barResult.update_yaxes(title="", tickfont=dict(
                size=10, color=self.colors["yaxis"]))
            barResult.update_traces(
                textfont_size=16, textposition="outside",  textfont_color=self.colors["values"])

            # add line for 5% threshold
            barResult.add_hline(y=self.percentageLimit, line_width=3,
                                line_color=self.colors["threshold"], layer="below")

            # export as png
            image_bytes = to_image(barResult, format="png", scale=3)
            with open(outputfile, "wb") as f:
                f.write(image_bytes)

        ############################################################################################
        # BAR_DIFFERENCE
        ############################################################################################
        if type == "BAR_DIFFERENCE":

            # Creating the main bar graph
            barDifference = plotly.bar(
                printData,
                x=self.columnParty,
                y="VOTINGS_RELATIVE_DIFF",
                color=self.columnParty,
                color_discrete_sequence=partyColors,
                text="VOTINGS_RELATIVE_DIFF",
            )

            # configure layout and other visuals
            barDifference.update_layout(
                title={"text": "<b>" + titleText +
                       "</b>", "font": {"size": 31, "color": self.colors["title"]}, "x": 0.07, "y": 0.97},
                showlegend=False,
                paper_bgcolor=self.colors["background"],
                plot_bgcolor=self.colors["diagram"],
                margin={"t": 70, "b": 0, "l": 0, "r": 20},
                yaxis=dict(range=[round(printData["VOTINGS_RELATIVE_DIFF"].min(
                ), 0) - 2, round(printData["VOTINGS_RELATIVE_DIFF"].max(), 0) + 2], gridcolor=self.colors["grid"]),
                annotations=[
                    dict(
                        x=0,
                        y=1.08,
                        xref="paper",
                        yref="paper",
                        text="<i>"+subtitle+"</i>",
                        showarrow=False,
                        font=dict(size=16, color=self.colors["subtitle"])
                    )
                ],
            )
            barDifference.update_xaxes(title="", tickfont=dict(
                size=18, color=self.colors["xaxis"]))
            barDifference.update_yaxes(title="", tickfont=dict(
                size=10, color=self.colors["yaxis"]))
            barDifference.update_traces(
                textfont_size=16, textposition="outside", textfont_color=self.colors["values"])

            # export as png
            image_bytes = to_image(barDifference, format="png", scale=3)
            with open(outputfile, "wb") as f:
                f.write(image_bytes)

##############################################################################################################################
##############################################################################################################################
##############################################################################################################################


votingData = VotingData("data/exampleData.csv", "YEAR",
                        "VOTINGS", "PARTY_SHORT", "PARTY_SPEC", "PARTY_COLOR", 120)

votingData.getGraph(2021, "BAR_RESULT",
                    outputfile="output/barResult.png", title="Wahl", subtitle="Anteil der Wählerstimmen in Prozent")
votingData.getGraph(2021, "BAR_DIFFERENCE",
                    outputfile="output/barDifference.png", title="Wahl", subtitle="Prozenzpunkte im Vergleich zur letzten Wahl")

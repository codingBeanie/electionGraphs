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
        # Variables
        ###########################################################

        self.parliamentSeats = parliamentSeats
        self.columnYear = columnYear
        self.columnParty = columnParty
        self.columnSpectrum = columnSpectrum
        self.columnColor = columnColor

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
##############################################################################################################################
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
##############################################################################################################################
##############################################################################################################################

    def getGraph(self, year, type, outputfile, title="VOTING", subtitle=""):

        # set up a dedicated dataframe for the graph
        printData = self.dataFrame[self.dataFrame[self.columnYear] == year].sort_values(
            by=["VOTINGS_RELATIVE"], ascending=False
        )

        # format the column votings_relative to 1 decimal place
        printData["VOTINGS_RELATIVE"] = printData["VOTINGS_RELATIVE"].apply(
            lambda x: round(x, 1))

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

        if type == "BAR_RESULT":
            # for displaying purposes
            partyColors = printData[self.columnColor].tolist()
            titleText = title + " " + str(year)

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
                       "</b>", "font": {"size": 31}, "x": 0.06, "y": 0.97},
                showlegend=False,
                margin={"t": 70, "b": 0, "l": 0, "r": 20},
                yaxis=dict(range=yRange),
                annotations=[
                    dict(
                        x=0,
                        y=1.08,
                        xref="paper",
                        yref="paper",
                        text="<i>"+subtitle+"</i>",
                        showarrow=False,
                        font=dict(size=16)
                    )
                ],
            )
            barResult.update_xaxes(title="", tickfont=dict(size=18))
            barResult.update_yaxes(title="", tickfont=dict(size=12))
            barResult.update_traces(
                textfont_size=16, textposition="outside")

            # export as png
            image_bytes = to_image(barResult, format="png", scale=3)
            with open(outputfile, "wb") as f:
                f.write(image_bytes)


votingData = VotingData("data/exampleData.csv", "YEAR",
                        "VOTINGS", "PARTY_SHORT", "PARTY_SPEC", "PARTY_COLOR", 120)
# print(votingData.dataFrame)
# print(votingData.getCoalitions(
#    2021, thresholdPolitcalDistance=300, deleteSubsets=True))
votingData.getGraph(2017, "BAR_RESULT",
                    outputfile="output/barResult.png", title="Wahl", subtitle="Anzahl der Stimmen in Prozent")

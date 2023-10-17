###########################################################
# Class for processing voting data
###########################################################
import pandas as pd
from itertools import combinations


class VotingData:
    def __init__(self, csvFile,  columnYear, columnVotings, columnParty, columnSpectrum, parliamentSeats, seperator=";", percentageLimit=5):

        # read the csv and create the base dataFrame
        self.dataFrame = pd.read_csv(csvFile, sep=seperator)

        ###########################################################
        # Variables
        ###########################################################

        self.parliamentSeats = parliamentSeats
        self.columnYear = columnYear
        self.columnParty = columnParty
        self.columnSpectrum = columnSpectrum

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

    def getCoalitions(self, year):
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

                print(politcalOrientation)
                for i in range(len(politcalOrientation) - 1):
                    for j in range(i, len(politcalOrientation)):

                        print("i: ", i, "j: ", j, politcalOrientation[j])
                # check if the coalition has the majority
                if coalitionSeats >= self.parliamentSeats / 2:
                    majority = True
                else:
                    majority = False

                # add the coalition to the dataFrame
                dataCoalitions = dataCoalitions._append(
                    {"PARTIES": combination, "SEATS": coalitionSeats, "MAJORITY": majority, "POLITCAL_DISTANCE": politcalOrientation}, ignore_index=True)

        return dataCoalitions


votingData = VotingData("data/exampleData.csv", "YEAR",
                        "VOTINGS", "PARTY_SHORT", "PARTY_SPEC", 120)
# print(votingData.dataFrame)
print(votingData.getCoalitions(2017))

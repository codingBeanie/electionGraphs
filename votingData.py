###########################################################
# Class for processing voting data
###########################################################
import pandas as pd
import os
from itertools import combinations
import plotly.express as plotly
import plotly.graph_objects as go
from plotly.io import to_image
from PIL import Image


# REFACTOR
# use dict() instead of "x":0.4,
# check if update-layout is necessary


class VotingData:
    def __init__(
        self,
        csvFile,
        columnYear,
        columnVotings,
        columnParty,
        columnSpectrum,
        columnColor,
        parliamentSeats,
        seperator=";",
        percentageLimit=5,
        scale=3,
    ):
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
        self.scale = scale

        ###########################################################
        # Styling Variable
        ##########################################################
        self.colors = {
            "background": "#F2EAD3",
            "diagram": "#F5F5F5",
            "title": "#3F2305",
            "subtitle": "#3F2305",
            "yaxis": "#3F2305",
            "xaxis": "#3F2305",
            "grid": "#DFD7BF",
            "values": "#3F2305",
            "threshold": "#DFD7BF",
        }

        self.fontsize = {
            "title": 32,
            "subtitle": 16,
            "values": 16,
            "yaxis": 10,
            "xaxis": 18,
        }

        yearsInDataFrame = sorted(self.dataFrame[self.columnYear].unique())

        ###########################################################
        # data processing
        ###########################################################

        # calculate the total and relative votes for each year in dataFrame
        for year in yearsInDataFrame:
            totalVotes = self.dataFrame.loc[
                self.dataFrame[self.columnYear] == year, columnVotings
            ].sum()
            self.dataFrame.loc[
                self.dataFrame[self.columnYear] == year, "VOTINGS_RELATIVE"
            ] = round(self.dataFrame[columnVotings] / totalVotes * 100, 3)
            # sum of all votes that are above 5%
            totalVotesAboveLimit = self.dataFrame.loc[
                (self.dataFrame[self.columnYear] == year)
                & (self.dataFrame["VOTINGS_RELATIVE"] >= percentageLimit),
                columnVotings,
            ].sum()

            # calculate the number of seats for each party which is above the percentage limit
            self.dataFrame.loc[
                (self.dataFrame[self.columnYear] == year)
                & (self.dataFrame["VOTINGS_RELATIVE"] >= 5),
                ["SEATS"],
            ] = round(
                parliamentSeats *
                self.dataFrame[columnVotings] / totalVotesAboveLimit
            )
            self.dataFrame["SEATS"] = self.dataFrame["SEATS"].fillna(0)
            self.dataFrame["SEATS"] = self.dataFrame["SEATS"].astype(int)

            # Calculate the difference of REL to the previous year
            for party in self.dataFrame[self.columnParty].unique():
                for i, year in enumerate(yearsInDataFrame):
                    if i != 0:
                        # filter the dataFrame by year and party and calculate the difference
                        currentRel = self.dataFrame.loc[
                            (self.dataFrame[self.columnYear] == year)
                            & (self.dataFrame[self.columnParty] == party),
                            "VOTINGS_RELATIVE",
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
                            (self.dataFrame[self.columnYear] == year)
                            & (self.dataFrame[self.columnParty] == party),
                            "VOTINGS_RELATIVE_DIFF",
                        ] = difference
                    else:
                        self.dataFrame.loc[
                            (self.dataFrame[self.columnYear] == year)
                            & (self.dataFrame[self.columnParty] == party),
                            "VOTINGS_RELATIVE_DIFF",
                        ] = None

    ##############################################################################################################################
    ##### getCoalitions #########################################################################################################
    ##############################################################################################################################

    def getCoalitions(self, year, thresholdPolitcalDistance=300, deleteSubsets=True):
        dataParties = self.dataFrame.loc[
            (self.dataFrame[self.columnYear] == year) & (
                self.dataFrame["SEATS"] > 0)
        ]

        arrayParties = dataParties[self.columnParty].to_list()

        # get all possible combinations of coalitions
        # create an empty dataframe
        dataCoalitions = pd.DataFrame(
            columns=["PARTIES", "SEATS", "MAJORITY", "POLITCAL_DISTANCE"]
        )

        # iterate through all possible combinations
        for i in range(2, len(arrayParties) + 1):
            for combination in list(combinations(arrayParties, i)):
                # calculate the number of seats for each coalition
                coalitionSeats = 0
                politcalOrientation = []
                for party in combination:
                    coalitionSeats += self.dataFrame.loc[
                        (self.dataFrame[self.columnYear] == year)
                        & (self.dataFrame[self.columnParty] == party),
                        "SEATS",
                    ].values[0]
                    politcalOrientation.append(
                        self.dataFrame.loc[
                            (self.dataFrame[self.columnYear] == year)
                            & (self.dataFrame[self.columnParty] == party),
                            self.columnSpectrum,
                        ].values[0]
                    )

                # calculate the politcal distance between the parties
                politcalDistance = []
                for i in range(len(politcalOrientation) - 1):
                    baseValue = politcalOrientation[i]
                    for j in range(i + 1, len(politcalOrientation)):
                        politcalDistance.append(
                            abs(baseValue - politcalOrientation[j]))
                politcalDistance = int(sum(politcalDistance))
                # check if the coalition has the majority
                if coalitionSeats > self.parliamentSeats / 2:
                    majority = True
                else:
                    majority = False

                # add the coalition to the dataFrame
                dataCoalitions = dataCoalitions._append(
                    {
                        "PARTIES": combination,
                        "SEATS": coalitionSeats,
                        "MAJORITY": majority,
                        "POLITCAL_DISTANCE": politcalDistance,
                    },
                    ignore_index=True,
                )
                # filter the dataFrame by majority and threshold of politcal distance

                dataCoalitions = dataCoalitions.loc[
                    (dataCoalitions["MAJORITY"] == True)
                    & (dataCoalitions["POLITCAL_DISTANCE"] <= thresholdPolitcalDistance)
                ]
        # end for
        if deleteSubsets:
            # loop through dataframe and find coalitions that are a subset of other coalitions (which have less parties involved)
            deleteRows = []
            for i in range(len(dataCoalitions)):
                for ii in range(i + 1, len(dataCoalitions)):
                    if set(dataCoalitions.loc[i, "PARTIES"]).issubset(
                        set(dataCoalitions.loc[ii, "PARTIES"])
                    ):
                        if ii not in deleteRows:
                            deleteRows.append(ii)

                    elif set(dataCoalitions.loc[ii, "PARTIES"]).issubset(
                        set(dataCoalitions.loc[i, "PARTIES"])
                    ):
                        if i not in deleteRows:
                            deleteRows.append(i)

            # delete indeces from dataframe that are a subset of other coalitions
            dataCoalitions = dataCoalitions.drop(deleteRows)

        # sort by politcal distance
        dataCoalitions = dataCoalitions.sort_values(
            by="POLITCAL_DISTANCE", ascending=True
        )
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
            lambda x: round(x, 1)
        )
        printData["VOTINGS_RELATIVE_DIFF"] = printData["VOTINGS_RELATIVE_DIFF"].apply(
            lambda x: round(x, 1)
        )

        # for displaying purposes
        partyColors = printData[self.columnColor].tolist()

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
                title={
                    "text": "<b>" + title + "</b>",
                    "font": {
                        "size": self.fontsize["title"],
                        "color": self.colors["title"],
                    },
                    "x": 0.06,
                    "y": 0.97,
                },
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
                        text="<i>" + subtitle + "</i>",
                        showarrow=False,
                        font=dict(
                            size=self.fontsize["subtitle"],
                            color=self.colors["subtitle"],
                        ),
                    )
                ],
            )
            barResult.update_xaxes(
                title="",
                tickfont=dict(
                    size=self.fontsize["xaxis"], color=self.colors["xaxis"]),
            )
            barResult.update_yaxes(
                title="",
                tickfont=dict(
                    size=self.fontsize["yaxis"], color=self.colors["yaxis"]),
            )
            barResult.update_traces(
                textfont_size=self.fontsize["values"],
                textposition="outside",
                textfont_color=self.colors["values"],
            )

            # add line for 5% threshold
            barResult.add_hline(
                y=self.percentageLimit,
                line_width=3,
                line_color=self.colors["threshold"],
                layer="below",
            )

            # export as png
            image_bytes = to_image(barResult, format="png", scale=self.scale)
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
                title={
                    "text": "<b>" + title + "</b>",
                    "font": {
                        "size": self.fontsize["title"],
                        "color": self.colors["title"],
                    },
                    "x": 0.07,
                    "y": 0.97,
                },
                showlegend=False,
                paper_bgcolor=self.colors["background"],
                plot_bgcolor=self.colors["diagram"],
                margin={"t": 70, "b": 0, "l": 0, "r": 20},
                yaxis=dict(
                    range=[
                        round(printData["VOTINGS_RELATIVE_DIFF"].min(), 0) - 2,
                        round(printData["VOTINGS_RELATIVE_DIFF"].max(), 0) + 2,
                    ],
                    gridcolor=self.colors["grid"],
                ),
                annotations=[
                    dict(
                        x=0,
                        y=1.08,
                        xref="paper",
                        yref="paper",
                        text="<i>" + subtitle + "</i>",
                        showarrow=False,
                        font=dict(
                            size=self.fontsize["subtitle"],
                            color=self.colors["subtitle"],
                        ),
                    )
                ],
            )
            barDifference.update_xaxes(
                title="",
                tickfont=dict(
                    size=self.fontsize["xaxis"], color=self.colors["xaxis"]),
            )
            barDifference.update_yaxes(
                title="",
                tickfont=dict(
                    size=self.fontsize["yaxis"], color=self.colors["yaxis"]),
            )
            barDifference.update_traces(
                textfont_size=self.fontsize["values"],
                textposition="outside",
                textfont_color=self.colors["values"],
            )

            # export as png
            image_bytes = to_image(
                barDifference, format="png", scale=self.scale)
            with open(outputfile, "wb") as f:
                f.write(image_bytes)

        ############################################################################################
        # PARLIAMENT GRAPH
        ############################################################################################
        if type == "PARLIAMENT":
            # filter the dataFrame by the threshold
            printDataParliament = printData.loc[
                (printData["VOTINGS_RELATIVE"] >= self.percentageLimit)
            ]

            # sort by politcal spectrum
            printDataParliament = printDataParliament.sort_values(
                by=[self.columnSpectrum], ascending=False
            )
            # add dummy row for displaying half-circle
            printDataParliament = printDataParliament._append(
                {
                    self.columnParty: "dummy",
                    "SEATS": self.parliamentSeats,
                    self.columnColor: self.colors["background"],
                },
                ignore_index=True,
            )

            # create Graph
            graphParliament = go.Figure(
                data=[
                    go.Pie(
                        labels=printDataParliament[self.columnParty],
                        values=printDataParliament["SEATS"],
                        title=dict(
                            text="<i>" + subtitle + "</i>",
                            font=dict(
                                size=self.fontsize["subtitle"],
                                color=self.colors["subtitle"],
                            ),
                            position="top left",
                        ),
                        text=printDataParliament[self.columnParty]
                        + " ("
                        + printDataParliament["SEATS"].astype(str)
                        + ")",
                        textinfo="text",
                        marker_colors=printDataParliament[self.columnColor],
                        textfont_size=self.fontsize["values"],
                        # textfont=dict(color=self.colors["values"]),
                        hole=0.3,
                        sort=False,
                        direction="clockwise",
                        rotation=270,
                        showlegend=False,
                    )
                ],
            )
            graphParliament.update_layout(
                margin=dict(l=0, r=0, t=40, b=0),
                paper_bgcolor=self.colors["background"],
                font=dict(color=self.colors["values"]),
                annotations=[
                    dict(
                        x=0.18,
                        y=1.08,
                        xref="paper",
                        yref="paper",
                        text="<b>" + title + "</b>",
                        showarrow=False,
                        font=dict(
                            size=self.fontsize["title"], color=self.colors["title"]
                        ),
                    )
                ],
            )
            # export as png
            image_bytes = to_image(
                graphParliament, format="png", scale=self.scale * 1.8
            )
            with open(outputfile, "wb") as f:
                f.write(image_bytes)
                # get image width
            with Image.open(outputfile) as img:
                width, height = img.size
                # crop image
                img.crop((0.1 * width, 0, width * 0.9,
                         height * 0.60)).save(outputfile)

        ##############################################################################################################################
        #### coalitionsGraph #########################################################################################################
        ##############################################################################################################################
        if type == "COALITIONS":
            printDataCoalitions = pd.DataFrame(
                columns=["COALITION", "PARTY", "SEATS"])
            coalitions = self.getCoalitions(year)
            for i in range(len(coalitions)):
                for p in coalitions.loc[i, "PARTIES"]:
                    partySeats = self.dataFrame.loc[
                        (self.dataFrame[self.columnYear] == year)
                        & (self.dataFrame[self.columnParty] == p),
                        "SEATS",
                    ].values[0]
                    printDataCoalitions = printDataCoalitions._append(
                        dict(COALITION=i, PARTY=p, SEATS=partySeats), ignore_index=True
                    )
            # sort by coalition and then seats
            printDataCoalitions = printDataCoalitions.sort_values(
                by=["COALITION", "SEATS"], ascending=[True, False])
            partyArray = printDataCoalitions["PARTY"].unique()
            partyColorsCoalitions = []
            for p in partyArray:
                partyColorsCoalitions.append(
                    self.dataFrame.loc[
                        (self.dataFrame[self.columnYear] == year)
                        & (self.dataFrame[self.columnParty] == p),
                        self.columnColor,
                    ].values[0]
                )

            # create Graph
            coalitionsGraph = plotly.bar(
                printDataCoalitions,
                x="SEATS",
                y="COALITION",
                color="PARTY",
                color_discrete_sequence=partyColorsCoalitions,
                text="PARTY",
                orientation="h",
                barmode="stack",
            )

            coalitionsGraph.update_traces(
                textposition="inside", insidetextanchor='middle', textfont_size=self.fontsize["values"])
            coalitionsGraph.update_layout(
                title=dict(
                    text="<b>" + title + "</b>",
                    font=dict(
                        size=self.fontsize["title"], color=self.colors["title"]),
                    x=0.03,
                    y=0.98,
                ),
                annotations=[
                    dict(
                        x=0,
                        y=1.08,
                        xref="paper",
                        yref="paper",
                        text="<i>" + subtitle + "</i>",
                        showarrow=False,
                        font=dict(
                            size=self.fontsize["subtitle"],
                            color=self.colors["subtitle"],
                        ),
                    )
                ],
                bargap=0.5,
                paper_bgcolor=self.colors["background"],
                plot_bgcolor=self.colors["diagram"],
                showlegend=False,
                margin={"t": 70, "b": 0, "l": 0, "r": 20},
                yaxis=dict(
                    gridcolor=self.colors["diagram"], title="", showticklabels=False),
                xaxis=dict(title="", gridcolor=self.colors["grid"]),
            ),

            # add line for majority
            coalitionsGraph.add_vline(
                x=self.parliamentSeats / 2,
                line_width=5,
                line_color=self.colors["threshold"],
                layer="below",
            )
            # export as png
            image_bytes = to_image(
                coalitionsGraph, format="png", scale=self.scale)
            with open(outputfile, "wb") as f:
                f.write(image_bytes)


##############################################################################################################################
#### createOnePager #########################################################################################################
##############################################################################################################################

    def createOnePager(self, year, outputfolder="output"):

        # title variables
        titleMain = "Wahl " + str(year)
        subtitleBarResult = "Anteil der Wählerstimmen in Prozent"
        subtitleBarCompare = "Prozentpunkte im Vergleich zur letzten Wahl"
        subtitlePieParliament = "Anzahl Sitze im Parlament"
        subtitleBarCoalitions = "Anzahl Sitze für mögliche Koalitionen"

        # filenames
        filenameBarResult = "barResult.png"
        filenameBarCompare = "barDifference.png"
        filenamePieParliament = "pieParliament.png"
        filenameBarCoalitions = "barCoalition.png"
        filenameOnePager = "ElectionResults_"+str(year)+".png"

        # create graphs
        self.getGraph(year, "BAR_RESULT",
                      outputfile=os.path.join(outputfolder, filenameBarResult), title=titleMain, subtitle=subtitleBarResult)
        self.getGraph(year, "BAR_DIFFERENCE",
                      outputfile=os.path.join(outputfolder, filenameBarCompare), title=titleMain, subtitle=subtitleBarCompare)
        self.getGraph(year, "PARLIAMENT",
                      outputfile=os.path.join(outputfolder, filenamePieParliament), title=titleMain, subtitle=subtitlePieParliament)
        self.getGraph(
            year,
            "COALITIONS",
            outputfile=os.path.join(outputfolder, filenameBarCoalitions),
            title=titleMain,
            subtitle=subtitleBarCoalitions,
        )

        imgBarResult = Image.open("output/barResult.png")
        imgBarCompare = Image.open("output/barDifference.png")
        imgPieParliament = Image.open("output/pieParliament.png")
        imgBarCoalitions = Image.open("output/barCoalition.png")

        widths = (imgBarResult.size[0] + imgBarCompare.size[0],
                  imgPieParliament.size[0] + imgBarCoalitions.size[0])
        heights = (imgBarResult.size[1] + imgPieParliament.size[1],
                   imgBarCompare.size[1] + imgBarCoalitions.size[1])

        # create onePager
        onePager = Image.new(
            "RGB",
            (
                max(widths),
                max(heights),
            ),
            color=self.colors["background"],
        )

        onePager.paste(imgBarResult, (0, 0))
        onePager.paste(imgPieParliament, (0, imgBarResult.size[1]))
        onePager.paste(imgBarCompare, (imgBarResult.size[0], 0))
        onePager.paste(
            imgBarCoalitions, (imgBarResult.size[0], imgBarCompare.size[1]))

        onePager.save(os.path.join(outputfolder, filenameOnePager),
                      "PNG", resolution=100.0)

##############################################################################################################################
##############################################################################################################################
##############################################################################################################################


votingData = VotingData(
    "data/exampleData.csv",
    "YEAR",
    "VOTINGS",
    "PARTY_SHORT",
    "PARTY_SPEC",
    "PARTY_COLOR",
    120,
)

votingData.createOnePager(2021)

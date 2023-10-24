from votingGraphPortfolio import VotingGraphs

votingGraphs = VotingGraphs(
    "data/exampleData.csv",
    "YEAR",
    "VOTINGS",
    "PARTY_SHORT",
    "PARTY_SPEC",
    "PARTY_COLOR",
)
votingGraphs.getGraph(2021, type="BAR_DIFFERENCE")
# votingData.getGraph(2021, "BAR_DIFFERENCE", "output/barDifference.png",
#                    title="Wahlergebnis 2021", subtitle="Prozentpunkte im Vergleich zur letzten Wahl")
# votingData.getGraph(2021, "PARLIAMENT", "output/pieParliament.png",
#                    title="Wahlergebnis 2021", subtitle="Anzahl Sitze im Parlament")
# votingData.getGraph(2021, "COALITIONS", "output/barCoalition.png",
#                    title="Wahlergebnis 2021", subtitle="Anzahl Sitze für mögliche Koalitionen")


votingGraphs.createOnePager()

from electionResultGraphs import ElectionResultGraphs

# example for instantiating the class
electionResultGraphs = ElectionResultGraphs(
    "data/exampleData.csv",
    "YEAR",
    "VOTINGS",
    "PARTY_SHORT",
    "PARTY_SPEC",
    "PARTY_COLOR",
)

# example for creating a graph
electionResultGraphs.getGraph(2021, type="BAR_DIFFERENCE")

# example for creating a one pager
electionResultGraphs.createOnePager()

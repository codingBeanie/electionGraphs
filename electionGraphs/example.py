from electionGraphs import ElectionGraphs

# example for instantiating the class
electionGraphs = ElectionGraphs(
    "data/exampleData.csv",
    "YEAR",
    "VOTINGS",
    "PARTY_SHORT",
    "PARTY_SPEC",
    "PARTY_COLOR",
)

# example for creating a graph
electionGraphs.getGraph(2021, type="BAR_DIFFERENCE")

# example for creating a one pager
electionGraphs.createOnePager()

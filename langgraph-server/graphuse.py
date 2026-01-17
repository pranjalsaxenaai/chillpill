from graph import graph
from contracts.states import StoryState

out = graph.invoke(StoryState(input_idea="A racer is competing in a high-speed race, to avenge his brother's death in a tragic accident.",
                              db_metadata={"project_id": "681796fabbb5d812dc05649e"}))
print(out)
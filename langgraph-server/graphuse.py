from graph import graph
from contracts.states import StoryState

out = graph.invoke(StoryState(input_idea="A racer is competing in a high-speed race, to avenge his brother's death in a tragic accident."))
print(out)
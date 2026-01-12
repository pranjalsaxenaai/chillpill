from graph import graph
from contracts import StoryState

out = graph.invoke(StoryState(input_idea="A bird is flying in the sky"))
print(out)
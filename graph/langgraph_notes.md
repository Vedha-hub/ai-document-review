# LangGraph Concepts - Week 2 Notes

## 1. State
A Python TypedDict passed between all nodes containing all data 
the workflow needs (input, draft, feedback, iteration count etc.)

## 2. Nodes
Plain Python functions that receive State and return updated State.
Each node does one job (write, review, finalize).

## 3. Edges
Connections between nodes that define the flow direction.
writer → critic → finalize

## 4. Conditional Edges
Choose the next node at runtime based on state values.
If score >= 75 → finalize, else → writer (revise)

## 5. StateGraph + compile()
The object used to build the graph by adding nodes and edges.
.compile() turns it into a runnable executable graph.
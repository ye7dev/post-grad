# Dijkstra vs. Floyd-Warshall

Status: algorithm
Theme: graph
Created time: February 8, 2024 8:21 PM
Last edited time: February 8, 2024 8:21 PM

Floyd-Warshall and running Dijkstra's algorithm from every node are both methods to find the shortest paths in a graph, but they differ significantly in their approach, complexity, and types of problems they are best suited for. Here's a comparison:

### Floyd-Warshall Algorithm

- **Approach**: A dynamic programming algorithm that calculates the shortest paths between all pairs of vertices in a graph. It systematically considers each vertex as an intermediate point in paths among all pairs of vertices.
- **Complexity**: \(O(V^3)\), where \(V\) is the number of vertices in the graph.
- **Graph Type**: Works on both directed and undirected graphs. Can handle negative weights but not negative cycles.
- **Use Cases**: Best used when you need the shortest paths between all pairs of vertices in a graph, especially for dense graphs or when both positive and negative edge weights are present.

### Dijkstra's Algorithm (for all nodes)

- **Approach**: An algorithm that finds the shortest paths from a single source vertex to all other vertices in the graph. Running Dijkstra's algorithm from every node means executing it \(V\) times, each time considering a different vertex as the source.
- **Complexity**: The complexity depends on the implementation. Using a min-priority queue implemented with a binary heap, the complexity is \(O(V^2 + VE \log V)\) when run from every vertex, where \(E\) is the number of edges. For sparse graphs, this can be more efficient than Floyd-Warshall.
- **Graph Type**: Works on graphs without negative weight edges. It can be used on both directed and undirected graphs.
- **Use Cases**: Best used when you have sparse graphs or when negative weight edges are not present. It's also useful when you only need the shortest path from a single source to all other vertices, though it can be adapted for all pairs by running it from each vertex as the source.

### Key Differences

- **Efficiency for Sparse vs. Dense Graphs**: Dijkstra's algorithm (when run from each vertex) can be more efficient than Floyd-Warshall for sparse graphs, especially if an efficient priority queue is used. Floyd-Warshall is generally more straightforward and potentially more efficient for dense graphs or when negative weights are involved.
- **Handling Negative Weights**: Floyd-Warshall can handle negative weights naturally and can also detect negative cycles. Dijkstra's algorithm, in its standard form, does not work with negative weight edges because it can lead to incorrect results.
- **Implementation Complexity**: Implementing Floyd-Warshall is typically simpler and more straightforward than implementing Dijkstra's algorithm multiple times, especially when considering the management of priority queues.

In summary, while both approaches can solve the all-pairs shortest path problem, the choice between Floyd-Warshall and running Dijkstra's algorithm from every node depends on the specific characteristics of the graph and the requirements of the problem at hand.
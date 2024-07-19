# Bellman-Ford negative cycle check

Status: algorithm
Theme: graph
Created time: February 7, 2024 6:12 PM
Last edited time: February 7, 2024 6:13 PM

The specific part of the Bellman-Ford algorithm you're referring to is crucial for detecting negative weight cycles in a graph. Here's why this part indicates the presence of a cycle and, in the context of the given problem, an arbitrage opportunity:

### Understanding Negative Weight Cycles

A negative weight cycle in a graph is a cycle (a path that starts and ends at the same vertex) for which the sum of the edge weights in the cycle is negative. If such a cycle exists, it means you can reduce the total path weight each time you traverse the cycle, theoretically reducing the path weight indefinitely.

### How Bellman-Ford Detects Negative Cycles

The Bellman-Ford algorithm operates under the principle that the shortest path between any two vertices in a graph without a negative weight cycle will have at most \(V-1\) edges, where \(V\) is the number of vertices. Therefore, it iteratively relaxes all edges \(V-1\) times to find the shortest paths.

- **Relaxation**: An edge relaxation checks if the current known distance to a vertex \(to\_currency\) can be reduced by taking an edge \((from\_currency, to\_currency)\). If so, it updates the distance to \(to\_currency\) to reflect this shorter path.
- **After \(V-1\) Iterations**: By this time, all shortest paths (if no negative weight cycle is present) should have been found. The shortest path property ensures that no further updates to the shortest paths should be possible.

### Checking for Cycles

- **The Check**: The part of the code you're referring to performs one more iteration over all edges to check if any distance can still be reduced. If an edge \((from\_currency, to\_currency)\) can further reduce the distance to \(to\_currency\) beyond the \(V-1\) relaxations, it implies that there is a cycle that allows for an even shorter path than any path of \(V-1\) edges or fewer. This can only occur if there is a negative weight cycle in the graph.
- **Implication in Arbitrage Detection**: In the context of currency exchange, a negative weight cycle means you can start with a certain amount of money, perform a series of exchanges (following the cycle), and end up with more money than you started with, hence detecting an arbitrage opportunity.

### Conclusion

This segment of the Bellman-Ford algorithm is a direct method for detecting negative weight cycles, leveraging the insight that if a path's weight can be further reduced after \(V-1\) edge relaxations, a negative cycle must exist because paths that traverse a negative cycle can always be made shorter by going around the cycle again. In financial applications like currency exchange, this translates to the possibility of arbitrage, exploiting the cycle to gain profit with each iteration.
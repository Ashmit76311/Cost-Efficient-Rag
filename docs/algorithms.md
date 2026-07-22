# Algorithms

An algorithm is a step-by-step procedure for solving a problem or performing a computation. Algorithm analysis focuses on time complexity (how runtime scales with input size) and space complexity (how memory usage scales).

## Sorting Algorithms

Sorting is one of the most studied problems in computer science.

**Bubble Sort** repeatedly swaps adjacent elements if they are in the wrong order. Time complexity is O(n^2) in the worst and average case, O(n) in the best case (already sorted). It is simple but inefficient for large datasets.

**Merge Sort** uses divide-and-conquer. It splits the array in half, recursively sorts each half, and merges the sorted halves. Time complexity is O(n log n) in all cases. It requires O(n) extra space for the merge step. Merge sort is stable, meaning equal elements maintain their relative order.

**Quick Sort** picks a pivot element, partitions the array around it, and recursively sorts the partitions. Average time complexity is O(n log n), but worst case is O(n^2) when the pivot is consistently the smallest or largest element. Randomized pivot selection or median-of-three helps avoid this. Quick sort is in-place (O(log n) stack space) and typically faster than merge sort in practice due to cache efficiency.

**Heap Sort** builds a max-heap and repeatedly extracts the maximum. Time complexity is O(n log n) in all cases with O(1) extra space. However, it has poor cache performance compared to quick sort.

## Searching Algorithms

**Linear Search** scans each element sequentially. O(n) time, works on unsorted data.

**Binary Search** requires sorted data. It repeatedly halves the search space by comparing the target with the middle element. Time complexity is O(log n). Binary search can be applied beyond arrays — it works on any monotonic function (binary search on the answer).

## Graph Algorithms

**Breadth-First Search (BFS)** explores nodes level by level using a queue. Time complexity is O(V + E). BFS finds the shortest path in unweighted graphs and is used for level-order traversal of trees.

**Depth-First Search (DFS)** explores as deep as possible along each branch before backtracking, using a stack (or recursion). Time complexity is O(V + E). DFS is used for cycle detection, topological sorting, and finding connected components.

**Dijkstra's Algorithm** finds the shortest path from a source to all other vertices in a weighted graph with non-negative edge weights. It uses a priority queue (min-heap) and has time complexity O((V + E) log V). It does not work with negative weights — for that, use Bellman-Ford which runs in O(VE).

## Dynamic Programming

Dynamic programming (DP) solves problems by breaking them into overlapping subproblems and storing their solutions to avoid recomputation. There are two approaches: top-down (memoization, using recursion with caching) and bottom-up (tabulation, building solutions from smaller subproblems iteratively).

Classic DP problems include the Fibonacci sequence, longest common subsequence, knapsack problem, edit distance, and coin change. The key to identifying a DP problem is finding optimal substructure (optimal solution contains optimal solutions to subproblems) and overlapping subproblems.

## Greedy Algorithms

Greedy algorithms make the locally optimal choice at each step. They don't always produce globally optimal solutions, but they do for problems with the greedy-choice property. Examples include Huffman coding, activity selection, and Kruskal's minimum spanning tree algorithm. Greedy algorithms are typically faster than DP since they don't explore all possibilities.

## Time Complexity Classes

- O(1): Constant — hash table lookup
- O(log n): Logarithmic — binary search
- O(n): Linear — linear search
- O(n log n): Linearithmic — merge sort, quick sort (average)
- O(n^2): Quadratic — bubble sort, insertion sort
- O(2^n): Exponential — brute force subset enumeration
- O(n!): Factorial — brute force permutations

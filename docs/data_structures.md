# Data Structures

Data structures are fundamental building blocks in computer science used to organize, store, and manage data efficiently. Choosing the right data structure can dramatically affect the performance of an algorithm.

## Arrays and Dynamic Arrays

An array is a contiguous block of memory that stores elements of the same type. Access by index is O(1), but insertion and deletion in the middle require shifting elements, making them O(n). Dynamic arrays (like Python lists or Java ArrayLists) automatically resize when they run out of space, typically doubling their capacity. This gives amortized O(1) append but O(n) worst-case for a single append that triggers resizing.

## Linked Lists

A linked list consists of nodes where each node contains data and a reference (pointer) to the next node. Singly linked lists have one pointer per node; doubly linked lists have pointers to both the next and previous nodes. Insertion and deletion at a known position are O(1), but searching requires traversing the list in O(n) time. Linked lists use more memory per element than arrays due to pointer storage overhead.

## Stacks and Queues

A stack follows Last-In-First-Out (LIFO) ordering. Push and pop operations are both O(1). Stacks are used in function call management (the call stack), expression evaluation, backtracking algorithms, and undo mechanisms. A queue follows First-In-First-Out (FIFO) ordering. Enqueue and dequeue are O(1) with proper implementation. Queues are used in BFS, task scheduling, and buffering.

## Hash Maps (Hash Tables)

Hash maps store key-value pairs and provide average O(1) lookup, insertion, and deletion. They work by computing a hash function on the key to determine the storage index. Collisions occur when two keys hash to the same index. Common collision resolution strategies include chaining (storing a linked list at each bucket) and open addressing (probing for the next empty slot using linear probing, quadratic probing, or double hashing). The load factor (number of elements / number of buckets) affects performance. Most implementations resize when the load factor exceeds a threshold (typically 0.75).

## Trees

A tree is a hierarchical data structure with a root node and child nodes forming a parent-child relationship. A Binary Search Tree (BST) maintains the invariant that left children are smaller and right children are larger than the parent. Basic BST operations (search, insert, delete) are O(h) where h is the tree height. In the worst case (degenerate/skewed tree), h = n, making operations O(n). Balanced BSTs like AVL trees and Red-Black trees guarantee O(log n) height through rotations.

## Heaps

A heap is a complete binary tree satisfying the heap property: in a min-heap, each parent is smaller than its children; in a max-heap, each parent is larger. Heaps are commonly implemented as arrays. Insert and delete operations are O(log n). Heaps are the backbone of priority queues and are used in Dijkstra's algorithm and heap sort. Building a heap from an unsorted array can be done in O(n) time using the heapify procedure.

## Graphs

A graph consists of vertices (nodes) and edges connecting them. Graphs can be directed or undirected, weighted or unweighted. Common representations include adjacency matrices (O(V^2) space, O(1) edge lookup) and adjacency lists (O(V+E) space, O(degree) edge lookup). Adjacency lists are preferred for sparse graphs, which are common in practice. Graph algorithms include BFS, DFS, Dijkstra's shortest path, and minimum spanning tree algorithms like Kruskal's and Prim's.

## Tries

A trie (prefix tree) is a tree-like structure where each node represents a character. Tries are used for efficient string operations like prefix search, autocomplete, and spell checking. Search and insert operations take O(m) time where m is the length of the string, regardless of how many strings are stored. The trade-off is higher memory usage compared to hash maps for string storage.

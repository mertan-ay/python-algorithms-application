# Python-algorithms-application
# Algorithmic Problem Solvers in Python

This repository contains two algorithmic programming projects implemented in Python.
Both projects were developed as part of the course Project Programmeren in the HBO Bachelor's programme Applied Mathematics at NHL Stenden University of Applied Sciences.


# 1. Block Puzzle Solver (Backtracking)

## Description

This project implements a solver for a block puzzle inspired by the classic pentomino problem.

The objective of the puzzle is to fill an 8×8 board using 8 uniquely shaped pieces. Each piece can appear in multiple orientations. The solver uses a recursive backtracking approach to systematically try all valid placements.

Whenever a piece does not fit, the algorithm backtracks and tries a different configuration. This continues until either a full board is constructed or all possibilities are exhausted.

A key requirement of the assignment was that rotationally or mirror-equivalent solutions should not be counted multiple times. The implementation ensures that only unique solutions are generated. The correct solver produces exactly 6 unique solutions.

The board is represented as a 1D list with padded borders to simplify bounds checking.

## Algorithmic Approach

- Constraint Satisfaction Problem (CSP)
- Recursive backtracking
- State mutation and rollback
- Search tree traversal

## Run

```
python blokjespuzzel_solver.py
```


# 2. Traveling Salesman Problem (Brute Force)
## Description

This project implements a brute-force solution to the symmetric Traveling Salesman Problem (TSP).

Given a set of cities and randomly generated distances between them, the goal is to determine the shortest possible round trip that starts and ends at city 0 while visiting every other city exactly once.

The implementation generates all permutations of the cities and computes the length of each possible tour. The shortest tour found is returned as the optimal solution.

In addition to solving the problem, I also measured the runtime for increasing values of n to study the growth in computational complexity.

## Algorithmic Approach

Lexicographic permutation generation

Exhaustive search

Evaluation of objective function

Empirical runtime measurement

A custom in-place next-permutation algorithm is implemented instead of relying on built-in libraries.

## Run
```
python tsp_bruteforce.py
```




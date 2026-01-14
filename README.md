# AI Pathfinding Simulation Using A* and Uniform Cost Search (UCS)

A grid-based pathfinding simulation built with **Python** and **Pygame** to compare two classical AI search algorithms:

- **A\*** Search (informed search using Manhattan distance heuristic)
- **Uniform Cost Search (UCS)** (uninformed search; equivalent to Dijkstra for uniform step cost)

The simulation displays:
- Grid world
- Random **tasks** (red cells with numbers)
- Random **barriers/obstacles** (black cells)
- An agent that moves to complete tasks using the selected algorithm
- Task-wise and total path cost statistics

---

## Project Structure

```text
.
├── run.py
├── agent1.py
├── agent2.py
├── environment.py
└── README.md

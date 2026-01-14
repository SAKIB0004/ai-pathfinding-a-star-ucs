# AI Pathfinding Simulation Using A* and Uniform Cost Search (UCS)

A grid-based pathfinding simulation built using **Python** and **Pygame** to compare two classical Artificial Intelligence search algorithms:

- **A\*** Search (informed search using Manhattan distance heuristic)
- **Uniform Cost Search (UCS)** (uninformed search; equivalent to Dijkstra’s algorithm for uniform step costs)

The simulation visualizes how an agent navigates a grid with obstacles to complete multiple tasks while minimizing total path cost.

---

## Features

- **Search Algorithms**: Implementations of **A\*** Search and **Uniform Cost Search (UCS)** for optimal pathfinding.
- **Agent Movement Simulation**: Visualizes an agent moving step-by-step in a grid environment while completing tasks.
- **Obstacle Handling**: Randomly generated barriers/obstacles that the agent must avoid.
- **User-Friendly Interface**: Interactive graphical simulation built with **Pygame**.
- **Modular Design**: Separate files for agents, environment, and runner script for easy extension.

---

## Installation

### Prerequisites

- **Python 3.9 or higher** (Python 3.10 recommended)
- **Pygame**

> ⚠️ Python 3.13 may cause installation issues with `pygame` on some systems.

### Steps

1. **Clone the Repository**

   ```bash
   https://github.com/SAKIB0004/ai-pathfinding-a-star-ucs.git
   cd ai-pathfinding-a-star-ucs
2. **Install Dependencies**

   Install the required Python packages using **pip**:
   ```
   python -m pip install pygame
   ```

## Project Structure

```text
/
│
├── run.py
├── agent1.py
├── agent2.py
├── environment.py
├── README.md

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
   git clone https://github.com/your_username/ai-pathfinding-a-star-ucs.git
   cd ai-pathfinding-a-star-ucs
2. **Install Dependencies**

   Install the required Python packages using **pip**:
   ```
   python -m pip install pygame
   ```

### Directory Structure

ai-pathfinding-a-star-ucs/
│
├── run.py              # Main simulation script
├── agent1.py           # A* Search agent
├── agent2.py           # Uniform Cost Search (UCS) agent
├── environment.py      # Grid environment, tasks, and barriers
├── README.md           # Project documentation

import pygame
import heapq


class Agent2(pygame.sprite.Sprite):
    def __init__(self, environment, grid_size):
        super().__init__()
        self.image = pygame.Surface((grid_size, grid_size))
        self.image.fill((0, 0, 255))  # Agent color is blue
        self.rect = self.image.get_rect()

        self.grid_size = grid_size
        self.environment = environment

        self.position = [0, 0]
        self.rect.topleft = (0, 0)

        self.task_completed = 0
        self.completed_tasks = []

        self.path = []
        self.moving = False

        # Tracking
        self.total_path_cost = 0
        self.completed_tasks_with_costs = []

        # For the currently planned task
        self.current_task_cost = 0

    def move(self):
        """Move the agent along the path."""
        if self.path:
            next_position = self.path.pop(0)
            self.position = list(next_position)
            self.rect.topleft = (self.position[0] * self.grid_size, self.position[1] * self.grid_size)
            self.check_task_completion()
        else:
            self.moving = False

    def check_task_completion(self):
        """Check if the agent has reached a task location."""
        pos = tuple(self.position)
        if pos in self.environment.task_locations:
            task_number = self.environment.task_locations.pop(pos)
            self.task_completed += 1
            self.completed_tasks.append(task_number)

            # Correct: use the UCS cost computed when planning this task
            path_cost = self.current_task_cost
            self.completed_tasks_with_costs.append((task_number, path_cost))
            self.total_path_cost += path_cost

            # Reset task cost after completion (optional but safer)
            self.current_task_cost = 0

    def find_nearest_task(self):
        """
        Find the task with the lowest UCS cost from the current position.
        (Uniform step cost = 1 per move)
        """
        best_task = None
        best_path = None
        best_cost = float("inf")

        for task_position in self.environment.task_locations.keys():
            path, cost = self.find_path_to(task_position)
            if path and cost < best_cost:
                best_cost = cost
                best_path = path
                best_task = task_position

        if best_path:
            self.path = best_path[1:]  # exclude current position
            self.current_task_cost = best_cost
            self.moving = True

    def find_path_to(self, target):
        """
        Correct UCS (Dijkstra with uniform costs):
        - priority queue ordered by path cost g
        - keep best known cost per node (not just visited set)
        Returns: (path, cost)
        """
        start = tuple(self.position)
        goal = target

        pq = [(0, start)]  # (cost, node)
        came_from = {start: None}
        best_cost = {start: 0}

        while pq:
            cost, current = heapq.heappop(pq)

            # Skip stale entries (common UCS/Dijkstra optimization)
            if cost != best_cost.get(current, float("inf")):
                continue

            if current == goal:
                # Reconstruct path
                path = []
                node = current
                while node is not None:
                    path.append(node)
                    node = came_from[node]
                path.reverse()
                return path, cost

            for neighbor in self.get_neighbors(*current):
                new_cost = cost + 1  # uniform step cost

                if new_cost < best_cost.get(neighbor, float("inf")):
                    best_cost[neighbor] = new_cost
                    came_from[neighbor] = current
                    heapq.heappush(pq, (new_cost, neighbor))

        return None, float("inf")

    def get_neighbors(self, x, y):
        """Get walkable neighboring positions."""
        neighbors = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.environment.is_within_bounds(nx, ny) and not self.environment.is_barrier(nx, ny):
                neighbors.append((nx, ny))
        return neighbors

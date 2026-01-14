import pygame
import heapq


class Agent1(pygame.sprite.Sprite):
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

        # For current task
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
        position_tuple = tuple(self.position)
        if position_tuple in self.environment.task_locations:
            task_number = self.environment.task_locations.pop(position_tuple)
            self.task_completed += 1
            self.completed_tasks.append(task_number)

            # TRUE path cost for the just-finished task
            path_cost = self.current_task_cost
            self.completed_tasks_with_costs.append((task_number, path_cost))
            self.total_path_cost += path_cost

    def find_nearest_task(self):
        """
        Choose the task with the lowest A* path cost from current position.
        (This is a fair comparison to your UCS agent.)
        """
        nearest_task = None
        best_path = None
        best_cost = float("inf")

        for task_position in self.environment.task_locations.keys():
            path, cost = self.find_path_to(task_position)
            if path and cost < best_cost:
                best_cost = cost
                best_path = path
                nearest_task = task_position

        if best_path:
            self.path = best_path[1:]  # exclude current position
            self.current_task_cost = best_cost
            self.moving = True

    def find_path_to(self, target):
        """
        Correct A*:
        - priority queue ordered by f = g + h
        - g = actual cost so far (here each step costs 1)
        - h = Manhattan distance to goal
        Returns: (path as list of (x,y), cost)
        """
        start = tuple(self.position)
        goal = target

        def h(a, b):
            (x1, y1) = a
            (x2, y2) = b
            return abs(x1 - x2) + abs(y1 - y2)

        open_heap = []
        heapq.heappush(open_heap, (h(start, goal), 0, start))  # (f, g, node)

        came_from = {}
        g_score = {start: 0}
        closed = set()

        while open_heap:
            f, g, current = heapq.heappop(open_heap)

            if current in closed:
                continue
            closed.add(current)

            if current == goal:
                # Reconstruct path
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path, g_score[goal]

            for neighbor in self.get_neighbors(*current):
                tentative_g = g_score[current] + 1  # uniform step cost

                # If we've found a better path to neighbor, record it
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + h(neighbor, goal)
                    heapq.heappush(open_heap, (f_score, tentative_g, neighbor))

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

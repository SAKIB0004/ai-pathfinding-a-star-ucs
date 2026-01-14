# environment.py
import random


class Environment:
    def __init__(self, width, height, grid_size, num_tasks, num_barriers, seed=None):
        self.width = width
        self.height = height
        self.grid_size = grid_size

        self.columns = width // grid_size
        self.rows = height // grid_size
        self.total_cells = self.columns * self.rows

        # Optional reproducibility
        self._rng = random.Random(seed)

        # Validate counts early
        if num_tasks < 0 or num_barriers < 0:
            raise ValueError("num_tasks and num_barriers must be >= 0")
        if num_tasks + num_barriers > self.total_cells:
            raise ValueError(
                f"Too many items for the grid: tasks({num_tasks}) + barriers({num_barriers}) "
                f"> total cells({self.total_cells})."
            )

        self.task_locations = self.generate_tasks(num_tasks)
        self.barrier_locations = self.generate_random_locations(
            num_barriers, exclude=set(self.task_locations.keys())
        )

    # ---------- Generation ----------

    def generate_tasks(self, count):
        """Generate unique task locations with task numbers 1..count."""
        tasks = {}
        used = set()

        for task_number in range(1, count + 1):
            location = self._pick_free_cell(exclude=used)
            tasks[location] = task_number
            used.add(location)

        return tasks

    def generate_random_locations(self, count, exclude=None):
        """Generate `count` unique random locations not in exclude."""
        if exclude is None:
            exclude = set()

        locations = set()
        for _ in range(count):
            loc = self._pick_free_cell(exclude=exclude | locations)
            locations.add(loc)

        return locations

    def _pick_free_cell(self, exclude):
        """Pick a random free cell not in exclude."""
        # Efficient when grid is not too full; validated counts prevent infinite loop.
        while True:
            location = (self._rng.randint(0, self.columns - 1), self._rng.randint(0, self.rows - 1))
            if location not in exclude:
                return location

    # ---------- Queries ----------

    def is_within_bounds(self, x, y):
        return 0 <= x < self.columns and 0 <= y < self.rows

    def is_barrier(self, x, y):
        return (x, y) in self.barrier_locations

    def get_task_number(self, x, y):
        """Return task number if a task exists at (x, y), else None."""
        return self.task_locations.get((x, y))

    # ---------- Mutations / encapsulation ----------

    def complete_task(self, x, y):
        """Remove and return the task number at (x, y), or None if no task."""
        return self.task_locations.pop((x, y), None)

    def reset(self, task_locations, barrier_locations):
        """Restore environment from saved data (deepcopy should be done by caller)."""
        self.task_locations = task_locations
        self.barrier_locations = barrier_locations

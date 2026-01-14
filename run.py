import pygame
import sys
import copy
from agent1 import Agent1
from agent2 import Agent2
from environment import Environment

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
GRID_SIZE = 40
STATUS_WIDTH = 600

BACKGROUND_COLOR = (255, 255, 255)
BARRIER_COLOR = (0, 0, 0)
TASK_COLOR = (255, 0, 0)
TEXT_COLOR = (0, 0, 0)

BUTTON_COLOR = (0, 200, 0)
BUTTON_HOVER_COLOR = (0, 255, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)

MOVEMENT_DELAY = 100  # ms between moves


def reset_simulation(agent, environment, original_environment_data):
    """Reset ANY agent + restore environment to original state."""
    # Reset agent core state
    agent.position = [0, 0]
    agent.rect.topleft = (0, 0)
    agent.task_completed = 0
    agent.completed_tasks = []
    agent.completed_tasks_with_costs = []
    agent.total_path_cost = 0
    agent.path = []
    agent.moving = False

    # Optional fields (Agent1/Agent2 may have these)
    if hasattr(agent, "current_task_cost"):
        agent.current_task_cost = 0
    if hasattr(agent, "total_heuristic"):
        agent.total_heuristic = 0

    # Restore environment
    environment.task_locations = copy.deepcopy(original_environment_data["task_locations"])
    environment.barrier_locations = copy.deepcopy(original_environment_data["barrier_locations"])


def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH + STATUS_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pygame AI Grid Simulation")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # Environment + agents
    environment = Environment(WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, num_tasks=5, num_barriers=15)
    agent1 = Agent1(environment, GRID_SIZE)
    agent2 = Agent2(environment, GRID_SIZE)

    # Backup environment
    original_environment_data = {
        "task_locations": copy.deepcopy(environment.task_locations),
        "barrier_locations": copy.deepcopy(environment.barrier_locations),
    }

    # We only draw the currently active agent
    active_sprites = pygame.sprite.Group()

    # Buttons (fixed position)
    button_width, button_height = 180, 50
    button_x = WINDOW_WIDTH + (STATUS_WIDTH - button_width) // 2
    button1_y = 420
    button2_y = button1_y + button_height + 20

    button1_rect = pygame.Rect(button_x, button1_y, button_width, button_height)
    button2_rect = pygame.Rect(button_x, button2_y, button_width, button_height)

    # Simulation
    active_agent = None
    simulation_started = {"Agent1": False, "Agent2": False}
    last_move_time = pygame.time.get_ticks()

    running = True
    while running:
        clock.tick(60)

        mouse_pos = pygame.mouse.get_pos()

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1_rect.collidepoint(event.pos):
                    reset_simulation(agent1, environment, original_environment_data)
                    simulation_started["Agent1"] = True
                    simulation_started["Agent2"] = False

                    active_agent = agent1
                    active_sprites.empty()
                    active_sprites.add(agent1)

                    if environment.task_locations:
                        agent1.find_nearest_task()

                if button2_rect.collidepoint(event.pos):
                    reset_simulation(agent2, environment, original_environment_data)
                    simulation_started["Agent1"] = False
                    simulation_started["Agent2"] = True

                    active_agent = agent2
                    active_sprites.empty()
                    active_sprites.add(agent2)

                    if environment.task_locations:
                        agent2.find_nearest_task()

        # --- Update (movement with delay) ---
        current_time = pygame.time.get_ticks()
        if active_agent:
            active_key = "Agent1" if active_agent == agent1 else "Agent2"
            if simulation_started[active_key] and (current_time - last_move_time > MOVEMENT_DELAY):
                if not active_agent.moving and environment.task_locations:
                    active_agent.find_nearest_task()
                elif active_agent.moving:
                    active_agent.move()
                last_move_time = current_time

        # --- Draw ---
        screen.fill(BACKGROUND_COLOR)

        # Grid
        for x in range(environment.columns):
            for y in range(environment.rows):
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)

        # Barriers
        for (bx, by) in environment.barrier_locations:
            barrier_rect = pygame.Rect(bx * GRID_SIZE, by * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, BARRIER_COLOR, barrier_rect)

        # Tasks
        for (tx, ty), task_number in environment.task_locations.items():
            task_rect = pygame.Rect(tx * GRID_SIZE, ty * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, TASK_COLOR, task_rect)
            num_surface = font.render(str(task_number), True, (255, 255, 255))
            num_rect = num_surface.get_rect(center=task_rect.center)
            screen.blit(num_surface, num_rect)

        # Draw only active agent
        active_sprites.draw(screen)

        # Status separator
        pygame.draw.line(screen, (0, 0, 0), (WINDOW_WIDTH, 0), (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Status text (both agents info)
        status_x = WINDOW_WIDTH + 10
        y = 20
        line_h = 26

        for name, agent in [("Agent1", agent1), ("Agent2", agent2)]:
            algo = "A* Search" if name == "Agent1" else "UCS"
            screen.blit(font.render(f"{name} - Algorithm: {algo}", True, TEXT_COLOR), (status_x, y))
            y += line_h

            screen.blit(font.render(f"Tasks Completed: {agent.task_completed}", True, TEXT_COLOR), (status_x, y))
            y += line_h

            screen.blit(font.render(f"Position: {agent.position}", True, TEXT_COLOR), (status_x, y))
            y += line_h

            completed = ", ".join([f"{t} (Cost: {c})" for t, c in agent.completed_tasks_with_costs]) or "None"
            screen.blit(font.render(f"Completed Tasks: {completed}", True, TEXT_COLOR), (status_x, y))
            y += line_h

            screen.blit(font.render(f"Total Path Cost: {agent.total_path_cost}", True, TEXT_COLOR), (status_x, y))
            y += line_h + 16

        # Buttons
        b1_color = BUTTON_HOVER_COLOR if button1_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, b1_color, button1_rect)
        screen.blit(font.render("Run A* (Agent1)", True, BUTTON_TEXT_COLOR),
                    font.render("Run A* (Agent1)", True, BUTTON_TEXT_COLOR).get_rect(center=button1_rect.center))

        b2_color = BUTTON_HOVER_COLOR if button2_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, b2_color, button2_rect)
        screen.blit(font.render("Run UCS (Agent2)", True, BUTTON_TEXT_COLOR),
                    font.render("Run UCS (Agent2)", True, BUTTON_TEXT_COLOR).get_rect(center=button2_rect.center))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

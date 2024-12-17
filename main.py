import random
from collections import deque

# Game Configuration
GRID_SIZE = 5
NUM_TREASURES = 3
NUM_LOCKED_TREASURES = 1
NUM_TRAPS = 3
NUM_POWERUPS = 2
NUM_KEYS = 1
INITIAL_HEALTH = 10

# Function to Create the Game Grid
def create_grid():
    """Creates a 5x5 grid with treasures, locked treasures, traps, power-ups, and keys."""
    grid = [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    place_items(grid, "T", NUM_TREASURES)          # Place treasures
    place_items(grid, "L", NUM_LOCKED_TREASURES)  # Place locked treasures
    place_items(grid, "X", NUM_TRAPS)             # Place traps
    place_items(grid, "U", NUM_POWERUPS)          # Place health power-ups
    place_items(grid, "K", NUM_KEYS)              # Place keys
    return grid

def place_items(grid, item, count):
    """Randomly places items on the grid."""
    while count > 0:
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        if grid[x][y] == " ":
            grid[x][y] = item
            count -= 1

# Search Algorithms
def bfs_search(grid, start, target):
    """Breadth-First Search to find the shortest path to a target."""
    queue = deque([start])
    visited = set()
    while queue:
        x, y = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if grid[x][y] == target:
            return (x, y)  # Return the position of the target
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                queue.append((nx, ny))
    return None  # Target not found

def dfs_search(grid, start, target):
    """Depth-First Search to find a target."""
    stack = [start]
    visited = set()
    while stack:
        x, y = stack.pop()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if grid[x][y] == target:
            return (x, y)  # Return the position of the target
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                stack.append((nx, ny))
    return None  # Target not found

def binary_search(grid, target_row, target):
    """Binary Search to find a target in a specific row."""
    low, high = 0, GRID_SIZE - 1
    while low <= high:
        mid = (low + high) // 2
        if grid[target_row][mid] == target:
            return (target_row, mid)
        elif grid[target_row][mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return None  # Target not found

# Player Class
class Player:
    """Represents a player in the game."""
    def __init__(self, name):
        self.name = name
        self.health = INITIAL_HEALTH
        self.score = 0
        self.position = (0, 0)  # Start at top-left corner
        self.keys = 0  # Number of keys the player has

    def move(self, direction):
        """Moves the player in the specified direction."""
        x, y = self.position
        if direction == "up" and x > 0:
            self.position = (x-1, y)
        elif direction == "down" and x < GRID_SIZE-1:
            self.position = (x+1, y)
        elif direction == "left" and y > 0:
            self.position = (x, y-1)
        elif direction == "right" and y < GRID_SIZE-1:
            self.position = (x, y+1)
        else:
            print("Invalid move. You hit the boundary!")

# Display Functions
def display_grid(grid, player_positions):
    """Displays the grid with hidden items and player positions."""
    print("\nGrid:")
    for x in range(GRID_SIZE):
        row = ""
        for y in range(GRID_SIZE):
            if (x, y) in player_positions:
                row += "P "  # Show player position
            elif grid[x][y] == " ":
                row += "? "  # Hidden items
            else:
                row += f"{grid[x][y]} "
        print(row)
    print()

# Main Game Logic
def play_game():
    """Main function to play the treasure hunt game."""
    # Display Instructions
    print("Welcome to the Treasure Hunt Game!")
    print("Instructions:")
    print("- Move using commands: 'up', 'down', 'left', or 'right'.")
    print("- Use search commands: 'search bfs', 'search dfs', or 'search bs'.")
    print("- Find treasures (T), avoid traps (X), and collect power-ups (U) and keys (K)!")
    print("- Locked treasures (L) need keys to unlock.")
    print("- Your position is marked as 'P' on the grid. Hidden cells are shown as '?'.")
    print("- Good luck and enjoy the game!\n")

    grid = create_grid()  # Create the game grid
    players = [Player("Player 1"), Player("Player 2")]  # Initialize players
    turn = 0

    while True:
        current_player = players[turn % len(players)]
        print(f"\n{current_player.name}'s turn")
        print(f"Health: {current_player.health}, Score: {current_player.score}, Keys: {current_player.keys}")
        print(f"Position: {current_player.position}")

        # Update and display the grid
        player_positions = [player.position for player in players]
        display_grid(grid, player_positions)

        # Player action
        action = input("Choose action: move (up/down/left/right) or search (bfs/dfs/bs): ").lower()

        if action in ["up", "down", "left", "right"]:
            current_player.move(action)
            x, y = current_player.position
            cell = grid[x][y]

            if cell == "T":
                print("You found a treasure!")
                current_player.score += 1
                grid[x][y] = " "
            elif cell == "L":
                if current_player.keys > 0:
                    print("You unlocked a locked treasure! Bonus points!")
                    current_player.score += 2
                    current_player.keys -= 1
                    grid[x][y] = " "
                else:
                    print("You need a key to unlock this treasure.")
            elif cell == "X":
                print("You hit a trap!")
                current_player.health -= 1
                grid[x][y] = " "
            elif cell == "U":
                print("You collected a power-up!")
                current_player.health += 1
                grid[x][y] = " "
            elif cell == "K":
                print("You found a key!")
                current_player.keys += 1
                grid[x][y] = " "
            else:
                print("Nothing here.")

        elif action.startswith("search"):
            if "bfs" in action:
                target = input("Enter the target item to search (T, L, X, U, K): ").strip().upper()
                result = bfs_search(grid, current_player.position, target)
                print(f"BFS Search result: {result}")
            elif "dfs" in action:
                target = input("Enter the target item to search (T, L, X, U, K): ").strip().upper()
                result = dfs_search(grid, current_player.position, target)
                print(f"DFS Search result: {result}")
            elif "bs" in action:
                target = input("Enter the target item to search in a row (T, L, X, U, K): ").strip().upper()
                row = int(input("Enter the row to search (0-4): "))
                result = binary_search(grid, row, target)
                print(f"Binary Search result: {result}")
            else:
                print("Invalid search command!")

        else:
            print("Invalid action! Please choose a valid move or search.")

        # Check if game over
        if current_player.health <= 0:
            print(f"{current_player.name} is eliminated!")
            players.remove(current_player)
        if not players or all(grid[x][y] != "T" for x in range(GRID_SIZE) for y in range(GRID_SIZE)):
            print("Game Over!")
            break

        turn += 1

if __name__ == "__main__":
    play_game()

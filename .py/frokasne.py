# FORSAKEN GENERATOR SOLVER
# MADE BY LULUWAFFLESS
# github.com/luluwaffless/codedump

# constants
WAIT = 0.5 # how much it waits in seconds before screenshotting after completing the previous step
SLIDE = 0.05 # slide duration in seconds
REGION = (701, 281, 518) # (x, y, size) - coordinates of the top-left corner and size of the square area to capture, if your screen isnt 1920x1080, 100% zoom and fullscreen roblox then adjust this
EXACT_SIZE = True # if you want to only use the main grid size (6), enable this
INSTRUCTIONS_Y_OFFSET = 54 # when you join a server instructions will appear for the first machine and interrupt the regular region, set this to the height difference of the instructions in pixels

# now onto the actual script
# libraries
from time import sleep
from os import system
import ctypes
try:
    from pynput.keyboard import Listener, Key
    from PIL import ImageGrab
except ImportError:
    print("please install the required libraries by running the following commands:\npip install pynput\npip install Pillow")
    exit()

# screenshots the puzzle area
def grab_puzzle_area(instructions=False):
    if instructions:
        x, y, size = REGION
        y += INSTRUCTIONS_Y_OFFSET
    else:
        x, y, size = REGION
    image = ImageGrab.grab(bbox=(x, y, x + size, y + size))
    return image

# gets the size of the grid, pretty simple, just counts the amount of divisions
def get_grid_length(image, width):
    colors = [image.getpixel((x, 1)) for x in range(width)]
    result = []
    current = []
    for item in colors:
        if item == (20, 20, 20):
            if current:
                result.append(current)
                current = []
        else:
            current.append(item)
    if current:
        result.append(current)
    return len(result)

# finds each pair by their color by iterating through each cell
def get_pairs(image, size):
    width, height = image.size
    cell_size = round(width / size)
    excluded = {"#0a0a0a", "#141414"}
    cells = []
    for row in range(size):
        row_colors = []
        for col in range(size):
            start_x = col * cell_size
            start_y = row * cell_size
            color_count = {}
            for y in range(start_y, min(start_y + cell_size, height)):
                for x in range(start_x, min(start_x + cell_size, width)):
                    rgb = image.getpixel((x, y))
                    hex_color = "#{:02x}{:02x}{:02x}".format(*rgb).lower()
                    if hex_color in excluded:
                        continue
                    color_count[hex_color] = color_count.get(hex_color, 0) + 1
            if color_count:
                predominant = max(color_count, key=lambda k: color_count[k])
            else:
                predominant = ""
            row_colors.append(predominant)
        cells.append(row_colors)
    pairs = {}
    for row_index, row in enumerate(cells):
        for col_index, color in enumerate(row):
            if color == "":
                continue
            pairs.setdefault(color, []).append((col_index, row_index))
    return pairs

# pathfinding algorithm made by AI cuz i had no idea how to make one
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

def solve_branch(pair_list, grid, solution, index, start_path, end, color, grid_size):
    """
    Runs backtracking for one branch (starting path) independently.
    """
    def backtrack(idx, grid, solution):
        if idx == len(pair_list):
            return solution
        color, start, end = pair_list[idx]
        visited = [[False] * grid_size for _ in range(grid_size)]
        visited[start[1]][start[0]] = True

        def generate_paths(x, y, visited, path):
            if (x, y) == end:
                yield list(path)
                return
            for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size and not visited[ny][nx]:
                    if (nx, ny) == end or grid[ny][nx] is None:
                        visited[ny][nx] = True
                        path.append((nx, ny))
                        yield from generate_paths(nx, ny, visited, path)
                        path.pop()
                        visited[ny][nx] = False

        for path_found in generate_paths(start[0], start[1], visited, [start]):
            filled = []
            for (px, py) in path_found:
                if (px, py) not in (start, end):
                    grid[py][px] = color
                    filled.append((px, py))
            new_solution = dict(solution)
            new_solution[color] = path_found
            res = backtrack(idx+1, grid, new_solution)
            if res:
                return res
            for (px, py) in filled:
                grid[py][px] = None
        return None

    # resume search from this branch
    return backtrack(index, [row[:] for row in grid], dict(solution))

def parallel_pathfind_solution(pairs, grid_size):
    pair_list = []
    grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]
    for color, endpoints in pairs.items():
        if len(endpoints) == 2:
            start, end = endpoints
            pair_list.append((color, start, end))
            grid[start[1]][start[0]] = color
            grid[end[1]][end[0]] = color

    # only parallelize the first pair’s possible paths
    color, start, end = pair_list[0]
    visited = [[False] * grid_size for _ in range(grid_size)]
    visited[start[1]][start[0]] = True

    def generate_initial_paths(x, y, visited, path):
        if (x, y) == end:
            yield list(path)
            return
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size and not visited[ny][nx]:
                if (nx, ny) == end or grid[ny][nx] is None:
                    visited[ny][nx] = True
                    path.append((nx, ny))
                    yield from generate_initial_paths(nx, ny, visited, path)
                    path.pop()
                    visited[ny][nx] = False

    initial_paths = list(generate_initial_paths(start[0], start[1], visited, [start]))

    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        futures = []
        for path in initial_paths:
            new_grid = [row[:] for row in grid]
            filled = []
            for (px, py) in path:
                if (px, py) not in (start, end):
                    new_grid[py][px] = color
                    filled.append((px, py))
            new_solution = {color: path}
            futures.append(
                executor.submit(solve_branch, pair_list, new_grid, new_solution, 1, path, end, color, grid_size)
            )

        for f in as_completed(futures):
            result = f.result()
            if result:
                executor.shutdown(cancel_futures=True)
                return result

    return {}
    
# mouse control stuff because i cant just use any mouse-controlling library. fuck you roblox.
PUL = ctypes.POINTER(ctypes.c_ulong)
class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long), ("dy", ctypes.c_long), ("mouseData", ctypes.c_ulong), ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong), ("dwExtraInfo", PUL)]
class Input_I(ctypes.Union):
    _fields_ = [("mi", MouseInput)]
class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]
def send_mouse_event(flags, x=0, y=0, data=0):
    mi = MouseInput(dx=x, dy=y, mouseData=data, dwFlags=flags, time=0, dwExtraInfo=None)
    ii = Input_I(mi=mi)
    input_struct = Input(type=0, ii=ii)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(input_struct), ctypes.sizeof(input_struct))
def move(target_x, target_y, duration=SLIDE, steps=60):
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)
    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    start_x, start_y = pt.x, pt.y
    for i in range(steps + 1):
        t = i / steps
        x = int(start_x + (target_x - start_x) * t)
        y = int(start_y + (target_y - start_y) * t)
        abs_x = int(x * 65535 / screen_width)
        abs_y = int(y * 65535 / screen_height)
        send_mouse_event(0x8001, abs_x, abs_y) 
        sleep(duration / steps)
def down():
    send_mouse_event(0x0002)
def up():
    send_mouse_event(0x0004)

# simplify solution to skip straight lines
def simplify_solution(solution):
    def simplify_path(path):
        if not path or len(path) < 3:
            return path
        simplified = [path[0]]
        for i in range(1, len(path) - 1):
            prev = path[i - 1]
            curr = path[i]
            next_ = path[i + 1]
            if (curr[0] - prev[0], curr[1] - prev[1]) != (next_[0] - curr[0], next_[1] - curr[1]):
                simplified.append(curr)
        simplified.append(path[-1])
        return simplified
    return {color: simplify_path(path) for color, path in solution.items()}

# drawing stuff for the solution
def draw_solution(solution, grid_size, region):
    x0, y0, size = region
    cell_size = size / grid_size
    def to_screen_coords(x, y):
        screen_x = x0 + (x + 0.5) * cell_size
        screen_y = y0 + (y + 0.5) * cell_size
        return int(screen_x), int(screen_y)
    for _, path in solution.items():
        if not path:
            continue
        x, y = to_screen_coords(*path[0])
        move(x, y)
        down()
        for px, py in path[1:]:
            x, y = to_screen_coords(px, py)
            move(x, y)
        up()

# now the fun part, the amalgamation of all functions into something thats useful
def main():
    system('cls')
    print("page down: exit\nright ctrl: start scanning\n---------------------------")
    loop = True
    steps = 0
    while loop:
        image = grab_puzzle_area()
        width, _ = image.size
        size = get_grid_length(image, width)
        if (EXACT_SIZE and size == 6) or (4 <= size <= 25):
            if steps == 0:
                print(f"grid size: {size}\n")
            pairs = get_pairs(image, size)
            print(f"pairs: {len(pairs)}")
            solution = parallel_pathfind_solution(pairs, size)
            if solution:
                print("simplifying...")
                solution = simplify_solution(solution)
                print("drawing...")
                draw_solution(solution, size, REGION)
                print("done!\n")
                steps += 1
                sleep(WAIT)
            else:
                print("ERROR: no solution found for these pairs:\n", pairs)
        else:
            loop = False
            if steps == 0:
                image = grab_puzzle_area(instructions=True)
                width, _ = image.size
                size = get_grid_length(image, width)
                if (EXACT_SIZE and size == 6) or (4 <= size <= 25):
                    loop = True
                    print("instructions detected, took screenshot with offset")
                    if steps == 0:
                        print(f"grid size: {size}\n")
                    pairs = get_pairs(image, size)
                    print(f"pairs: {len(pairs)}")
                    solution = parallel_pathfind_solution(pairs, size)
                    if solution:
                        print("simplifying...")
                        solution = simplify_solution(solution)
                        print("drawing...")
                        draw_solution(solution, size, (REGION[0], REGION[1] + INSTRUCTIONS_Y_OFFSET, REGION[2]))
                        print("done!\n")
                        steps += 1
                        sleep(WAIT)
                    else:
                        print("ERROR: no solution found for these pairs:\n", pairs)
                else:
                    print(f"ERROR: invalid grid size ({size}), expected {"6" if EXACT_SIZE else "4-25"}\ndid you take the screenshot too early{"/forget to disable exact size" if EXACT_SIZE and 4 <= size <= 25 else ""}?")
            else:
                print(f"finished generator with {steps} steps.")

# just the key listener
if __name__ == "__main__":
    system('title frokasne machine solver')
    system('cls')
    print("page down: exit\nright ctrl: start scanning\n---------------------------")
    def on_press(key):
        if key == Key.page_down:
            print("exiting...")
            exit()
        elif key == Key.ctrl_r:
            main()
    with Listener(on_press=on_press) as listener:
        listener.join()
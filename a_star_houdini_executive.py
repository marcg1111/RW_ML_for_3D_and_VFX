import hou
import math
import random
import json
import sys

#add path to A* script
sys.path.append(r"")
from a_star import AStarPathFinding

#get the grid geo
def get_grid():
    node = hou.pwd()
    grid_path = node.parm('grid_path').eval()
    grid_geo = hou.node(grid_path).geometry()
    if not grid_geo:
        raise hou.NodeError(f"Invalid grid path: {grid_path}")
    return grid_geo


def get_maze_from_grid(grid_geo):
    prims = grid_geo.prims()
    
    #calculating rows/colums count
    num_rows = num_colums = int(math.sqrt(len(prims)))
    
    grid_matrix = []
    for row in range(num_rows):
        new_row = []
        for col in range(num_colums):
            prim_index = row*num_colums + col
            prim = grid_geo.prim(prim_index)
            color = prim.attribValue("Cd")
            #append 1 to the row if color is white, otherwise 0
            new_row.append(1 if color == (1.0, 1.0, 1.0) else 0)
        grid_matrix.append(new_row)
    return grid_matrix

def solve_maze():
    node = hou.pwd()
    grid_geo = get_grid()
    maze = get_maze_from_grid(grid_geo)

    # Get white prim positions to place main char and NPCs
    white_positions = []
    for prim in grid_geo.prims():
        cd = prim.attribValue("Cd")
        if cd == (1.0, 1.0, 1.0):
            center = prim.boundingBox().center()
            pos_x = round(center[0])
            pos_z = round(center[2])
            white_positions.append((pos_x, 0, pos_z))
    random.shuffle(white_positions)

    # Place main char
    main_char_path = node.parm("main_char").eval()
    main_char = hou.node(main_char_path)
    if not main_char:
        raise hou.NodeError(f"Invalid main_char path: {main_char_path}")
    main_char_pos = white_positions.pop()
    main_char.parmTuple("t").set(main_char_pos)

    # Place NPCs and compute paths
    npc_count = node.parm("npcs").eval()
    if npc_count > len(white_positions):
        raise hou.NodeError("Not enough white tiles for all NPCs.")

    target_x, _, target_z = main_char_pos
    target_rc = (int(round(target_z)), int(round(target_x)))  # row = Z, col = X

    npc_paths = {}
    for i in range(npc_count):
        npc_path_parm = node.evalParm(f"npc_{i+1}")
        npc_node = hou.node(npc_path_parm)
        if not npc_node:
            raise hou.NodeError(f"Invalid NPC path: {npc_path_parm}")

        npc_pos = white_positions.pop()
        npc_node.parmTuple("t").set(npc_pos)
        x, _, z = npc_pos
        npc_rc = (int(round(z)), int(round(x)))  # row = Z, col = X

        path_finder = AStarPathFinding(maze, npc_rc, target_rc)
        path = path_finder.find_path()
        #debug------------------------------------------------------------------
        print(path)
        if path:
            path = [(int(round(r)), int(round(c))) for r, c in path]
        npc_paths[npc_path_parm] = path if path else []

    #Stores paths as a JSON string in node's user data
    node.setUserData('npc_paths', json.dumps(npc_paths))
    
    updateNpcsPosition(node)
    return path

def updateNpcsPosition(node):
    import json

    # Get current frame 
    step_index = max(0, hou.frame()-1) 

    npc_paths_str = node.userData('npc_paths')
    if not npc_paths_str:
        return  # no paths yet

    npc_paths = json.loads(npc_paths_str)
    
    # Find the longest path for looping
    max_path_length = max((len(path) for path in npc_paths.values()), default=0)
    if max_path_length == 0:
        return  # All paths are empty
        
    # Wrap around using modulo
    step = int(step_index % max_path_length)

    # Move each NPC
    for npc_node_path, path in npc_paths.items():
        if not path:
            continue

        npc_node = hou.node(npc_node_path)
        if not npc_node:
            continue
            
    # Clamp step if this NPC has a shorter path
        local_step = min(step, len(path)-1)
        
        row, col = path[int(local_step)]
        npc_node.parmTuple('t').set((col, 0, row))
        print(f"step: {step}")
        print(f"npc should be on row: {row} and col: {col} _____________________________________________")
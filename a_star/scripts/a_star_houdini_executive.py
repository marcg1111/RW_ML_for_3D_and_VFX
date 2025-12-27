import hou
import math
import sys

sys.path.append(r"C:\Users\marcg\OneDrive\rebelway_ML_for_3D_and_VFX\RW_ML_for_3D_and_VFX\a_star\scripts")

from a_star import AStarPathFinding

#convert 2D grid to matrix
def get_maze_from_grid():
    grid = hou.pwd().parm('grid_path').eval()
    geo = hou.node(grid).geometry()
    
    prims = geo.prims()
    num_rows = num_colums = int(math.sqrt(len(prims)))
    
    grid_matrix = []
    
    for row in range(num_rows):
        new_row = []
        for col in range(num_colums):
            prim_index = row*num_colums + col
            prim = geo.prim(prim_index)
            color = prim.attribValue("Cd")
            new_row.append(1 if color == (1.0, 1.0, 1.0) else 0)
        grid_matrix.append(new_row)
        
    #print("______________DEBUG MATRIX___________________________")
    #for row in grid_matrix:
    #   print(row)
    
    return grid_matrix
    

def position_object(obj_path, row, col, cell_size=1, num_rows=None):
    main_char = hou.node(obj_path)
    
    if num_rows is None:
        num_rows = 7  # Or dynamically detect it

    world_x = col * cell_size
    world_z = (num_rows - 1 - row) * cell_size  # Flip Z

    main_char.parmTuple("t").set((world_x, 0, world_z))
    pos = (row, col)
    
    print(pos)
    return pos
    
def solve_maze():
    main_char_path = hou.pwd().parm("main_char").eval()
    npc1_char_path = hou.pwd().parm("npc_1").eval()
    
    start_pos = position_object(npc1_char_path, 0,3)
    target_pos = position_object(main_char_path, 6, 1)
    
    maze = get_maze_from_grid()
    print("")
    for row in maze:
        print(row)
        
    path_finder = AStarPathFinding(maze, start_pos, target_pos)
    path = path_finder.find_path()
    
    if path:
        print("Path found: ", path)
        
    else:
        print("No path found.")
    

    
    
    
    
    
    
    
    
    import hou
import random

def place_npc():
    node = hou.pwd()

    # Get the grid node
    grid_path = node.parm('grid_path').eval()
    grid_node = hou.node(grid_path)
    if not grid_node:
        raise hou.NodeError(f"Invalid grid path: {grid_path}")

    geo = grid_node.geometry()

    # Check if Cd attribute exists
    if geo.findPrimAttrib("Cd") is None:
        raise hou.NodeError("Grid does not have a 'Cd' primitive attribute.")

    # Collect valid (x, z) integer coordinates from white prims
    white_positions = []
    for prim in geo.prims():
        cd = prim.attribValue("Cd")
        if cd == (1.0, 1.0, 1.0):  # pure white
            center = prim.boundingBox().center()
            
            pos_x = round(center[0])
            pos_z = round(center[2])
            white_positions.append((pos_x, 0, pos_z))

    if not white_positions:
        raise hou.NodeError("No white fields found on the grid.")

    random.shuffle(white_positions)
    
    
    #Place main character
    main_char_path = node.parm("main_char").eval()
    main_char = hou.node(main_char_path)
    if not main_char:
        raise hou.NodeError(f"Invalid main_char path: {main_char_path}")

    main_char_pos = white_positions.pop()  # reserve one position
    main_char.parmTuple("t").set(main_char_pos)
    

    #Place NPCs
    npc_count = node.parm("npcs").eval()
    if npc_count > len(white_positions):
        raise hou.NodeError("Not enough white tiles for all NPCs (excluding main char).")

    for i in range(npc_count):
        npc_path = node.evalParm(f"npc_{i+1}")
        npc_node = hou.node(npc_path)
        if not npc_node:
            raise hou.NodeError(f"Invalid NPC path: {npc_path}")
        
        npc_pos = white_positions.pop()
        npc_node.parmTuple("t").set(npc_pos)
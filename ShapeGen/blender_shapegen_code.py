import bpy
import math
import random
import os
import sys
from mathutils import Matrix, Vector

# Configuration
filepath_name = '/Users/albert/Documents/GitHub/Human_AI_perception/ShapeGen'  # folder dir
amount_count = 10 # How many extrusion do you need？
rotate_num = 1000 # How many set of generation picture?
loop_count = 5 # How many generation in one set?

# Get command-line arguments
args = sys.argv
if "--" in args:
    user_args = args[args.index("--") + 1:]  # Extract everything after "--"
else:
    user_args = []

# Ensure the user provided the OBJ file path
if len(user_args) < 1:
    print("Usage: blender --background --python script.py -- <amount> <angle>")
    sys.exit(1)

# Valid input, working on directory X (from 1-9)
amount = int(user_args[0])
rotation_increment = math.radians(int(user_args[1]))

# Create the directory for the angle
filepath_name = os.path.join(filepath_name, str(user_args[1]))
os.makedirs(filepath_name, exist_ok=True)

# Cleanup function
def clear_scene():
    for collection in list(bpy.data.collections):
        for obj in collection.objects:
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(collection)
    
    # Clear remaining objects
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    
    # Clear orphan data
    for block in [bpy.data.meshes, bpy.data.materials]:
        for item in block:
            block.remove(item)

# Rotation function using proper world-space matrix operations
def rotate_around_world(obj, axis, angle):
    """Rotate object around world axis using matrix multiplication"""
    # Create rotation matrix
    rot_matrix = Matrix.Rotation(angle, 4, axis)
    # Apply to world matrix
    obj.matrix_world = rot_matrix @ obj.matrix_world
    # Force update of object data
    obj.data.update()
 

def shapeGenGenerator(amount, seed):
    # Generate the shape collection
    bpy.ops.mesh.shape_generator()
    collection = bpy.data.collections["Generated Shape Collection"]
    
    # Set shape generator properties
    props = collection.shape_generator_properties
    props.random_seed = seed
    props.is_bevel = True
    props.bevel_segments = 10
    props.amount = amount
    
    # Get generated object
    shape_obj = bpy.data.objects['Generated Shape']
    
    # Set origin to geometry center
    bpy.context.view_layer.objects.active = shape_obj
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    
    # Apply scale transformations
    bpy.ops.object.select_all(action='DESELECT')
    shape_obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    return shape_obj

# Create output directories
base_path = filepath_name

for seed in range(1,rotate_num+1):
    # check if the specific directory exists, if it is, skip this one
    current_path = base_path + "/" + str(seed)
    if os.path.exists(current_path):
        pass
    else:
        clear_scene()
        os.makedirs(base_path, exist_ok=True)
        
        # Generate shape object
        shape_obj = shapeGenGenerator(amount, seed)
        shape_obj.location[0] = 0
        shape_obj.location[1] = 0
        shape_obj.location[2] = 0

        
        # Add camera
        bpy.ops.object.camera_add()
        camera = bpy.context.object

        # Adjust camera position to directly face the object's mass center
        camera_distance = 7.0  # Adjust as needed
        camera.location = Vector((0, -camera_distance, 0))
        camera.rotation_euler = (math.radians(90), 0, 0)  # Face forward
        
        # Configure render settings
        scene = bpy.context.scene
        scene.render.engine = 'BLENDER_WORKBENCH'
        scene.render.resolution_x = 1080
        scene.render.resolution_y = 1080
        scene.display.shading.light = 'STUDIO'
        scene.display.shading.color_type = 'MATERIAL'
        scene.render.film_transparent = True
        scene.camera = camera
        
        # Initial render
        scene.render.filepath = os.path.join(current_path, "initial.png")
        bpy.ops.render.render(write_still=True)
        
        # Perform rotations and render
        rotation_steps = []
        for step in range(loop_count):
            # Generate random rotation
            axis = random.choice(['X', 'Y', 'Z'])
            direction = random.choice([-1, 1])
            angle = direction * rotation_increment
            
            # Apply rotation
            rotate_around_world(shape_obj, axis, angle)
            
            # Update rotation history
            rotation_steps.append(f"{'-' if direction < 0 else ''}{axis}")
            
            # Render and save
            fname = f"rotation_{'_'.join(rotation_steps)}.png"
            scene.render.filepath = os.path.join(current_path, fname)
            bpy.ops.render.render(write_still=True)
            
    #            # Force UI update
    #            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

print("Rendering completed successfully!")

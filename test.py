import bpy
import math
import random
from mathutils import Matrix, Vector
import os
import sys

# Configuration
collection_name = "ImportedMeshes"
rotation_increment = math.radians(15)  # Convert degrees to radians
loop = 7
filepath_name = os.getcwd()  # Use the current working directory
#obj_directory = '/Users/albert/.cache/huggingface/hub/datasets--ShapeNet--ShapeNetCore/blobs/02773838/10a885f5971d9d4ce858db1dc3499392/models/model_normalized.obj'
obj_directory = '/Users/albert/.cache/huggingface/hub/datasets--ShapeNet--ShapeNetCore/blobs/'

# Get command-line arguments
args = sys.argv
if "--" in args:
    user_args = args[args.index("--") + 1:]  # Extract everything after "--"
else:
    user_args = []

# Ensure the user provided the OBJ file path
if len(user_args) < 1:
    print("Usage: blender --background --python script.py -- <obj_path>")
    sys.exit(1)

obj_path = obj_directory+user_args[0]+'/models/model_normalized.obj' # First argument: Object file path

# Print the provided path for confirmation
print(f"Loading OBJ file from: {obj_path}")

# Cleanup function
def clear_scene():
    # Remove existing collection
    collection = bpy.data.collections.get(collection_name)
    if collection:
        for obj in collection.objects:
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(collection)
    
    # Clear remaining objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

# Fix normals function
def recalculate_normals(obj):
    if obj.type == 'MESH':
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.mode_set(mode='OBJECT')

# Scene setup
clear_scene()

# Import OBJ file
bpy.ops.wm.obj_import(
    filepath=bpy.path.abspath(obj_path),
    use_split_objects=True,
    use_split_groups=True,
    validate_meshes=True
)

# Create a new collection and move imported objects
new_collection = bpy.data.collections.new(collection_name)
bpy.context.scene.collection.children.link(new_collection)
for obj in bpy.data.objects:
    new_collection.objects.link(obj)

# Fix normals
for obj in new_collection.objects:
    if obj.type == 'MESH':
        recalculate_normals(obj)

# Calculate center of mass of the imported object
def get_collection_center(collection):
    total_center = Vector((0, 0, 0))
    total_vertices = 0
    
    for obj in collection.objects:
        if obj.type == 'MESH':
            world_matrix = obj.matrix_world
            for v in obj.data.vertices:
                world_v = world_matrix @ v.co
                total_center += world_v
                total_vertices += 1
    
    if total_vertices > 0:
        return total_center / total_vertices
    return Vector((0, 0, 0))

mass_center = get_collection_center(new_collection)

# Set up Workbench rendering engine
scene = bpy.context.scene
scene.render.engine = 'BLENDER_WORKBENCH'
scene.render.resolution_x = 1080
scene.render.resolution_y = 1080

# Workbench shading settings for white background
scene.display.shading.light = 'STUDIO'
scene.display.shading.color_type = 'MATERIAL'
scene.display.shading.background_type = 'VIEWPORT'  # Force a solid background
scene.display.shading.background_color = (1, 1, 1)  # White background

scene.display.shading.show_backface_culling = True  # Optional, but can help with transparency
scene.render.film_transparent = True  # Enable transparent background

# Create an empty object at the mass center for correct rotation
bpy.ops.object.empty_add(type='PLAIN_AXES', location=mass_center)
parent_empty = bpy.context.object
parent_empty.name = "WorldRotationPivot"

# Parent all objects to the empty
for obj in new_collection.objects:
    obj.parent = parent_empty

# Set up the camera at an appropriate distance
if not any(o for o in scene.objects if o.type == 'CAMERA'):
    bpy.ops.object.camera_add()
    camera = bpy.context.object
    scene.camera = camera

# Adjust camera position to directly face the object's mass center
camera_distance = 3.0  # Adjust as needed
camera.location = mass_center + Vector((0, -camera_distance, 0))
camera.rotation_euler = (math.radians(90), 0, 0)  # Face forward

# Ensure the camera tracks the mass center
bpy.ops.object.empty_add(type='PLAIN_AXES', location=mass_center)
target_empty = bpy.context.object
target_empty.name = "CameraTarget"

# Apply tracking constraint to the camera
track = camera.constraints.new(type='TRACK_TO')
track.target = target_empty
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'

# Function to rotate around world axes
def rotate_around_world(obj, axis, angle):
    """Applies rotation around the world axis."""
    rot_matrix = Matrix.Rotation(angle, 4, axis)
    obj.matrix_world = rot_matrix @ obj.matrix_world

# Rotation and rendering setup
rotation_order = ''

# Initial render before rotation
scene.render.filepath = f"{filepath_name}/sample.png"
bpy.ops.render.render(write_still=True)

# Perform rotations and render each step
for i in range(1, loop):
    axis = random.choice(['X', 'Y', 'Z'])  # Choose a random axis
    direction = random.choice([-1, 1])  # Choose a random direction
    angle = direction * rotation_increment  # Apply the increment

    # Update rotation order string
    rotation_symbol = f"{'-' if direction == -1 else ''}{axis}"
    rotation_order = f"{rotation_order}_{rotation_symbol}" if rotation_order else rotation_symbol

    # Apply rotation around the selected world axis
    rotate_around_world(parent_empty, axis, angle)

    # Render and save the image
    scene.render.filepath = f"{filepath_name}/sample_{rotation_order}.png"
    bpy.ops.render.render(write_still=True)

print("Rendering complete!")


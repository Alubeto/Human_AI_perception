#!/bin/bash

BLENDER_TIMEOUT=60  # 1 minutes, if it has not finished the process yet, kill it
# Define paths
WORKING_DIR="/Users/albert/Documents/GitHub/Human_AI_perception"
OUTPUT_FILE="directory.txt"
SCRIPT_DIR="/Users/albert/Documents/GitHub/Human_AI_perception/blender_code.py"

# Check if output file exists
if [ ! -f "$OUTPUT_FILE" ]; then
    echo "Error: $OUTPUT_FILE not found!"
    exit 1
fi

# Read the batch info
echo "Enter the batch info:"
read name
echo "Generating batch $name!"

WORKING_DIR="/Users/albert/Documents/GitHub/Human_AI_perception/$name"

while IFS= read -r line; do
     # Extract folder and subfolder
     folder=$(echo "$line" | cut -d'/' -f1)
     subfolder=$(echo "$line" | cut -d'/' -f2)
 
     # Check if the working directory exist, if not create one
     mkdir -p "$WORKING_DIR/$folder"
     
     # Check if the folder exists
     if [ -d "$WORKING_DIR/$folder" ]; then
         # Change to the subfolder
         cd "$WORKING_DIR/$folder" || { echo "Failed to enter $folder"; continue; }
         
         # Check if the subfolder exists, if not create it
         mkdir -p "$subfolder"
         cd "$subfolder" || { echo "Failed to enter $subfolder"; continue; }
         
         # Run Blender in the background
         echo "Running Blender in $WORKING_DIR/$folder/$subfolder"
         timeout $BLENDER_TIMEOUT /Applications/Blender.app/Contents/MacOS/Blender -b -P "$SCRIPT_DIR" -- "$folder/$subfolder"
 
         # Move back to the working directory
         cd "$WORKING_DIR" || exit
     else
         echo "Warning: Folder $folder does not exist in $WORKING_DIR"
     fi

done < "$OUTPUT_FILE"

echo "Script execution completed."

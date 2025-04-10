#!/bin/bash

# Define paths
WORKING_DIR="/Users/albert/Documents/GitHub/Human_AI_perception"
OUTPUT_FILE="output.txt"

# Check if output file exists
if [ ! -f "$OUTPUT_FILE" ]; then
    echo "Error: $OUTPUT_FILE not found!"
    exit 1
fi

# Read each line from output.txt
while IFS= read -r line; do
    # Extract folder and subfolder
    folder=$(echo "$line" | cut -d'/' -f1)
    subfolder=$(echo "$line" | cut -d'/' -f2)

    # Check if the folder exists
    if [ -d "$WORKING_DIR/$folder" ]; then
        # Change to the subfolder
        cd "$WORKING_DIR/$folder" || { echo "Failed to enter $folder"; continue; }
        
        # Check if the subfolder exists, if not create it
        mkdir -p "$subfolder"
        cd "$subfolder" || { echo "Failed to enter $subfolder"; continue; }
        
        # Run Blender in the background
        echo "Running Blender in $WORKING_DIR/$folder/$subfolder"
        /Applications/Blender.app/Contents/MacOS/Blender -b -P test.py -- "$folder/$subfolder" &

        # Move back to the working directory
        cd "$WORKING_DIR" || exit
    else
        echo "Warning: Folder $folder does not exist in $WORKING_DIR"
    fi

done < "$OUTPUT_FILE"

echo "Script execution completed."


#!/bin/bash

# Specify the directory you want to read
TARGET_DIR="/Users/albert/.cache/huggingface/hub/datasets--ShapeNet--ShapeNetCore/blobs"

WORKING_DIR="/Users/albert/Documents/GitHub/Human_AI_perception"

BLENDER_PATH="/Applications/Blender.app/Contents/MacOS/Blender"

SCRIPT_PATH="/Users/albert/Documents/GitHub/Human_AI_perception/test.py"

# Check if the directory exists
if [ -d "$TARGET_DIR" ]; then
    echo "Reading directories in: $TARGET_DIR"
    
    # Move to the target directory
    cd "$TARGET_DIR" || { echo "Failed to cd into $TARGET_DIR"; exit 1; }
    
    # Loop through all items in the TARGET_DIR
    for first_level in *; do
        # Check if the item is a directory
        if [ -d "$first_level" ]; then
            echo "Found first-level directory: $first_level"
            echo "Duplicating first-level directory: $first_level"
            cd "$WORKING_DIR"
            if [ -d "$WORKING_DIR/$first_level" ]; then
                echo "Directory $first_level already exists in $WORKING_DIR, skipping..."
                cd "$TARGET_DIR"
                continue
            fi
            mkdir -p "$first_level"
            # Switch back to the target directory
            cd "$TARGET_DIR"
        else
            # If it doesn't exist, create it
            # Switch to working directory and make the directory
            echo "Not A directory"
        fi
        
        # Switch back to the target directory
        cd "$TARGET_DIR"
        # Move into the first-level directory
        cd "$first_level" || { echo "Failed to cd into $first_level"; continue; }
        
        # Loop through all items in the first-level directory
        for second_level in *; do
            # Check if the item is a directory
            if [ -d "$second_level" ]; then
                echo "Found second-level directory: $second_level"
                # If it doesn't exist, create it
                echo "Creating second-level directory: $second_level"
                # Switch to working directory and make the directory
                cd "$WORKING_DIR/$first_level"
                mkdir -p "$second_level"
                cd "$second_level"
                gtimeout 60 "$BLENDER_PATH" --background --python "$SCRIPT_PATH" -- "$first_level/$second_level"
#                BLENDER_PID=$!  # Get Blender process ID
#
#                # Wait for Blender to finish, but kill it after 300 seconds
#                ( sleep 200 && kill -9 $BLENDER_PID 2>/dev/null && echo "Blender force killed due to timeout: $first_level/$second_level" ) &
#
#                wait $BLENDER_PID  # Wait for Blender to complete
#            else
                echo "Not a directory"
            fi
            # Switch to target directory
            cd "$TARGET_DIR/$first_level"
        done
        
        # Move back to the previous level (TARGET_DIR)
        cd ..
    done
else
    echo "Error: Directory $TARGET_DIR does not exist."
fi

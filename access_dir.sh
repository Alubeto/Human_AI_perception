#!/bin/bash

# Specify the directory you want to read
TARGET_DIR="/Users/albert/.cache/huggingface/hub/datasets--ShapeNet--ShapeNetCore/blobs"

# Output file to store the paths
OUTPUT_FILE="/Users/albert/Documents/GitHub/Human_AI_perception/output.txt"

# Clear the output file (if it exists) or create a new one
> "$OUTPUT_FILE"

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
            
            # Move into the first-level directory
            cd "$first_level" || { echo "Failed to cd into $first_level"; continue; }
            
            # Loop through all items in the first-level directory
            for second_level in *; do
                # Check if the item is a directory
                if [ -d "$second_level" ]; then
                    echo "Found second-level directory: $second_level"
                    
                    # Write the full path to the output file
                    echo "$first_level/$second_level" >> "$OUTPUT_FILE"
                fi
            done
            
            # Move back to the previous level (TARGET_DIR)
            cd ..
        fi
    done
    
    echo "All paths have been written to: $OUTPUT_FILE"
else
    echo "Error: Directory $TARGET_DIR does not exist."
fi

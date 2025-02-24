#!/bin/bash

# Specify the directory you want to read
TARGET_DIR="/Users/albert/.cache/huggingface/hub/datasets--ShapeNet--ShapeNetCore/blobs"

# Check if the directory exists
if [ -d "$TARGET_DIR" ]; then
    echo "Reading directories in: $TARGET_DIR"
    
    # Loop through all items in the TARGET_DIR
    for first_level in "$TARGET_DIR"/*; do
        # Check if the item is a directory
        if [ -d "$first_level" ]; then
            # Loop through all items in the first-level directory
            for second_level in "$first_level"/*; do
                # Check if the item is a directory
                if [ -d "$second_level" ]; then
                    # Print the full path of the second-level directory
                    echo "$second_level"
                fi
            done
        fi
    done
else
    echo "Error: Directory $TARGET_DIR does not exist."
fi

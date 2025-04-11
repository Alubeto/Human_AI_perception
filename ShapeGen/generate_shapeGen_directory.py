# Open a file for writing ('w' mode)
# This will create the file if it doesn't exist, or overwrite it if it does
with open('shapeGen_directory.txt', 'w') as file:
    for i in range(1,10):
        for j in range(1,10001):
            file.write(f"{i}/{j}\n")

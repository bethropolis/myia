import os
import re

def generate_version_name(file_name, directory='.'):
    
    # Extracting the base file name without extension
    base_name, extension = os.path.splitext(file_name)

    # Searching for files with similar names in the directory
    matching_files = [f for f in os.listdir(directory) if f.startswith(base_name)]

    # Extracting versions from matching files
    versions = []
    pattern = re.compile(rf"{re.escape(base_name)}_(\d+_\d+_\d+)\.\w+")
    for file in matching_files:
        match = pattern.match(file)
        if match:
            versions.append(match.group(1))

    # Function to increment the version
    def increment_version(version):
        version_parts = list(map(int, version.split('_')))
        version_parts[-1] += 1  # Incrementing the last part of the version
        return '_'.join(map(str, version_parts))

    if versions:
        # Sorting versions and getting the latest one
        versions.sort(reverse=True)
        latest_version = versions[0]
        
        # Generating the next version
        next_version = increment_version(latest_version)
        new_file_name = f"{base_name}_{next_version}{extension}"  # Dynamically adding the extension
        if os.path.exists(new_file_name):
            print(f"A file with the generated version '{new_file_name}' already exists.")
            return None
        else:
            return new_file_name
    else:
        return f"{base_name}_1_0_0{extension}"  # Dynamically adding the extension

    

import os
import yaml
import json

def load_yaml(filepath, mode='r', encoding='utf-8'):
    with open(filepath, mode, encoding=encoding) as f:
        data = yaml.full_load(f)
        return data

def save_yaml(data, filepath, mode='w', encoding='utf-8'):
    with open(filepath, mode, encoding=encoding) as f:
        yaml.dump(data, f)

def load_json(filepath, mode='r', encoding='utf-8'):
    with open(filepath, mode, encoding=encoding) as f:
        data = json.load(f)
        return data

def save_json(data, filepath, mode='w', encoding='utf-8'):
    with open(filepath, mode, encoding=encoding) as f:
        json.dump(data, f, indent=4)

def get_directory_size(directory):
    """Returns the `directory` size in bytes."""
    total = 0
    try:
        # print("[+] Getting the size of", directory)
        for entry in os.scandir(directory):
            if entry.is_file():
                # if it's a file, use stat() function
                total += entry.stat().st_size
            elif entry.is_dir():
                # if it's a directory, recursively call this function
                total += get_directory_size(entry.path)
    except NotADirectoryError:
        # if `directory` isn't a directory, get the file size then
        return os.path.getsize(directory)
    except PermissionError:
        # if for whatever reason we can't open the folder, return 0
        return 0
    return total

def get_directory_size(directory):
    """Returns the `directory` size in bytes."""
    total = 0
    try:
        for entry in os.scandir(directory):
            if entry.is_file():
                # if it's a file, use stat() function
                total += entry.stat().st_size
            elif entry.is_dir():
                # if it's a directory, recursively call this function
                total += get_directory_size(entry.path)
    except NotADirectoryError:
        # if `directory` isn't a directory, get the file size then
        return os.path.getsize(directory)
    except PermissionError:
        # if for whatever reason we can't open the folder, return 0
        return 0
    return total

def get_file_extension(filename, remove_dot=True, default=''):
    ext = os.path.splitext(filename)[1]

    if len(ext) > 0:
        return ext[1:] if remove_dot else ext
    else:
        return default

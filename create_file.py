from os import makedirs, path
import time

def write_file(pathname, filename, string):
    '''save string to file'''
    if not path.isdir(pathname):
        try:
            makedirs(pathname, exist_ok=True)
        except OSError as e:
            raise RuntimeError("Error creating file path")
    full_path = path.join(pathname, filename)
    try:
        f = open(full_path, "w")
    except OSError:
        raise RuntimeError("Error opening file: " + full_path)
    f.write(string)
    time.sleep(0.5)
    print("File created: " + path.abspath(f.name))
    f.close()
    return
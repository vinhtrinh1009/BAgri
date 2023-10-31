
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print('base_dir: ', base_dir)
map_type = {"string": "string", "array": "repeated"}

class Config:
    pass

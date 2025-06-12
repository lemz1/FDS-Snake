import os

functions_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.dirname(functions_dir)

def get_asset_path(relative_path_from_project_root):
    return os.path.join(project_root_dir, relative_path_from_project_root)

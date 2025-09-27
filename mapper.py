import os

def list_files(startpath, prefix=""):
    files = os.listdir(startpath)
    files.sort()  # optional: keeps output sorted

    for index, f in enumerate(files):
        path = os.path.join(startpath, f)
        connector = "└── " if index == len(files) - 1 else "├── "
        print(prefix + connector + f)
        if os.path.isdir(path):
            extension = "    " if index == len(files) - 1 else "│   "
            list_files(path, prefix + extension)

if __name__ == "__main__":
    project_folder = "."  # Change this to your folder path
    print(project_folder)
    list_files(project_folder)

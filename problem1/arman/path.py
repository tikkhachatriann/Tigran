import armen
import tiko
import inspect
import os


def get_path() -> list:
     list_for_path = []
     list_for_path.append(inspect.getfile(armen))
     list_for_path.append(inspect.getfile(tiko))
     list_for_path.sort()
     return list_for_path


def get_size() -> list:
    list_for_size = []
    list_for_size.append(os.path.getsize(inspect.getfile(armen)))
    list_for_size.append(os.path.getsize(inspect.getfile(tiko)))
    list_for_size.sort()
    return list_for_size


def get_info(path):
    list_for_depth = []
    for dirPath, dirNames, fileNames in os.walk(path):
        steps = dirPath.split("/")
        steps.pop(0)
        depths = len(steps)
        list_for_depth.append(depths)
        print("depths", depths)
        print("Directory Path: ", dirPath)
        print("Directories = ", dirNames)
        print("Files = ", fileNames)
        print('-' * 10)
    print(f"The maximum depths of path: {max(list_for_depth)}")


if __name__ == "__main__":
    print(
        f" list for paths {get_path()} \n",
        f"list for sizes {get_size()} \n "
    )
    get_info(os.getcwd())

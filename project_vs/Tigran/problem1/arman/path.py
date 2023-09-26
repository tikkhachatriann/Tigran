import os


def get_info(path):

    list_for_path = []
    list_for_size = []
    list_for_depth = []

    for dirPath, dirNames, fileNames in os.walk(path):
        steps = dirPath.split("/")
        depths = len(steps)

        list_for_path.append(dirPath)
        list_for_size.append(os.path.getsize(dirPath))
        list_for_depth.append(depths)

    list_for_path.sort()
    list_for_size.sort()

    while True:
        press_dig = input(
            "if you want sort by path "
            "press 1 if by size press 2 "
            "if you want see count of maximum depths press 3"
        )

        if press_dig == "1":
            print(f"The list of path: {list_for_path}")
        elif press_dig == "2":
            print(f"The list size of path: {list_for_size}")
        elif press_dig == "3":
            print(f"The maximum depths of path: {max(list_for_depth)}")
        else:
            break

    return list_for_path, list_for_size, list_for_size


if __name__ == "__main__":
    get_info(os.getcwd())

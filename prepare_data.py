import os

PACKAGE: str = "juego"

if __name__ == "__main__":
    files_names = os.listdir(f"./{PACKAGE}/submissions")
    for name in files_names:
        if not name.startswith("__"):
            index = name.find("_")
            tmp_name = f"{name[:index].strip()}.py"
            new_name = tmp_name.lower().replace(" ", "_")
            os.renames(f"./{PACKAGE}/submissions/{name}", f"./{PACKAGE}/submissions/{new_name}")

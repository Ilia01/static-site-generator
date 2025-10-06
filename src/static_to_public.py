import os
import shutil

PUBLIC_FOLDER_PATH = "../public"
STATIC_FOLDER_PATH = "../static"


def static_to_public(public_path=PUBLIC_FOLDER_PATH, static_path=STATIC_FOLDER_PATH):
    print(f"Starting copy process from '{static_path}' to '{public_path}'.")

    try:
        if os.path.exists(public_path):
            print(f"Removing existing directory tree: {public_path}")
            shutil.rmtree(public_path)
            print(f"Re-Creating directory: {public_path}")
            os.mkdir(public_path)
        else:
            print(f"Creating directory: {public_path}")
            os.mkdir(public_path)

        for f in os.listdir(static_path):
            static_child_path = os.path.join(static_path, f)
            public_relative_path = os.path.join(public_path, f)

            if os.path.isdir(static_child_path):
                print(f"  Found subdirectory: '{static_child_path}'. Recursing.")
                static_to_public(
                    public_path=public_relative_path, static_path=static_child_path
                )
            else:
                print(
                    f"  Copying file: '{static_child_path}' to '{public_relative_path}'"
                )
                shutil.copy(static_child_path, public_relative_path)

    except Exception as e:
        print(f"CRITICAL ERROR: An unexpected error occurred: {e}")

    print("Copy process finished.")

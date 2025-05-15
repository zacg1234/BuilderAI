import os
import shutil

output_folder_path = "output"



def reset_output_folder():
    if os.path.exists(output_folder_path):
        shutil.rmtree(output_folder_path)
    os.makedirs(output_folder_path, exist_ok=True)
    return f"Output folder '{output_folder_path}' has been reset."

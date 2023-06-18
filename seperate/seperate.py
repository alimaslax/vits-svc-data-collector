import os
import subprocess
import shlex

folder_path = './dreamchasers3'

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        print(file_path)
        script = f'demucs --two-stems vocals "{file_path}"'
        subprocess.run(shlex.split(script))
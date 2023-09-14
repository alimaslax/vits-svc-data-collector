import os
import subprocess
import shlex
import shutil

folder_path = './vocals/realme2'
source_folder = './vocals/realme2'
destination_folder = './separated'
rename_flag = False

if (not rename_flag):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            print(file_path)
            script = f'demucs --two-stems vocals "{file_path}"'
            subprocess.run(shlex.split(script))

            filename = filename.replace('.mp4','')
            # Get the output file path
            #output_path = os.path.join(source_folder, f'{filename}', 'vocals.wav')

            # Get the destination file path
            #destination_path = os.path.join(source_folder, f'{filename}.wav')

            # Move the separated vocals.wav file to the destination path
            #shutil.move(output_path, destination_path)
else:
    # Iterate over all subdirectories in the source folder
    for root, dirs, files in os.walk(source_folder):
        for dir_name in dirs:
            # Get the current subdirectory path
            subdir_path = os.path.join(root, dir_name)

            # Get the source file path
            source_file_path = os.path.join(subdir_path, 'vocals.wav')

            # Check if the source file exists
            if os.path.isfile(source_file_path):
                # Get the filename without the extension
                filename = os.path.basename(subdir_path)

                # Get the destination file path
                destination_file_path = os.path.join(destination_folder, f'{filename}.wav')

                # Move the file to the destination folder
                shutil.move(source_file_path, destination_file_path)
                print(f"Moved file: {source_file_path} --> {destination_file_path}")


import os
import shutil
import subprocess
from itertools import count


folder_counter = count(start=1)
file_counter = count(start=1)

def reset_file_counter():
    global file_counter
    file_counter = count(start=1)

def format_id(id):
    return 'id' + str(next(folder_counter)).zfill(5)

def format_file_name(file):
    base, ext = os.path.splitext(file)
    return str(next(file_counter)).zfill(5) + ext

def m4a_to_wav(src_dir, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.m4a'):
                src_file_path = os.path.join(root, file)
                dst_file_path = os.path.join(dst_dir, format_file_name(file).replace('.m4a', '.wav'))
                
                if not os.path.exists(dst_file_path):
                  command = f'ffmpeg -i {src_file_path} {dst_file_path}'
                  subprocess.call(command, shell=True)
            elif file.endswith('.wav'):
                src_file_path = os.path.join(root, file)
                dst_file_path = os.path.join(dst_dir, format_file_name(file))
                
                if not os.path.exists(dst_file_path):
                    shutil.copy(src_file_path, dst_file_path)


def process_voxceleb(base_dir):
    ids = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    
    for id in ids:
        reset_file_counter()
        old_id_dir = os.path.join(base_dir, id)
        new_id_dir = os.path.join(base_dir, format_id(id))
        
        if old_id_dir != new_id_dir:
            
            if not os.path.exists(new_id_dir):
                os.rename(old_id_dir, new_id_dir)
            else: # if new_id_dir already exists
                shutil.rmtree(old_id_dir)
        
        
        subdir_names = [d for d in os.listdir(new_id_dir) if os.path.isdir(os.path.join(new_id_dir, d))]
        
        for subdir_name in subdir_names:
            subdir_path = os.path.join(new_id_dir, subdir_name)
            m4a_to_wav(subdir_path, new_id_dir)
            
            for root, dirs, files in os.walk(subdir_path):
                for file in files:
                    if file.endswith('.m4a'):
                        os.remove(os.path.join(root, file))
        for subdir_name in subdir_names:
            subdir_path = os.path.join(new_id_dir, subdir_name)
            shutil.rmtree(subdir_path)

# Usage
# process_voxceleb('/path/to/voxceleb/dataset')

# Usage
process_voxceleb('/home/data/panjianan/Vox-Celeb/')
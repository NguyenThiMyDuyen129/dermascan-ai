import os
import shutil

def main():
    # Construct paths using environment variables to keep it clean and robust
    userprofile = os.environ.get('USERPROFILE', '')
    if not userprofile:
        print("USERPROFILE environment variable not found.")
        return
        
    src_dir = os.path.join(userprofile, '.gemini', 'antigravity', 'brain', 'a49aed53-4fd1-4f0c-bf45-44bb2ae5c200')
    dest_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', 'assets'))
    
    os.makedirs(dest_dir, exist_ok=True)
    
    files_to_copy = {
        'media__1784291843973.png': 'demo_multi_lesions.png',
        'media__1784291967373.png': 'demo_single_lesion.png'
    }
    
    for src_name, dest_name in files_to_copy.items():
        src_path = os.path.join(src_dir, src_name)
        dest_path = os.path.join(dest_dir, dest_name)
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            print(f"Successfully copied {src_name} -> {dest_name}")
        else:
            print(f"Source file not found: {src_path}")

if __name__ == '__main__':
    main()

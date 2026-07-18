import os
import shutil

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    weights_dir = os.path.join(base_dir, 'backend', 'weights')
    
    print("=== WORKSPACE PREPARATION & CLEANUP ===")
    
    # 1. Copy screenshots from Gemini Brain to docs/assets
    userprofile = os.environ.get('USERPROFILE', '')
    if userprofile:
        src_dir = os.path.join(userprofile, '.gemini', 'antigravity', 'brain', 'a49aed53-4fd1-4f0c-bf45-44bb2ae5c200')
        dest_dir = os.path.join(base_dir, 'docs', 'assets')
        os.makedirs(dest_dir, exist_ok=True)
        
        files_to_copy = {
            'media__1784291843973.png': 'demo_multi_lesions.png',
            'media__1784291967373.png': 'demo_single_lesion.png'
        }
        
        for src_name, dest_name in files_to_copy.items():
            src_path = os.path.join(src_dir, src_name)
            dest_path = os.path.join(dest_dir, dest_name)
            if os.path.exists(src_path):
                try:
                    shutil.copy2(src_path, dest_path)
                    print(f"[OK] Copied screenshot asset: {dest_name}")
                except Exception as e:
                    print(f"[ERR] Error copying {src_name}: {e}")
            else:
                print(f"[WARN] Screenshot source not found: {src_path}")
    else:
        print("[WARN] USERPROFILE not found, skipping asset copying.")

    # 2. Paths of old weights to delete
    old_yolo = os.path.join(weights_dir, 'yolo_best.pt')
    old_densenet = os.path.join(weights_dir, 'best_densenet.pth')
    
    # 3. Paths of new weights to rename
    new_yolo = os.path.join(weights_dir, 'yolo_best_v2.pt')
    new_densenet = os.path.join(weights_dir, 'best_densenet_v2.pth')
    
    # Delete old files
    for path in [old_yolo, old_densenet]:
        if os.path.exists(path):
            try:
                os.remove(path)
                print(f"[OK] Deleted old weight: {os.path.basename(path)}")
            except Exception as e:
                print(f"[ERR] Error deleting {path}: {e}")
                
    # Rename V2 files to standard names
    if os.path.exists(new_yolo):
        try:
            os.rename(new_yolo, old_yolo)
            print(f"[OK] Renamed V2 YOLO: yolo_best_v2.pt -> yolo_best.pt")
        except Exception as e:
            print(f"[ERR] Error renaming yolo weight: {e}")
            
    if os.path.exists(new_densenet):
        try:
            os.rename(new_densenet, old_densenet)
            print(f"[OK] Renamed V2 DenseNet: best_densenet_v2.pth -> best_densenet.pth")
        except Exception as e:
            print(f"[ERR] Error renaming densenet weight: {e}")
            
    # 4. Clean up unzipped folders in the root
    folders_to_delete = ['best_densenet_v2', 'yolo_best_v2']
    for folder in folders_to_delete:
        folder_path = os.path.join(base_dir, folder)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            try:
                shutil.rmtree(folder_path)
                print(f"[OK] Cleaned up folder: {folder}")
            except Exception as e:
                print(f"[ERR] Error deleting folder {folder}: {e}")
                
    # 5. Clean up temporary test images in the root
    images_to_delete = ['input_cropped.jpg', 'input_cropped_large_lesion.jpg']
    for img in images_to_delete:
        img_path = os.path.join(base_dir, img)
        if os.path.exists(img_path):
            try:
                os.remove(img_path)
                print(f"[OK] Deleted temp image: {img}")
            except Exception as e:
                print(f"[ERR] Error deleting image {img}: {e}")

    # Remove temporary scripts if they exist
    for script in ['copy_assets.py', 'cleanup_weights.py']:
        script_path = os.path.join(os.path.dirname(__file__), script)
        if os.path.exists(script_path):
            try:
                os.remove(script_path)
            except Exception:
                pass
                
    print("=== WORKSPACE PREPARATION COMPLETED ===")

if __name__ == '__main__':
    main()

import os
import shutil

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    weights_dir = os.path.join(base_dir, 'backend', 'weights')
    
    # 1. Paths of old weights to delete
    old_yolo = os.path.join(weights_dir, 'yolo_best.pt')
    old_densenet = os.path.join(weights_dir, 'best_densenet.pth')
    
    # 2. Paths of new weights to rename
    new_yolo = os.path.join(weights_dir, 'yolo_best_v2.pt')
    new_densenet = os.path.join(weights_dir, 'best_densenet_v2.pth')
    
    # Delete old files
    for path in [old_yolo, old_densenet]:
        if os.path.exists(path):
            try:
                os.remove(path)
                print(f"Deleted old weight: {os.path.basename(path)}")
            except Exception as e:
                print(f"Error deleting {path}: {e}")
                
    # Rename V2 files to standard names
    if os.path.exists(new_yolo):
        try:
            os.rename(new_yolo, old_yolo)
            print(f"Renamed: yolo_best_v2.pt -> yolo_best.pt")
        except Exception as e:
            print(f"Error renaming yolo weight: {e}")
            
    if os.path.exists(new_densenet):
        try:
            os.rename(new_densenet, old_densenet)
            print(f"Renamed: best_densenet_v2.pth -> best_densenet.pth")
        except Exception as e:
            print(f"Error renaming densenet weight: {e}")
            
    # 3. Clean up unzipped folders in the root
    folders_to_delete = ['best_densenet_v2', 'yolo_best_v2']
    for folder in folders_to_delete:
        folder_path = os.path.join(base_dir, folder)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            try:
                shutil.rmtree(folder_path)
                print(f"Deleted folder: {folder}")
            except Exception as e:
                print(f"Error deleting folder {folder}: {e}")
                
    # 4. Clean up temporary test images in the root
    images_to_delete = ['input_cropped.jpg', 'input_cropped_large_lesion.jpg']
    for img in images_to_delete:
        img_path = os.path.join(base_dir, img)
        if os.path.exists(img_path):
            try:
                os.remove(img_path)
                print(f"Deleted temp image: {img}")
            except Exception as e:
                print(f"Error deleting image {img}: {e}")

if __name__ == '__main__':
    main()

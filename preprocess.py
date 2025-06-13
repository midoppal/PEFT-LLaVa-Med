import os
import random
import shutil
import csv
from PIL import Image

# === CONFIGURATION ===
label_dirs = {
    'No Finding': 'no_finding_images',
    'Pneumothorax': 'pneumothorax_images',
    'Cardiomegaly': 'cardiomegaly_images',
    'Infiltration': 'infiltration_images',
    'Effusion': 'effusion_images',
    'Emphysema': 'emphysema_images',
    'Atelectasis': 'atelectasis_images'
}
label_to_int = {label: idx for idx, label in enumerate(label_dirs.keys())}

output_root = 'preprocessed_pneumothorax_open_classification'
splits = ['train', 'val', 'test']
split_ratios = [0.7, 0.15, 0.15]
image_size = (336, 336)

# === SETUP OUTPUT DIRS ===
for split in splits:
    os.makedirs(os.path.join(output_root, split), exist_ok=True)

# === LOAD AND SHUFFLE FILES ===
def split_data(file_list):
    random.shuffle(file_list)
    total = len(file_list)
    train_end = int(total * split_ratios[0])
    val_end = train_end + int(total * split_ratios[1])
    return {
        'train': file_list[:train_end],
        'val': file_list[train_end:val_end],
        'test': file_list[val_end:]
    }

split_files = {}
for label, dir_path in label_dirs.items():
    files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.lower().endswith('.png')]
    split_files[label] = split_data(files)

# === PREPROCESS AND SAVE ===
for split in splits:
    label_file = os.path.join(output_root, f'{split}.csv')
    with open(label_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['filename', 'label'])

        for label, files_by_split in split_files.items():
            label_id = label_to_int[label]
            for src_path in files_by_split[split]:
                try:
                    img = Image.open(src_path).convert("RGB")
                    img = img.resize(image_size)

                    filename = os.path.basename(src_path)
                    dst_path = os.path.join(output_root, split, filename)
                    img.save(dst_path)

                    writer.writerow([filename, label_id])
                except Exception as e:
                    print(f"Failed to process {src_path}: {e}")

print("✅ Done. Images split, resized, and labeled.")

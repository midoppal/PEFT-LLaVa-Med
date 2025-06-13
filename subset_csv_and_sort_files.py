import os
import csv
import shutil

# === USER CONFIGURATION ===
csv_file = 'Data_Entry_2017_v2020.csv'  # Update this to your CSV file
image_root_dir = 'lung_dataset'  # Top-level directory containing subfolders of PNGs
max_no_finding = 2000

# === DISEASE LABELS TO EXTRACT ===
target_labels = [
    'Cardiomegaly',
    'Infiltration',
    'Effusion',
    'Emphysema',
    'Atelectasis',
    'No Finding',
    'Pneumothorax'
]

# === OUTPUT DIR SETUP ===
output_dirs = {label: f"{label.lower().replace(' ', '_')}_images" for label in target_labels}
for dir_path in output_dirs.values():
    os.makedirs(dir_path, exist_ok=True)

# === LOAD CSV MAPPINGS ===
label_to_filenames = {label: [] for label in target_labels}

with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        label = row['Finding Labels'].strip()
        filename = row['Image Index'].strip()

        # Match exact labels only (i.e., not "Pneumothorax|Emphysema")
        if label in target_labels:
            if label == 'No Finding':
                if len(label_to_filenames['No Finding']) < max_no_finding:
                    label_to_filenames['No Finding'].append(filename)
            else:
                label_to_filenames[label].append(filename)

# === HELPER FUNCTION TO FIND AND MOVE FILE ===
def move_file(filename, target_dir):
    for root, _, files in os.walk(image_root_dir):
        if filename in files:
            src = os.path.join(root, filename)
            dst = os.path.join(target_dir, filename)
            shutil.move(src, dst)
            return True
    return False

# === MOVE FILES ===
for label, filenames in label_to_filenames.items():
    print(f"Moving {len(filenames)} files for label: {label}...")
    for file in filenames:
        found = move_file(file, output_dirs[label])
        if not found:
            print(f"  [WARNING] Could not find: {file}")

print("Done.")

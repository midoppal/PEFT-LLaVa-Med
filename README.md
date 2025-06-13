## Download Dataset
https://nihcc.app.box.com/v/ChestXray-NIHCC

## Preprocess 
Subset the csv and sorts files into categories; may need to change folder/file names in code.
Determine which classes by deleting labels 

Run: ```subset_csv_and_sort_files.py```

Preprocess code into train/val/test

Run: ```preprocess.py```

## Binary Classifier
Run on google colab, change file/folder names accordingly

Run: ```CSE244C_Final_Project_LoRA_Bitfit.ipynb```

## Multi-Class Classifier
Run on google colab, change file/folder names accordingly

Run: ```CSE244C_Final_Project_Open_Classification.ipynb```

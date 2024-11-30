#%%
from pathlib import Path
import os
import shutil

directory_path = Path("/cns/share/Vincent/McHugh_lab/CA2Cre_DREADD/")
excluded_folder = directory_path / "renamed_ntt_files"
file_extension = ".ntt"  # Change this to your desired file extension

# Use Path.rglob to find files of the specified type
ntt_files = list(directory_path.rglob(f"*{file_extension}"))

ntt_files = [str(f) for f in ntt_files if "_all" not in str(f) and not str(f).startswith(str(excluded_folder))] # a list of all available .ntt filepaths, except for the ones marked "_all"

ntt_tetrode_keys = { # which tetrode is in which area. list position corresponds to tetrode number
    "144": [None, "CA1", "CA2", None, None, "CA1", "CA1", None, "CA2"],
    "161": [None, "CA1", None, "CA1", "CA2", "CA1", "CA1", "CA1", "CA1"],
    "248": [None, "CA2", None, "CA1", "CA1", "CA1", "CA1", "CA1", "CA1"],
    "368": [None, "CA1", "CA1", "CA2", "CA3", "CA1", "CA1", "CA1", "CA1", ],
    "550": [None, "CA1", "CA1", "CA2", None, "CA1", "DEEP", None, None],
    "556": [None, "CA2", "CA1", "CA2", "DEEP", "CA2", "CA2-CA1", "CA1", "CA1"],
    "572": [None, None, "CA3-CA2", "CA1", "DEEP", None, None, "CA2", "CA2"],
    "1216": [None, "CA2", "CA3a", "CA3c", "CA1", "CA2", "CA1", "CA3c", "CA1"],
    "1223": [None, None, "CA3a", "CA3b", "CA1", "CA3a", "CA2", "CA3b", "CA1"],
    "1232": [None, None, "CA1", "CA3b", "CA3a", "CA1", "CA13b", "CA2", None]
    }


ntt_files_new = []
# create clear filenames
for filepath in ntt_files:
    animal_info = filepath.split("/")[6:]
    
    animal_nr = animal_info[0].split("_")[1] # extract animal name from filepath. Can remain string
    day = animal_info[1].split("_")[1]
    task, state = animal_info[2].split("_")
    
    tetrode_nr = int(animal_info[3][2])
    
    area = ntt_tetrode_keys[animal_nr][tetrode_nr]
    if not area:
        continue
    
    new_filename = f"model{animal_nr}_d{day}_{task}_tt{tetrode_nr}_{area}_{state}.ntt"
    ntt_files_new.append([filepath, new_filename])


# copy them to common directory

destination_folder = "/cns/share/Vincent/McHugh_lab/CA2Cre_DREADD/renamed_ntt_files/"
destination_folder_list = os.listdir("/cns/share/Vincent/McHugh_lab/CA2Cre_DREADD/renamed_ntt_files/")

# Loop through the file list and rename/copy files
for sublist in ntt_files_new:
    original_path, new_filename = sublist
    if new_filename in destination_folder_list:
        continue
    
    # Construct the destination path
    destination_path = os.path.join(destination_folder, new_filename)
    
    # Copy the file to the destination with the new name
    shutil.copy2(original_path, destination_path)
    print(new_filename)

print("File renaming and copying complete.")



# %%

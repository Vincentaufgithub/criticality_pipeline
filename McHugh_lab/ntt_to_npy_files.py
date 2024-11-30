# This file is used to read all ntt files (in one folder),
# convert them into npy-files and save them into another folder.
# I had to do this one on my private PC because there issues with matlabengine on our lab computers
# so adjust the filepaths accordingly.


# %%

import matlab.engine
import os
import numpy as np

directory_path = "C:/Users/User/Documents/Arbeit/McHugh/renamed_ntt_files"
ntt_files = os.listdir(directory_path)

goal_directory = "C:/Users/User/Documents/Arbeit/McHugh/extracted_spike_trains"

# Start the MATLAB engine
eng = matlab.engine.start_matlab()
# Add the path to the Neuralynx Matlab ImportExport toolbox
eng.addpath("C:/Users/User/Documents/Arbeit/McHugh/MatlabImportExport_v6.0.0", nargout=0)

for file in ntt_files:
    try:
        print("reading", file)
        ntt_file_path = f"{directory_path}/{file}"
        
        
        # Convert FieldSelectionFlags to MATLAB's double array format
        FieldSelectionFlags = matlab.double([1, 1, 1, 1, 1])  # This is essential for proper argument passing

        # Set HeaderExtractionFlag as a double (1 to extract header)
        HeaderExtractionFlag = matlab.double([1])

        # Use ExtractionMode 1 (Extract All Records)
        ExtractionMode = matlab.double([1])

        # Empty ExtractionModeVector as it's not needed for ExtractionMode 1 (set it as an empty matrix)
        ExtractionModeVector = matlab.double([])

        # Call the Nlx2MatSpike function

        timestamps_mat, ScNumbers, CellNumbers, Features, Samples, Header = eng.Nlx2MatSpike(
            ntt_file_path,
            FieldSelectionFlags,
            HeaderExtractionFlag,
            ExtractionMode,
            ExtractionModeVector,
            nargout=6
            )

        # Convert the MATLAB arrays to NumPy arrays
        timestamps = np.array(timestamps_mat)[0]
        np.save(f"{goal_directory}/{file[:-4]}.npy", timestamps)
        
        # would like to avoid this, but takes up too much space
        os.remove(ntt_file_path)
    
    except Exception as e:
        print(file, e)
        with open("C:/Users/User/Documents/Arbeit/McHugh/failed_unpack.txt", 'a') as f:
            f.write(f"{file}: {e}\n")
        continue

eng.quit()


# %%


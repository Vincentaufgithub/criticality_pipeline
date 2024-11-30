# %%

import numpy as np
import tools
import os
from McHugh_lab.find_ntt_files import ntt_files



directory = '181-1223/181-1232/DAY07_2016-09-01_12-02-01/'


all_files = [f for f in os.listdir("/cns/share/Vincent/McHugh_lab/analysis_results/numpy_spike_trains/")]
raw_data_directory = "/cns/share/Vincent/McHugh_lab/CA2Cre_DREADD/"

# Start the MATLAB engine
eng = matlab.engine.start_matlab()

# Add the path to the Neuralynx Matlab ImportExport toolbox
eng.addpath('/home/dekorvyb/Documents/criticality_pipeline/MatlabImportExport_v6.0.0', nargout=0)


#################################################
all_files = []

tetrode_files = {
# day 16
        # sleep1
        
    "144_D16_sleep1_CA1_1_pre": "144/DAY16_2014-05-29_10-40-02/02_Sleep1/TT1.ntt",
    "144_D16_sleep1_CA2_1_pre": "144/DAY16_2014-05-29_10-40-02/02_Sleep1/TT2.ntt",
    "144_D16_sleep1_CA1_2_pre": "144/DAY16_2014-05-29_10-40-02/02_Sleep1/TT5.ntt",
    "144_D16_sleep1_CA1_3_pre": "144/DAY16_2014-05-29_10-40-02/02_Sleep1/TT6.ntt",
    "144_D16_sleep1_CA2_2_pre": "144/DAY16_2014-05-29_10-40-02/02_Sleep1/TT8.ntt",
        # BoxA
    "144_D16_boxA_CA1_1_pre": "144/DAY16_2014-05-29_10-40-02/04_BoxA/TT1.ntt",
    "144_D16_boxA_CA2_1_pre": "144/DAY16_2014-05-29_10-40-02/04_BoxA/TT2.ntt",
    "144_D16_boxA_CA1_2_pre": "144/DAY16_2014-05-29_10-40-02/04_BoxA/TT5.ntt",
    "144_D16_boxA_CA1_3_pre": "144/DAY16_2014-05-29_10-40-02/04_BoxA/TT6.ntt",
    "144_D16_boxA_CA2_2_pre": "144/DAY16_2014-05-29_10-40-02/04_BoxA/TT8.ntt",
        #sleep2
    "144_D16_sleep2_CA1_1_pre": "144/DAY16_2014-05-29_10-40-02/06_Sleep2/TT1.ntt",
    "144_D16_sleep2_CA2_1_pre": "144/DAY16_2014-05-29_10-40-02/06_Sleep2/TT2.ntt",
    "144_D16_sleep2_CA1_2_pre": "144/DAY16_2014-05-29_10-40-02/06_Sleep2/TT5.ntt",
    "144_D16_sleep2_CA1_3_pre": "144/DAY16_2014-05-29_10-40-02/06_Sleep2/TT6.ntt",
    "144_D16_sleep2_CA2_2_pre": "144/DAY16_2014-05-29_10-40-02/06_Sleep2/TT8.ntt",
        # boxC
    "144_D16_boxC_CA1_1_post": "144/DAY16_2014-05-29_10-40-02/10_BoxC/TT1.ntt",
    "144_D16_boxC_CA2_1_post": "144/DAY16_2014-05-29_10-40-02/10_BoxC/TT2.ntt",
    "144_D16_boxC_CA1_2_post": "144/DAY16_2014-05-29_10-40-02/10_BoxC/TT5.ntt",
    "144_D16_boxC_CA1_3_post": "144/DAY16_2014-05-29_10-40-02/10_BoxC/TT6.ntt",
    "144_D16_boxC_CA2_2_post": "144/DAY16_2014-05-29_10-40-02/10_BoxC/TT8.ntt",
        # sleep 4
    "144_D16_sleep4_CA1_1_post": "144/DAY16_2014-05-29_10-40-02/12_Sleep4/TT1.ntt",
    "144_D16_sleep4_CA2_1_post": "144/DAY16_2014-05-29_10-40-02/12_Sleep4/TT2.ntt",
    "144_D16_sleep4_CA1_2_post": "144/DAY16_2014-05-29_10-40-02/12_Sleep4/TT5.ntt",
    "144_D16_sleep4_CA1_3_post": "144/DAY16_2014-05-29_10-40-02/12_Sleep4/TT6.ntt",
    "144_D16_sleep4_CA2_2_post": "144/DAY16_2014-05-29_10-40-02/12_Sleep4/TT8.ntt",
        # Box A2
    "144_D16_boxA2_CA1_1_post": "144/DAY16_2014-05-29_10-40-02/14_BoxA2/TT1.ntt",
    "144_D16_boxA2_CA2_1_post": "144/DAY16_2014-05-29_10-40-02/14_BoxA2/TT2.ntt",
    "144_D16_boxA2_CA1_2_post": "144/DAY16_2014-05-29_10-40-02/14_BoxA2/TT5.ntt",
    "144_D16_boxA2_CA1_3_post": "144/DAY16_2014-05-29_10-40-02/14_BoxA2/TT6.ntt",
    "144_D16_boxA2_CA2_2_post": "144/DAY16_2014-05-29_10-40-02/14_BoxA2/TT8.ntt",
        # sleep 5
    "144_D16_sleep5_CA1_1_post": "144/DAY16_2014-05-29_10-40-02/16_Sleep5/TT1.ntt",
    "144_D16_sleep5_CA2_1_post": "144/DAY16_2014-05-29_10-40-02/16_Sleep5TT2.ntt",
    "144_D16_sleep5_CA1_2_post": "144/DAY16_2014-05-29_10-40-02/16_Sleep5TT5.ntt",
    "144_D16_sleep5_CA1_3_post": "144/DAY16_2014-05-29_10-40-02/16_Sleep5TT6.ntt",
    "144_D16_sleep5_CA2_2_post": "144/DAY16_2014-05-29_10-40-02/16_Sleep5TT8.ntt"
        
    }
        
        
for tetrode in tetrode_dictionary.keys():
    
    if f'{tetrode}.npy' in all_files:
        continue
    
    try:
        file_path = f'{raw_data_directory}{tetrode_files[tetrode]}'
        print("ANALYSING", tetrode)

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
                file_path,
                FieldSelectionFlags,
                HeaderExtractionFlag,
                ExtractionMode,
                ExtractionModeVector,
                nargout=6
            )

        # Convert the MATLAB arrays to NumPy arrays
        timestamps = np.array(timestamps_mat)[0]
        print("extracted spike train")
        
        binned = tools.bin_timestamps(timestamps, unit = "us") # data unit according to https://neuralynx.com/_software/NeuralynxDataFileFormats.pdf
        # np.save(f'/cns/share/Vincent/McHugh_lab/analysis_results/test/{tetrode}', binned)
        print("binned and saved")
        # print(binned, len(binned), max(binned))
        
        
        tools.mr_estimator_for_prepared_epoch_data(binned, window_size = 90, bin_size = 5, filename = f'/cns/share/Vincent/McHugh_lab/analysis_results/test/{tetrode}', fit_func = "f_complex")
        
    except Exception as e:
        with open('/cns/share/Vincent/McHugh_lab/analysis_results/failed_analysis.txt', 'a') as f:
            f.write(f"{tetrode}\n")
        continue
        
eng.quit()



# %%
####################################
# Create linear Model
####################################

import os
import pandas as pd
import statsmodels.formula.api as smf

filepath = "/cns/share/Vincent/McHugh_lab/analysis_results/test/"
results = [f for f in os.listdir(filepath)]

big_df = []

for result in results:
    try:
        # Create a new DataFrame for each result file
        df = pd.DataFrame()

        # Extract the area (e.g., "CA1") from the filename
        area = result.split("_")[3] 
        state = result.split("_")[2][:-1]
        cno = result.split("_")[-1][:-11]

        # Read the "beta" column from the parquet file
        tau = pd.read_parquet(f"{filepath}{result}")["tau"].values[0]
        
        file_data = {
                    "tau": tau,
                    "area": str(area),
                    "state": str(state),
                    "cno": str(cno)
                }
        big_df.append(file_data)
        
    except:
        continue
    
    '''
    df["tau"] = tau
    
    # Add the 'area' as a new column
    df["area"] = str(area)

    print(df)
    # Append this DataFrame to the list
    big_df.append(df)
    '''
    
combined_df = pd.DataFrame(big_df)
    
combined_df = combined_df.dropna()
print(combined_df)

formula = "tau ~ area * state * cno"

# Fit the linear model using Ordinary Least Squares (OLS)
model = smf.ols(formula=formula, data=combined_df).fit()

# Print the summary of the model
print(model.summary())

# %%
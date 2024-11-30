# %%
import numpy as np
import sys
sys.path.append("/home/dekorvyb/Documents/criticality_pipeline/")

import os
import tools


npy_directory = '/cns/share/Vincent/McHugh_lab/CA2Cre_DREADD/extracted_spike_trains/'
npy_files =[f.split(".")[0] for f in os.listdir(npy_directory)]

result_directory = '/cns/share/Vincent/McHugh_lab/CA2Cre_DREADD/loren_frank_results/'
result_files = [f.split(".")[0] for f in os.listdir(result_directory)]


        
for tetrode in npy_files:
    
    if tetrode in result_files:
        continue
    
    try:
        file_path = f'{npy_directory}{tetrode}.npy'
        print("ANALYSING", tetrode)

        timestamps = np.load(file_path)
        binned = tools.bin_timestamps(timestamps, unit = "us") # data unit according to https://neuralynx.com/_software/NeuralynxDataFileFormats.pdf
        # np.save(f'/cns/share/Vincent/McHugh_lab/analysis_results/test/{tetrode}', binned)
        
        
        tools.mr_estimator_for_numpy(binned, window_size = 90, bin_size = 5, filename = f'{result_directory}/{tetrode}', fit_func = "f_complex")
        
    except Exception as e:
        with open('/cns/share/Vincent/McHugh_lab/CA2Cre_DREADD/loren_frank_results/failed_analysis.txt', 'a') as f:
            f.write(f"{tetrode}: {e}\n")
        continue

# %%

'''
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
    
    
    df["tau"] = tau
    
    # Add the 'area' as a new column
    df["area"] = str(area)

    print(df)
    # Append this DataFrame to the list
    big_df.append(df)
    
    
combined_df = pd.DataFrame(big_df)
    
combined_df = combined_df.dropna()
print(combined_df)

formula = "tau ~ area * state * cno"

# Fit the linear model using Ordinary Least Squares (OLS)
model = smf.ols(formula=formula, data=combined_df).fit()

# Print the summary of the model
print(model.summary())

# %%


'''
# %%

import pandas as pd
import os
from statsmodels.regression.mixed_linear_model import MixedLM


criticality_dict = '/cns/share/Vincent/McHugh_lab/CA2Cre_DREADD/loren_frank_results/'
files = [f for f in os.listdir(criticality_dict) if f.endswith(".parquet")]

all_data = []


for filename in files:
    filename_split = filename.split('_') # with filename pattern being:  "animal name _ experimental day _ task _ tetrode nr. _ brain area _ pre or post treatment _ timechunk .parquet"
    
    df = pd.read_parquet(f'{criticality_dict}/{filename}')
    df['tau'] = df['tau'][0]
    
    df['animal'] = filename_split[0]
    df['day'] = filename_split [1]
    df ['task'] = filename_split[2]
    df['tetrode'] = filename_split[3]
    df['area'] = filename_split[4]
    df['treatment'] = filename_split[5]
    df['timechunk'] = int(filename_split[6].split('.')[0])
    all_data.append(df)


# Combine all data
df = pd.concat(all_data, ignore_index=True)
print('combined all data')
# 2. Prepare Data
# Convert categorical variables
df['area'] = df['area'].astype('category')
df['treatment'] = df['treatment'].astype('category')
df['animal'] = df['animal'].astype('category')

print("fitting model")
# 3. Fit the LME Model
# Formula: tau ~ treatment * area + (1|animal)
model = MixedLM.from_formula("tau ~ treatment * area", groups="animal", data=df)
result = model.fit()

# 4. Summarize Results
print(result.summary())


# %%
# %%

import os
import pandas as pd
import numpy as np
from allensdk.brain_observatory.ecephys.ecephys_project_cache import EcephysProjectCache
import logging



# Function to download data for each session using wget
def download_session_data(session_id):
    try:
        session_dir = os.path.join(output_dir, f"session_{session_id}")
        if not os.path.exists(session_dir):
            os.makedirs(session_dir)

        # Download only the required data
        session = cache.get_session_data(session_id)
        logging.info(f"Successfully downloaded data for session {session_id}")

    except Exception as e:
        logging.error(f"Error downloading data for session {session_id}: {e}")
        
        
        

# Setup logging
logging.basicConfig(filename='download_log.txt', level=logging.INFO, format='%(asctime)s %(message)s')

# Directory to save downloaded data
output_dir = '/local2/Vincent/neuro_pixels_sessions/'

# Manifest file
manifest_path = os.path.join(output_dir, "manifest.json")

# Create cache object
cache = EcephysProjectCache.from_warehouse(manifest=manifest_path)

# Get list of sessions
sessions = cache.get_session_table()

# Filter sessions based on your criteria
filtered_sessions = sessions[
    (sessions.ecephys_structure_acronyms.apply(lambda acronyms: any(area in acronyms for area in ['CA1', 'CA3', 'DG', 'SUB', 'ProS'])))]

# Loop through filtered sessions and download data
for session_id in filtered_sessions.index.values:
    download_session_data(session_id)

print("All downloads attempted. Check download_log.txt for details.")


# %%
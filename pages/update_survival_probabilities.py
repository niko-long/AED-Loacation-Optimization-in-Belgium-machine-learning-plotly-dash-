import joblib
import dash_leaflet as dl
import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree
from geopy.distance import geodesic
from aed_location_existed import read_patient_data, read_aed_data

# Load the saved model pipeline
model = joblib.load('model/aed_survival_pipeline.pkl')

def update_distance_to_aed(patients_df, aed_locations):
    """
    Update the distance from patients to the nearest AED
    """
    if not aed_locations:
        # If aed_locations is empty, return the original patients_df
        patients_df['distance_to_aed'] = np.nan
        return patients_df
    
    # Create a BallTree to calculate distances
    aed_coords = np.radians(aed_locations)
    tree_aed = BallTree(aed_coords, metric='haversine')
    patient_coords = np.radians(patients_df[['latitude', 'longitude']])
    
    distances_aed, indices_aed = tree_aed.query(patient_coords, k=1)
    distances_aed = distances_aed * 6371  # Convert to kilometers
    
    patients_df['distance_to_aed'] = distances_aed
    return patients_df

def update_patient_survival_probabilities(patients_df, model):
    """
    Calculate the survival probability for all patients
    """
    # Extract relevant patient data
    key_cols = ['Postal_code', 'latitude', 'longitude', 'EventLevel Trip', 
                'distance_to_center', 'distance_to_aed', 'time']
    X = patients_df[key_cols]
    print('Computing the new survival probability...')
    non_survival_probabilities = model.predict_proba(X)[:, 0]  # Get the probability of non-survival
    print('Computed.')

    # Update the DataFrame with survival probabilities
    patients_df['Non_Survival_Probability'] = non_survival_probabilities

    return patients_df

def generate_patient_tooltips_with_probability(patients_df):
    tooltips = []
    for _, row in patients_df.iterrows():
        popup_text = f"{row['Non_Survival_Probability']:.2f}"
        tooltip = dl.Tooltip(popup_text, permanent=True, direction="right")
        tooltips.append((row['latitude'], row['longitude'], tooltip))
    return tooltips

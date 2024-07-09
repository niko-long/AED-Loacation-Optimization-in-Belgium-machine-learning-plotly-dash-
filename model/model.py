import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
import joblib
import datetime
import time

intervention = pd.read_excel('data/intervention_all.xlsx')

# Parse date-time string
def parse_datetime(x):
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f%z", "%Y-%m-%d %H:%M:%S.%f"):
        try:
            return datetime.datetime.strptime(x, fmt)
        except ValueError:
            continue
    raise ValueError(f"Time data '{x}' does not match any known format")

intervention['T0'] = intervention['T0'].astype("string")
intervention['T0'] = intervention['T0'].str[:26]
intervention['T0'] = intervention['T0'].apply(parse_datetime)
intervention['time'] = intervention['T0'].apply(lambda x: x.time())
intervention['Mortality'] = intervention.apply(lambda row: 1 if row['Abandon reason']=='Overleden' else 0, axis=1)

key_col = ['Mission ID','PostalCode permanence', 'Latitude intervention', 'Longitude intervention', 
           'EventLevel Trip', 'time', 'T3-T0 in Minutes', 'Mortality']
inter = intervention[key_col]

# Rename columns
inter.rename(columns={'PostalCode permanence': 'Postal_code',
                      'Latitude intervention': 'latitude',
                      'Longitude intervention': 'longitude'}, inplace=True)

import pandas as pd
from geopy.distance import geodesic
from sklearn.neighbors import BallTree
import numpy as np
import googlemaps

# Use your Google Maps API key
api_key = 'AIzaSyAaMgtqAAp07HTqibk9KlYkHIfHYK2sutc'
gmaps = googlemaps.Client(key=api_key)

patients = inter.copy()
hospitals = pd.read_excel('data/hospitals.xlsx')
aed_all = pd.read_excel('data/AED_locations.xlsx')
aed_data = aed_all[['id', 'full_address', 'latitude', 'longitude', 'public']]
aed_data.dropna(axis = 0, inplace = True)
public_aed = aed_data[aed_data['public'] == 'yes']

# Ensure index continuity
patients.reset_index(drop=True, inplace=True)

# Calculate straight-line distance to emergency centers
centers_coords = np.radians(hospitals[['latitude', 'longitude']])
tree_centers = BallTree(centers_coords, metric='haversine')
patients_coords = np.radians(patients[['latitude', 'longitude']])
distances_centers, indices_centers = tree_centers.query(patients_coords, k=5)

# Calculate straight-line distance to AED
aed_coords = np.radians(public_aed[['latitude', 'longitude']])
tree_aed = BallTree(aed_coords, metric='haversine')
distances_aed, indices_aed = tree_aed.query(patients_coords, k=1)

# Define a function to calculate walking distance
def get_walking_distance(patient_location, center_location):
    try:
        result = gmaps.distance_matrix(origins=[patient_location],
                                       destinations=[center_location],
                                       mode="walking")
        if result['rows'][0]['elements'][0]['status'] == 'OK':
            distance = result['rows'][0]['elements'][0]['distance']['value']  # Distance in meters
            return distance
        else:
            print(f"Error in Google Maps API response: {result['rows'][0]['elements'][0]['status']}")
            return float('inf')
    except Exception as e:
        print(f"Exception occurred: {e}")
        return float('inf')

# Calculate walking distance to nearest emergency center
def find_nearest_center(patient):
    patient_location = (patient['latitude'], patient['longitude'])
    patient_index = patient.name  # Use index instead of name
    
    # Calculate walking distance to nearest emergency center
    nearest_centers = indices_centers[patient_index]  # Get indices of nearest emergency centers by straight-line distance
    walking_distances_centers = []
    for center_index in nearest_centers:
        center = hospitals.iloc[center_index]
        center_location = (center['latitude'], center['longitude'])
        distance = get_walking_distance(patient_location, center_location)
        walking_distances_centers.append((distance, center['full_address']))
    min_distance_center, nearest_center_name = min(walking_distances_centers, key=lambda x: x[0])
    
    return nearest_center_name, min_distance_center

# Calculate walking distance to nearest AED
def find_nearest_aed(patient):
    patient_location = (patient['latitude'], patient['longitude'])
    patient_index = patient.name  # Use index instead of name
    
    # Calculate walking distance to nearest AED
    nearest_aeds = indices_aed[patient_index]  # Get indices of nearest AEDs by straight-line distance
    aed_nearest = public_aed.iloc[nearest_aeds[0]]
    aed_location = (aed_nearest['latitude'], aed_nearest['longitude'])
    distance_aed = get_walking_distance(patient_location, aed_location)
    
    return aed_nearest['full_address'], distance_aed

# Calculate walking distance to nearest emergency center for each patient
results_centers = patients.apply(find_nearest_center, axis=1, result_type='expand')
patients['nearest_center_name'] = results_centers[0]
patients['distance_to_center'] = results_centers[1] / 1000  # Convert to kilometers

# Calculate walking distance to nearest AED for each patient
results_aeds = patients.apply(find_nearest_aed, axis=1, result_type='expand')
patients['nearest_aed_name'] = results_aeds[0]
patients['distance_to_aed'] = results_aeds[1] / 1000  # Convert to kilometers
patients.to_excel('data/patients.xlsx')

# Model
patients = pd.read_excel('data/patients.xlsx')
# Convert event type and time features to appropriate format
patients['time'] = patients['time'].str[:8]
patients['time'] = pd.to_datetime(patients['time'], format='%H:%M:%S').dt.hour
patients.to_excel('data/patients.xlsx')

# Select features and labels
key_cols = ['Postal_code', 'latitude', 'longitude', 'EventLevel Trip', 
            'distance_to_center', 'distance_to_aed', 'time']
X = patients[key_cols]
y = patients['Mortality']

# Get all possible categories
postal_code_categories = sorted(X['Postal_code'].unique())
event_level_categories = sorted(X['EventLevel Trip'].unique())

# One-Hot encode categorical variables
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['latitude', 'longitude', 
                                   'distance_to_center', 'distance_to_aed', 'time']),
        ('cat', OneHotEncoder(categories=[postal_code_categories, event_level_categories], handle_unknown='ignore'), 
         ['Postal_code', 'EventLevel Trip'])
    ])

# XGBoost model
xgb = XGBClassifier(random_state=42)

# Hyperparameter grid
param_grid = {
    'n_estimators': [200],
    'max_depth': [3, 4, 5, 6],
    'learning_rate': [0.01, 0.1, 0.2],
    'subsample': [1.0],
    'colsample_bytree': [1.0]
}

# Grid search
grid_search = GridSearchCV(
    estimator=xgb, param_grid=param_grid, 
    scoring='roc_auc', cv=10, verbose=2, n_jobs=-1  # Set cross-validation folds to 5
)

# Build model pipeline
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('grid_search', grid_search)
])

# Train model and perform cross-validation
model.fit(X, y)

# Save the entire model pipeline
joblib.dump(model, 'aed_survival_pipeline.pkl')

# Evaluate model
cv_results = grid_search.cv_results_
best_params = grid_search.best_params_
best_score = grid_search.best_score_

print(f'Best Parameters: {best_params}')
print(f'Best ROC AUC Score: {best_score}')

# AED Optimization Project for Modern Data Analytics Course
## Introduction
In this project, a machine learning model was built to predict survival rates for out-of-hospital cardiac arrest using intervention, hospital and AED information. Additionally, a web application was developed via Dash and Plotly to visualize the survival information with relation to locations of AEDs and hospitals, and to enable users to interactively add new AEDs to explore AED optimization possibilities.
# ——————————————————————
### Project Background
Seconds are critical to survivability of out-hospital Sudden Cardiac Arrest (SCA) patients since SCA typically causes death if proper care is not administered rapidly. Early defibrillation is key in the ‘Chain of Survival’ for treating these patients. This care can be provided by Automated External Defibrillators (AEDs), medical devices designed to provide cardiac defibrillation in out-of-hospital environments by bystanders with limited or no training.

Improved response time, or decreased time-to-shock, using public-access AEDs has shown improved survival rates. Rapid response times are achieved by making AEDs publicly available for bystander use. Public-access AED programs empower bystanders to provide early cardiac defibrillation providing rapid and open access to AEDs.

### Project Objectives
In this project, we aim to build a machine learning model to predict survival rates for out-of-hospital cardiac arrest using intervention, hospital, and AED information. Using Dash and Plotly, we also aim to develop a web application to visualize the survival information with relation to locations of AEDs and hospitals, and enable users to interactively add new AED for survival chance optimization.

# Pre-processing
We pre-process the dataset by the following steps:
- Since we are interested in the survival outcome of the patient at T3, we create a new variable ‘target’, with value 1 representing patients with abandon reasons of ‘Overleden (death in Dutch)’ or ‘Dood Ter Plaatse (death in French)’, and 0 otherwise.
- We filter patients with event types at vector trips of ‘P003 (Cardiac arrest)’ only, which is the most relevant event type with AED optimization.
- Meanwhile, we calculate the duration between T0 and T3 as an important feature.
- In our analysis, we extract and keep features including **Mission ID**, **PostalCode permanence**, **EventType Trip**, **EventLevel Trip**, **Latitude intervention**, **Longitude intervention**, **T3-T0 in Minutes**, **T0**, and **T3** in Intervention dataset, **id**, **full_address**, **latitude**, **longitude**, and **public** in AED dataset, and **latitude** and **longitude** in hospital dataset as relevant features for predicting survival rate at T3 and location visualization.
- We delete incorrect input values of postal code and duplicate observations, and convert incorrectly input coordinate values accordingly.
- We delete missing values in T3-T0 in minutes, Latitude intervention, Longitude intervention, EventType Trip, EventLevel trip, and PostalCode permanence.
- For the purpose of visualization, we only select observations of three cities including Brussels, Antwerp, and Liege.

# Feature engineering
When a cardiac patient has a heart attack, we think his chances of being saved are likely to increase if an AED is available or an emergency center is very close by. Therefore, in addition to region, latitude and longitude, disease class, and time of onset (an integer from 0 to 24), we introduce two innovative variables ‘distance to the nearest AED’ and ‘distance to the nearest hospital’.

In order to reduce the time complexity, we first calculate the coordinates of the five closest AEDs and hospitals in a straight line from each patient, then calculate the walking distance between these five locations and the patient, and finally choose the smallest value as the value of this variable.

Then, we use ‘One Hot Encoder’ to encode categorical variables (Postal Code and Event Level) to avoid the model misinterpreting these categories as ordinal variables.

We use ‘StandardScaler’ to standardize numerical features, ensuring they have equal influence in the model.

After doing the above steps, we save these new variable generation steps as pipeline models for future visualizations.

# Model Training
After Encoding, we get a total of 215 variables including category variables and continuous variables. In order to get a better model, we choose the XGBoost model training dataset with the combination of grid search and cross-validation, and the model reaches the optimum when the estimators are 200 and the maximum depth is 3.

Our final model has a best AUC Score of 0.613, indicating a moderate ability to discriminate. Figure \ref{fig:model} shows the top 10 feature importance of our model. Eventlevel Trip N5 has the highest importance, and the remaining 9 features are all postal codes.

Similarly, we save the trained model as a pipeline along with the previous encoding part for subsequent use.

# Application development
After the survival rate prediction model was built, we next develop an application to visualize the survival rate in relation to AED and hospital locations, and enable users to add new AEDs to increase the survival chances of current SCA patients. Besides, we also visualize the trend of survival rates of SCA patients in three cities, including Brussels, Antwerp, and Liege, as examples during the period between June 2022 and May 2023.

There are four pages in our web application:
## Project Main Page
The main page is a thumbnail of all the features of our app, with four sections in total. In the upper left section is the introduction of our project. In the upper right, lower left and upper right sections are our three interactive pages, namely "AED Optimization for Better Survival", "Mortality Rate Analysis by Different Cities and Month", and "Mortality Rate Analysis by Different Years and Cities".
By clicking the picture in the three section, we can directly go the interactive page. To go back the main page, we set a hamburger button in the top left corner. By clicking the hamburger button, we can choose any page out of the four pages you want to go.
![Project Main Page](Figures/mainpage.png)

## AED Optimization for Better Survival
In this page, we have four check boxes, enabling users to display "Existing AED Locations", "Patients", "Hospitals", and "New AED Placement", as shown in Figure \ref{fig:page1}. By click "Existing AED Locations", "Patients", and "Hospitals" boxes, users can see existing AED locations, patients, and hospitals information. Patients with green logo represent patients who survived at T3, while patients with red logo represent patients who died at T3. By clicking "New AED Placement" box, users can see current survival rate of existing patients. At the same time, users can interactively add new AED on the map by clicking on the map, the Latitude and Longitude information of the new AED location shows in the text box at right immediately, and the survival rates of existing patients update accordingly.

This part of the implementation relies on the previously stored pipeline, when the user clicks on a new AED location, the new latitude and longitude are automatically read and stored in a list called \text{stored\_coordinates}. The function that updates the survival rate automatically reads all the values within that list and passes them into the stored pipeline model to calculate the new survival rate result, which is finally displayed on the map.
![AED Optimization for Better Survival](Figures/page1.png)

## Mortality Rate Analysis Across Cities by Different Month
At this page, we show the mortality rate of three different cities at different period, and enable users to use slide bar to choose their interested months to see the mortality rate of SCA patients at three cities in that month as shown in Figure \ref{fig:page2}.
![Mortality Rate Analysis by Different Cities and Month](Figures/page2.png)

## Mortality Rate Analysis by Different Years and Cities
In this page, we show the trend of mortality rate of chosen city in a chosen year. The user can use the drop down to choose interested years and cities to see the mortality rate trend as shown below.
![Mortality Rate Analysis by Different Years and Cities](Figures/page3.png)

# Deployment
To access our app from public link, we deploy our app in Heroku. Since we have four pages in total, we need to deploy the three sub-pages and then update their URL in the main page so that the four pages can interactively switch to each others.
![Heroku Deployment](Figures/heroku.jpg)

Users can achieve our app via this link [https://mdamainpage-26dd5ba1b110.herokuapp.com](https://mdamainpage-26dd5ba1b110.herokuapp.com) or via the QR code below:
![Web APP QR Code](Figures/qr.jpg)

# Github Version Control
In our project, we use Github for version control and remote repository. Branch are used to allow different group member working on different part of app development separately. Requirement.txt and readme file are provided for user to successfully download and use our web app.
The github link is provide: [MDA Project](https://github.com/niko-long/MDA_Project2024_AED_Optimization) (https://github.com/niko-long/MDA_Project2024_AED_Optimization.git)
![Github](Figures/github.jpg)

# Further Discussion and Limitations
In our project,



# ————————————————————————




## Usage
The app has been deployed on Heroko, users can simply access the APP via the link below:

[https://mdamainpage-26dd5ba1b110.herokuapp.com](https://mdamainpage-26dd5ba1b110.herokuapp.com)

or via this QR code:

![QR Code](/pages/assets/heroku_app_qr.png)

## Repository Structure
```
MDA_Project2024_AED_Optimization/
├── data/                             # data files
├── preprocess/                       # pre-processing files
│   ├── preprocessing.ipynb
├── model/                            # prediction model files
│   ├── aed_survival_pipeline.pkl
│   ├── model.py
├── pages/                            # web application files
│   ├── main.py                       # source file for main page
│   ├── app7.py                       # source file for map page
│   ├── page1.py                      # source file for page 1
│   ├── page2.py                      # source file for page 2
│   ├── layout.py                     # source file for layout
│   ├── assets/                       # other application files
├── deploy/                           # deployment files
│   ├── QR_code.py
├── airflow/                          # airflow files
│   ├── dag.py
├── README.md                         # readme files
├── requirements.txt                  # requirement files


```

# AED Optimization Project for Modern Data Analytics Course
## Introduction
In this project, a machine learning model was built to predict survival rates for out-of-hospital cardiac arrest using intervention, hospital and AED information. Additionally, a web application was developed via Dash and Plotly to visualize the survival information with relation to locations of AEDs and hospitals, and to enable users to interactively add new AEDs to explore AED optimization possibilities.
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

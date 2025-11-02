# deng-task

The dataset can be acquired here: [Kaggle](https://www.kaggle.com/datasets/programmer3/catalytic-cracking-process-control-dataset)

Google drive link: [Google Drive](https://drive.google.com/drive/folders/1U4CEg9VGIRylRaEeVHwqn1dEEMGfP0mG?usp=drive_link)

The author claims that this dataset can be used to create an optimization model for the catalytic cracking unit.

Since it's a dataset from Kaggle, it allegedly lacks noise and outliers, although it does have operational disturbances.

## Dataset description

The dataset contains data on operational parameters of a catalytic cracking unit. General diagram of the process is shown below.

![Diagram](https://github.com/lagadoswift/deng-task/blob/main/images/FCCdiagram.png)

The following table provides short description of the columns in the dataset.


| Variable | Description |
| ------------- | ------------- |
| Reactor_Temperature | Self-explanatory |
| Regenerator_Temperature | Self-explanatory |
| Reactor_Pressure | Self-explanatory |
| Feed_Flow_Rate | Flow of oil |
| Catalyst_to_Oil_Ratio | Mass of catalyst divided to mass of oil in the reactor |
| Catalyst_Activity | Self-explanatory |
| Air_Flow_Rate | Flow of air to the regenerator |
| Fractionator_Top_Temp | Temperature in the upper section of the fractionator column |
| Fractionator_Bottom_Temp | Temperature in the lower section of the fractionator column |
| Feedstock_Quality_Index | Quality of the feedstock |
| Setpoint_Reactor_Temp | Target temperature for the PID controller |
| Setpoint_Regenerator_Temp | Target temperature for the PID controller |
| PID_Kp | Coeff. of the PID controller |
| PID_Ki | Coeff. of the PID controller |
| PID_Kd | Coeff. of the PID controller |
| Fuzzy_Adjustment_Factor | Parameter for the PID controller |
| Product_Yield | Product flow |
| Conversion_Rate | % of the chemically changed feed |
| Energy_Consumption | Energy consumed by the whole unit |
| Emission_NOx | Nitrogen oxides emission |
| Emission_SOx | Sulphur oxides emission |
| Control_Stability_Index | Parameter of the controller efficiency |
| Reward_Score | Controller parameter |
| Feed_Change_Event | Special event: feed change |
| Catalyst_Replacement | Special event: catalyst replacement |
| External_Disturbance_Type | External disturbance affecting the unit |

## Project structure

```
deng_task/
│
├── data/ # created after execution of the ETL process
│   ├──processed # a folder for the processed data
│   └──raw # a folder for the raw data
│ 
│── drafts/ # early drafts
│   ├── api_example/ # example of the api access
│   │   ├── .gitignore
│   │   ├── api_reader.py
│   │   ├── readme.md
│   │   └── requirements.txt
│   │
│   ├── parse_example/ # example of the webscraping using BeautifulSoup
│   │   ├── .gitignore
│   │   ├── data_parser.py
│   │   ├── readme.md
│   │   └── requirements.txt
│   │
│   ├── data_loader.py # early draft of the data extraction script
│   └── write_to_db.py # early draft of the load to DB script
│
│── etl/
│   ├── __init__.py
│   ├── extract.py # essential data extraction script
│   ├── load.py # essential data loading script
│   ├── main.py # essential script to launch the ETL process
│   └── transform.py # essential data transformation script
|
│── images/
│   └── FCCdiagram.png
│
│── notebooks/
│   └── eda.ipynb # Jupyter notebook where the data is being explored
│
├── .gitignore
├── readme.md # this file
└── requirements.txt # requirements for the project
```

## ETL components

- extract.py - the file which does the data extraction step. Accepts only .csv files for extraction. Also saves the raw data into data/raw/
- transform.py - this scripts changes types of the columns in the dataset and fills missing values
- load.py - this scripts uploads the transformed data into the SQL database and saves the processed data into data/processed
- main.py - the script to start the ETL process. Only this script should be started directly.

## Setting up the virtual environment and launching the ETL process

Requires Python 3.13.5 or newer.

Set up the Python virtual environment.

To install the required packages use pip. Open the project directory and type in the Windows cmd:

`py -m pip install -r requirements.txt`

Once all packages are installed, you should create an .env file with at least the following environment variables:

- INPUT_FILE - URL or disk destination of the file
- DB_USER - username to access the SQL database
- DB_PASSWORD - password for the SQL DB
- DB_URL - host address of the SQL DB
- DB_NAME - name of the SQL DB
- DB_TABLE_NAME - name of the table to save the data into

To launch the ETL process type in the cmd:

`python -m etl.main`

## EDA

EDA notebook can be viewed in the repository in [notebooks/EDA.ipynb](https://github.com/lagadoswift/deng-task/blob/main/notebooks/EDA.ipynb)

Visualization can also be viewed here: [NBview](https://nbviewer.org/github/lagadoswift/deng-task/blob/main/notebooks/EDA.ipynb)

Note that scatter plots are not visible from these links. You have to download the notebook and launch kernel in order to see the scatter plots.

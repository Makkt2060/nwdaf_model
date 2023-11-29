# Anomaly Detection in 5G Network 

The objective of the project is to identify anomalies according to data obtained from the network (simulated). To achieve this, the Data Analytic Platform (DAP) has a Machine Learning (ML) model, trained with network data (NWDAF), to detect anomalies. 

The NWDAF is the service responsible for triggering training and inference in the model. This service is divided into Model Training Logical Function (MTLF) and Analytics Logical Function (AnLF). MTLF is a function that trains ML models and exposes new training services such as an ML model provisioning service. AnLF performs inference with ML models and provides the analytics results to service consumers (e.g., 5G network functions, application functions, and OAM). When the NWDAF is activated, the Network Exposure Function (NEF) listens for the requests and passes the request to the DAP, following the idea of Pub/Sub.

The DAP is a Python module with a Flask Application Programming Interface (API) for providing the services to train ML models (MTLF) and perform inference on new data (AnLF). The MTLF class processes the data (feature engineering), trains an XGBoost model, and saves this model on a local path. The AnLF loads a trained model and performs inference on new data.

### Proposed architecture

![MicrosoftTeams-image](https://github.com/luanlazz/nwdaf_model/assets/23390758/da50e0a6-683b-42df-8d3e-b81cb5ae54e3)

## Data:

The project contains a structured Python notebook to describe the Exploratory Data Analysis (EDA) process, showing the details about the dataset used for training the ML model to detect anomalies. This notebook is available [here](./DAP/notebooks/eda.ipynb).

## ML Model:

The project also has a structured Python notebook for describing the training process of ML models. It is worth noting that this notebook pertains to an experimentation phase, being a good first step to understand how the training process occurs. This notebook can be accessed [here](./DAP/notebooks/model_training.ipynb).

In the production environment, the code of this notebook is organized in Python scripts, available in the [model folder](./DAP/model/).

## Requirements:

**Python libraries:**
- pandas
- sklearn
- xgboost
- flask

**Python version: 3.11.6**

**Go version : 1.21.4**

## Instructions to run:

1) DAP (Data analytics platform)

DAP description...
   
```
cd DAP 
python Main.py
```
> [!TIP]
> Expected result:

![image](https://github.com/luanlazz/nwdaf_model/assets/23390758/8e5fd61b-fa88-4b1e-b15c-cd594ca61b3e)

2) NEF (Network Exposure Function)
   
Responsible for exposing the 5G network, making network resources such as data and network services easily available to communication service providers and third parties. In this case, the DAP subscribes to the NWDAF service, allowing the NWDAF to trigger training or inference on the DAP.

To run the service, follow the code:
```
cd NEF
rm -rf go.sum
go mod tidy
go run server/nefserver.go
```
> [!TIP]
> Expected result:

![image](https://github.com/luanlazz/nwdaf_model/assets/23390758/12d12930-9655-461a-a530-520abb7dcb32)

3) NWDAF (Network Data Analytics Function)
   
Responsible for collecting information from various 5G core network functions (NF), application functions (AF), operations systems, administration and management, and operational support systems.
The service contain the model training (MTLF) and inference (AnLF).

To "compile" the service, follow the code:
```
cd NWDAF
rm -rf go.sum
go mod tidy
```

To training the service, follow the code: 
```
go run MTLF/model_training.go 
```
> [!TIP]
> Expected result:

![image](https://github.com/luanlazz/nwdaf_model/assets/23390758/4395d8e3-3b96-49e0-b9c8-5328f08f3be9)

To infer if there is an anomaly, follow the code:
```
go run AnLF/model_inference.go
```
This command randomly chooses a record in a network static dataset.
> [!TIP]
> Expected result:

![image](https://github.com/luanlazz/nwdaf_model/assets/23390758/89479e8a-4353-4c37-89bb-f96a0155cef2)


# Inconsistency detection in 5G Network 

This project use data analytics to detect inconsistency.  

## Requirements :

**Python libraries:**
- pandas
- sklearn

**Python version: 3.11.6**

**Go version : 1.21.4**

## Instructions to run:

1) DAP module
```
cd DAP 
python Main.py
```
> [!TIP]
> Expected result:

 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 944-792-113

2) NEF server
```
cd NEF
rm -rf go.sum
go mod tidy
go run server/nefserver.go
```

> [!TIP]
> Expected result:

Running on http://127.0.0.1:9538

3) NWDAF
```
cd NWDAF
rm -rf go.sum
go mod tidy
```

- run python module
```
cd pythonmodule
python main.py
```
Running on http://127.0.0.1:9538

- Training
```
go run MTLF/model_training.go 
```
- Inference
```
go run AnLF/model_inference.go
```

> [!TIP]
> Expected result:


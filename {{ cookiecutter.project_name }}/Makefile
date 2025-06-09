SHELL := /bin/bash

notebook:
	poetry run jupyter notebook --no-browser --port 8080

mlflow:
	cd ./experiments/logs && poetry run mlflow ui


# Dataproject

## The NokiaSnake Client
Throughout our studies we have focused on explanatory analysis. For this dataproject we decided on a different 
approach. The NokiaSnake Client is a tool to explore data. The Graphic User Interface allow for easy and interactive 
data import. Furthermore, you can easily adjust the columns and categories in the dataset. Data analysis made easy.

## Current version
The current version of the client supports custom table import from the DST api. We have also included a preloaded 
dataset NAN1. We use this preloaded dataset to give a tour of data analysis features to come. It's our ambition to 
extend these data analysis features to any and all tables found in the DST api

## What is included, and how to get the best experience
The repository contains:

README.md	           : The file you are reading

Project.py	           : The python file for the client

Dataproject.ipynb      : The Jupyter notebook, which goes into the details of the Client.

In order to get the best experience, we recommend you run the client from the project.py file.
The file is incapable of being run snippet by snippet as presented in the Jupyter notebook. 
We have however included the entire client in the last code cell, and the client can run from that cell.


### Requirements
The NokiaSnake Client requires the following libraries to run:

tkinter     : pip install tkinter

pandas      : pip intall pandas

numpy       : pip intall numpy

matplotlib  : pip install matplotlib

pydst       : pip install git+https://github.com/elben10/pydst 


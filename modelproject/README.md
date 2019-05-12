# Modelproject

## Glosten-Milgrom Model
In this project we derive and simulate the Glosten-Milgrom model for security markets. We further examine the proporties of the model. 
Lastly, we introduce several types of shock to the model and examine the adaptation of the equilibrium. 

The project can be read in [modelproject.ipynb](modelproject.ipynb). 

The project depends on plotter.py to make some graphs. The entire folder must therefore be downloaded in order to make the notebook run.


## The folder

README.md	           : The file you are reading

plotter.py		   : Custom graphwindow library. 

Modelproject.ipynb	   : The Jupyter notebook containing the project

__init__.py		   : Required file in order to import classes and functions from plotter.py


## Requirements
The modelproject requires the following libraries to run: matplotlib, numpy, sympy, pandas. It further depends on Plotter.py, 
which makes use of the tkinter and mpl-finance library.

you can get mpl-finance with : pip install mpl-finance

tkinter should be baseline in anaconda 3.7. If you get errors, try : pip install tkinter



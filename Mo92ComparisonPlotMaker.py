import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
#pip install corner
import corner
from scipy.optimize import curve_fit
from scipy import optimize
from scipy import integrate
#pip install emcee #PA added this
import emcee
from IPython.display import display, Math

nucleiData = np.loadtxt("Mo92.csv",delimiter=',')#these data are the photoneutron data

mask = np.abs(nucleiData[:,0]<24)#truncate to <24 MeV for the gamma-ray energy
nucleiData = nucleiData[mask]

xdata = nucleiData[1:,0]
ydata = nucleiData[1:,1]
dydata = nucleiData[1:,2]

nucleiData2 = np.loadtxt("Mo92_activation.csv",delimiter=',')#activation data, fairly obviously

mask = np.abs(nucleiData2[:,0]<24)#truncate to <24 MeV for the gamma-ray energy
nucleiData2 = nucleiData2[mask]

xdata2 = nucleiData2[1:,0]
ydata2 = nucleiData2[1:,1]
#dydata2 = nucleiData2[1:,2]

plt.errorbar(xdata, ydata, yerr=dydata, fmt=".k", capsize=0)
plt.plot(xdata2,ydata2,color="orange")
plt.legend(fontsize=14)
plt.xlim(10, 25)
plt.xlabel(r'$\gamma$-ray Energy [MeV]')
plt.ylabel("Cross Section [mb]")

outputFigName = 'figures/MoComparisonPlot.png'
plt.savefig(outputFigName)

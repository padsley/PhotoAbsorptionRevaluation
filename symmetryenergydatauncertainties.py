# -*- coding: utf-8 -*-
"""SymmetryEnergydatauncertainties.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DW2UwbUBtyMiGAetRvHMHwTgpzuJJyDe
"""

#from google.colab import drive
#drive.mount('/content/drive',force_remount=True)#need to run this before running the rest of the code to mount the shared drive

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

def model(theta,xdata):
  if(len(theta)==3):
    wid_fit,sig,em = theta
    cross_section_model = (sig*(wid_fit)**2*(xdata)**2)/(((xdata**2-em**2)**2)+((wid_fit)**2*(xdata)**2))
    #sigma_d = 61.2*(xdata - 2.22452)**(3/2)*xdata**(-3)
    #Pauli_blocking = -1
    #if(xdata[0:,]<20):
     # Pauli_blocking = numpy.exp**(-73.3/xdata)
    #elif(xdata[0:,]>140):
    #  Pauli_blocking = numpy.exp**(-24.2348/xdata)
    #else:
    #Pauli_blocking = 0.083714 - 0.0098343*xdata + 4.1222*10**(-4)*xdata**2 - 3.4762*10**(-6)*xdata**3 + 9.3537 * 10**(-9)*xdata**4
    #cross_section_model += 6.5 * 50*40/90 * sigma_d * Pauli_blocking
  elif(len(theta)==6):
    wid_fit1,sig1,em1,wid_fit2,sig2,em2 = theta
    cross_section_model = (sig1*(wid_fit1)**2*(xdata)**2)/(((xdata**2-em1**2)**2)+((wid_fit1)**2*(xdata)**2)) + (sig2*(wid_fit2)**2*(xdata)**2)/(((xdata**2-em2**2)**2)+((wid_fit2)**2*(xdata)**2))
  else:
    cross_section_model = -1
  return cross_section_model

def model_minus2(theta,x):
  if(len(theta)==3):
    wid_fit,sig,em = theta
    cross_section_model2 = (sig*(wid_fit)**2*(x)**2)/(((x**2-em**2)**2)+((wid_fit)**2*(x)**2))/x**2
  if(len(theta)==6):
    wid_fit1,sig1,em1,wid_fit2,sig2,em2 = theta
    cross_section_model2 = (sig1*(wid_fit1)**2*(x)**2)/(((x**2-em1**2)**2)+((wid_fit1)**2*(x)**2))/x**2 + (sig2*(wid_fit2)**2*(x)**2)/(((x**2-em2**2)**2)+((wid_fit2)**2*(x)**2))/x**2
  return cross_section_model2

#PA
def log_likelihood(theta, x, y, yerr):
  if(len(theta)==3):
    wid_fit, sig, em = theta #log_f is the log of the fractional underestimation of the Gaussian uncertainty
    model = (sig*(wid_fit)**2*(x)**2)/(((x**2-em**2)**2)+((wid_fit)**2*(x)**2))
    sigma2 = yerr**2
  elif(len(theta)==6):
    wid_fit1, sig1, em1, wid_fit2, sig2, em2 = theta #log_f is the log of the fractional underestimation of the Gaussian uncertainty
    model = (sig1*(wid_fit1)**2*(x)**2)/(((x**2-em1**2)**2)+((wid_fit1)**2*(x)**2)) + (sig2*(wid_fit2)**2*(x)**2)/(((x**2-em2**2)**2)+((wid_fit2)**2*(x)**2))
    sigma2 = yerr**2

  for i in range(len(sigma2)):
    if(sigma2[i] == 0):
      print("sigma2 = 0!")
    elif(sigma2[i] < 0):
      print("sigma2 = ",sigma2)

  return -0.5 * np.sum((y-model)**2 / sigma2 + np.log(sigma2))

#PA
def log_prior(theta):
  if(len(theta)==3):
    wid_fit, sig, em = theta
    if 0 < wid_fit < 25 and 0 < sig < 1000 and 0 < em < 30:
      return 0.0
  elif(len(theta)==6):
    wid_fit1, sig1, em1, wid_fit2, sig2, em2 = theta
    if 0 < wid_fit1 < 25 and 0 < sig1 < 1000 and 0 < em1 < 30 and 0 < wid_fit2 < 25 and 0 < sig2 < 1000 and 0 < em2 < 30:
      return 0.0
  return -np.inf

#PA
def log_probability(theta, x, y, yerr):
  lp = log_prior(theta)
  if not np.isfinite(lp):
    return -np.inf
  return lp + log_likelihood(theta, x, y, yerr)

#from google.colab import drive
#drive.mount('/content/drive')#need to run this before running the rest of the code to mount the shared drive

#string Nucleus = 'Pb208'

#Pb208 - Ref. Physical Review C xyz EXFOR entry xyz
#pathPb208 = '/content/drive/MyDrive/Pb208datacrosssectiondataCSV.csv'
#Pb208data = loadtxt(pathPb208,delimiter=',')


#92Zr from the other file - single photoneutron
#pathZr92s = '/content/drive/MyDrive/Zr92 Single Photo Neutron Cross section data .csv'
#Zr92sdata = loadtxt(pathZr92s,delimeter= ',')
#Pr141data = '/content/drive/MyDrive/PR141.csv'
#Tb159data = '/content/drive/MyDrive/Tb159.csv'
#Ta181data = '/content/drive/MyDrive/Ta181.csv'
listOfNuclei = list()
listOfNuclei.append('Y89')
listOfNuclei.append('Zr90')#finally a good fit! needs two peaks??
listOfNuclei.append('Zr91')#good fit
listOfNuclei.append('Zr92')#good fit
listOfNuclei.append('Zr94')
listOfNuclei.append('Rh103')#good fit
listOfNuclei.append('Sn112')
listOfNuclei.append('Sn114')
listOfNuclei.append('Sn116')
listOfNuclei.append('Sn117')
listOfNuclei.append('Sn118')
listOfNuclei.append('Sn119')
listOfNuclei.append('Sn120')
listOfNuclei.append('Sn122')
listOfNuclei.append('Sn124')
listOfNuclei.append('Cs133')#good fit
listOfNuclei.append('Ba138')#good fit
listOfNuclei.append('La139')#good fit
listOfNuclei.append('Pr141')#good fit
listOfNuclei.append('Sm144')#good fit
listOfNuclei.append('Tb159')#good fit
listOfNuclei.append('Ho165')#good fit
listOfNuclei.append('Tm169')#good fit
listOfNuclei.append('Ta181')#good fit with a new dataset
listOfNuclei.append('Au197')#good fit but might want to include lower-energy data
listOfNuclei.append('Pb206')
listOfNuclei.append('Pb207')#good fit but very small! -EXFOR data appear to peak at 500 mb not 600 mb as paper suggests
listOfNuclei.append('Pb208')#fit works

PolarValues = []
dPolarValues = []
MassNumberArray = []
ElementNumberArray = []
TRKValues = []
dTRKValues = []
ElementSymbolArray = []
StoreDBResultsForLaTeXTable = []
StoreCeboNicoResultsForLaTeXTable = []

#load values from Dietrich and Berman, so many data entry errors which I had to check :'(
DBMassArray = [89,89,89,90,90,91,92,92,93,94,94,96,98,100,103,107,115,115,116,116,117,117,118,118,119,120,120,124,124,124,126,127,127,127,128,130,133,133,138,139,140,141,141,141,141,141,142,142,143,144,144,145,146,148,148,150,150,152,153,154,159,159,160,165,165,175,181,181,186,186,188,189,190,190,197,197,197,206,207,208,208,208,209,209]
DBPolarValues = [3.48,4.46,2.52,3.38,4.08,4.07,3.92,3.16,4.80,4.40,4.73,5.44,5.89,6.06,5.97,4.82,7.13,6.91,6.13,6.78,7.30,7.05,6.83,7.07,7.55,7.79,7.49,8.02,6.74,8.29,8.56,6.70,8.53,5.4,8.92,9.27,8.09,9.09,8.71,8.54,10.3,8.37,7.31,6.41,7.0,6.4,10.7,8.66,9.39,9.01,8.41,11.3,9.6,9.02,9.51,10.4,10.4,10.5,10.2,10.6,10.5,12.1,11.6,13.9,12.9,12.5,10.7,14.8,14.5,13.2,16.7,16.7,15.8,16.0,14.7,15.9,15.6,15.0,14.2,14.2,17.6,13.3,15.8,13.8]

#removed 138La from this list because 138Ba in amongst the nuclei we analysed
CeboNicoMassArray = [45,50,51,56,766,92,95,139,153]
CeboNicoPolarValues = [1.840,1.458,1.472,2.231,3.189,3.131,4.743,8.015,9.999]
CeboNicoPolarValuesUncertainties = [0.130,0.100,0.100,0.155,0.225,0.220,0.330,0.560,0.700]

if(len(DBMassArray)!=len(DBPolarValues)):
  print("MESSED UP THE Dietrich and Berman RESULTS!!!")
  print(len(DBMassArray))
  print(len(DBPolarValues))

GorielyMassArray = [59,89,103,139,159,165,169,181,197,208,209]
GorielyTRKValues = [1.15,1.13,1.28,1.31,1.33,1.32,1.25,1.31,1.32,1.29,1.53]
dGorielyTRKValues = [0.01,0.02,0.01,0.02,0.01,0.03,0.02,0.03,0.02,0.03,0.02]
GorielyPolarValues = [2.84,4.73,6.90,10.78,13.63,15.11,13.56,16.40,18.04,19.82,22.64]
dGorielyPolarValues = [0.08,0.14,0.17,0.23,0.27,0.38,0.36,0.65,0.50,0.49,0.51]

#if(len(listNumPeaks) != len(listOfNuclei)):
#  sys.exit(1)#exit if the size of the array giving the number of peaks for the fits doesn't match the number of nuclei to be fitted

print("Going to run calculations for the following nuclei",listOfNuclei)

ListOfElementSymbols = np.loadtxt('ElementSymbols.csv',dtype='str')
#ListOfElementSymbols = np.array(ListOfElementSymbols)
print(ListOfElementSymbols)

#for loop from here down to
for NucleiName in listOfNuclei:
  #pathData = '/content/drive/Shareddrives/Photonuclear_CrossSections/'
  pathData = NucleiName

  pathData += '.csv'

  print(pathData)

  nucleiData = np.loadtxt(pathData,delimiter=',')

  mask = np.abs(nucleiData[:,0]<24)#truncate to <24 MeV for the gamma-ray energy
  nucleiData = nucleiData[mask]

  #extract the mass number from the array (eventually, this took me way too long!)
  A = ''.join(filter(str.isdigit,NucleiName))
  print("the mass number is",A)
  numberA = int(A)#need to convert to use as a number in calculations
  print("numberA = ",numberA)
  
  dummytext = ""
  
  for i in range(len(DBMassArray)):
    if(numberA==DBMassArray[i]):
        print("DBMassArray[",i,"]: ",DBMassArray[i])
        print("DBPolarValues[",i,"]: ",str(DBPolarValues[i]))
        if(dummytext==""):
            dummytext += str(DBPolarValues[i])
        else:
            dummytext += "/"
            dummytext += str(DBPolarValues[i])
    
  print("dummy text for storing DB results for LaTeX Table: ",dummytext)
  StoreDBResultsForLaTeXTable.append(dummytext)
  
  
  dummytext = ""
  for i in range(len(CeboNicoMassArray)):
      if(numberA==CeboNicoMassArray[i]):
          dummytext += str(CeboNicoPolarValues[i])
          dummytext += "("
          dummytext += str(CeboNicoPolarValuesUncertainties[i]*1000)#the x1000 is cheating to get the right formatting for the table since all of the uncertainties are around the same size, don't judge me
          dummytext += ")"
  
  StoreCeboNicoResultsForLaTeXTable.append(dummytext)

  ElementSymbol = ''.join(filter(str.isalpha,NucleiName))
  print("the element symbol is",ElementSymbol)
  ElementNumber = (np.where(ListOfElementSymbols==ElementSymbol))[0]+1#returns an array for the symbol index starting at 0 so we need to add one to get proton number and also get a number not an array
  print('the element/proton number is',ElementNumber[0])

  ElementSymbolArray.append(ElementSymbol)

  xdata = nucleiData[1:,0]
  ydata = nucleiData[1:,1]
  dydata = nucleiData[1:,2]

  #take the differential data to find the peaks
  differential_data = np.gradient(ydata,xdata)

  plt.plot(xdata,differential_data)#checking what the differential data look like for finding the peaks and shit like that - PA

  #to store the peak index/location
  PeakIndices = list()
  PeakLocations = list()

  for i in range(len(differential_data)):
    if(differential_data[i-1]>0 and differential_data[i]<0 and len(PeakLocations)==0 and ydata[i]>0.5*np.max(ydata)):
      PeakIndices.append(i)
      PeakLocations.append(0.5*(xdata[i]+xdata[i-1]))
    elif(len(PeakIndices)==1 and differential_data[i-1]>0 and differential_data[i]<0 and len(PeakLocations)==1 and np.abs(xdata[i]-PeakLocations[0])>1.0 and ydata[i]>0.2*np.max(ydata) and ydata[i]>0.5*np.max(ydata)):#0.6 here is chosen manually because I couldn't work out how to automate this
      print('Found a second peak in condition 1')
      PeakIndices.append(i)
      PeakLocations.append(0.5*(xdata[i]+xdata[i-1]))
    elif(len(PeakIndices)==1 and i<len(differential_data)-1 and differential_data[i-i]-differential_data[i]>0 and differential_data[i+1]-differential_data[i]>0 and np.abs(xdata[i]-PeakLocations[0])>2.5 and ydata[i]>0.5*np.max(ydata)):
      print('Found a second peak in condition 2')
      print('i',i)
      print('differential_data[i-i]-differential_data[i]',differential_data[i-i]-differential_data[i])
      print('differential_data[i+1]-differential_data[i]',differential_data[i+1]-differential_data[i])
      PeakIndices.append(i)
      PeakLocations.append(0.5*(xdata[i]+xdata[i-1]))
      print('ydata',ydata[i])
      print('ydata max/2',0.5*np.max(ydata))

  if(len(PeakLocations)>2):
    print("Too many peaks! Aaahhhh!")

  print("Peak locations:",PeakLocations)

  probability_list = []

  PeakWidths = []

  #find the peak widths!
  if(len(PeakIndices)>0):
    #print(ydata[0:PeakIndices[0]])
    width = np.abs(xdata[PeakIndices[0]] - xdata[np.abs(ydata[0:PeakIndices[0]] - 0.5*np.max(ydata)).argmin()])
    PeakWidths.append(width)
  if(len(PeakIndices)==2):
    width = np.abs(xdata[PeakIndices[1]] - xdata[np.abs(ydata[PeakIndices[1]:len(ydata)] - 0.5*np.max(ydata[PeakIndices[1]:len(ydata)])).argmin()])
    #print('xdata[PeakIndices[1]]',xdata[PeakIndices[1]],'xdata[np.abs(ydata[PeakIndices[1]:len(ydata)] - 0.5*np.argmax(ydata)).argmin()]',xdata[np.abs(ydata[PeakIndices[1]:len(ydata)] - 0.5*np.argmax(ydata)).argmin()],)
    PeakWidths.append(width)

  #print("PeakWidths",PeakWidths)

  #fit_result = optimize.fmin(lnlike, x0=[10.2,37.5])
  np.random.seed(42)
  nll = lambda *args: -log_likelihood(*args)

  #generalising the starting guesses
  

  if(len(PeakLocations)==1):
    initial = np.array([PeakWidths[0],ydata[PeakIndices[0]],PeakLocations[0]])+ 0.1*np.random.randn(3)
  elif(len(PeakLocations)==2):
    initial = np.array([PeakWidths[0],ydata[PeakIndices[0]],PeakLocations[0],PeakWidths[1],ydata[PeakIndices[1]],PeakLocations[1]]) + 0.1*np.random.randn(6)

  print('initial array',initial)

  soln = optimize.minimize(nll, initial, args=(xdata, ydata, dydata))
  if(len(soln.x)==3):
    wid_fit_opt, sig_opt, em_opt = soln.x
    #print("Maximum likelihood estimates:")
    #print("Width = {0:.3f}".format(wid_fit_opt))
    #print("Max cross section = {0:.3f}".format(sig_opt))
    #print("Peak Energy = {0:.3f}".format(em_opt))
  elif(len(soln.x)==6):
    wid_fit1_opt, sig1_opt, em1_opt, wid_fit2_opt, sig2_opt, em2_opt = soln.x
    #print("Maximum likelihood estimates:")
    #print("Width 1 = {0:.3f}".format(wid_fit1_opt))
    #print("Max cross section 1 = {0:.3f}".format(sig1_opt))
    #print("Peak Energy 1 = {0:.3f}".format(em1_opt))
    #print("Width 2 = {0:.3f}".format(wid_fit2_opt))
    #print("Max cross section 2 = {0:.3f}".format(sig2_opt))
    #print("Peak Energy 2 = {0:.3f}".format(em2_opt))

  print("soln.x",soln.x)

  if(len(soln.x)==6):
    if(NucleiName=='Sn112' or NucleiName=='Zr94'):
      print('Sn112 or Zr94, need to manually make a single peak for some reason?')
      initial = np.array([PeakWidths[0],ydata[PeakIndices[0]],PeakLocations[0]])+ 0.1*np.random.randn(3)
      soln = optimize.minimize(nll, initial, args=(xdata, ydata, dydata))
      wid_fit_opt, sig_opt, em_opt = soln.x
    elif(sig1_opt*wid_fit1_opt < 0.15*sig2_opt*wid_fit2_opt or sig1_opt < 0.15*sig2_opt):
      print("first peak too small, use only the second one for fitting")
      initial = np.array([PeakWidths[1],ydata[PeakIndices[1]],PeakLocations[1]])+ 0.1*np.random.randn(3)
      soln = optimize.minimize(nll, initial, args=(xdata, ydata, dydata))
      wid_fit_opt, sig_opt, em_opt = soln.x
    elif(sig2_opt*wid_fit2_opt < 0.15*sig1_opt*wid_fit1_opt or sig2_opt < 0.15*sig1_opt):
      print("second peak too small, use only the first one for fitting")
      initial = np.array([PeakWidths[0],ydata[PeakIndices[0]],PeakLocations[0]])+ 0.1*np.random.randn(3)
      soln = optimize.minimize(nll, initial, args=(xdata, ydata, dydata))
      wid_fit_opt, sig_opt, em_opt = soln.x
    else:
      print("Using two peaks for the later analysis")
      print(soln.x)

  #print("Fractional underestimation = {0:.3f}".format(log_f_opt))

  #after this, mostly using https://emcee.readthedocs.io/en/stable/tutorials/line/

  #draw some shit
  #len==3 for one peak, len==6 for two peaks
  if(len(soln.x)==3):
    fit_y = model([wid_fit_opt, sig_opt, em_opt],xdata)
  elif(len(soln.x)==6):
    fit_y = model([wid_fit1_opt, sig1_opt, em1_opt, wid_fit2_opt, sig2_opt, em2_opt],xdata)
    fit_y1 = model([wid_fit1_opt, sig1_opt, em1_opt],xdata)
    fit_y2 = model([wid_fit2_opt, sig2_opt, em2_opt],xdata)

  x_outline = np.linspace(0, 10, 500)

  plt.errorbar(xdata, ydata, yerr=dydata, fmt=".k", capsize=0)
  if(len(soln.x)==3):
    plt.plot(xdata, fit_y, "k", alpha=0.3, lw=3, label="ML")
  elif(len(soln.x)==6):
    plt.plot(xdata, fit_y1, "k", alpha=0.3, lw=3, label="ML 1")
    plt.plot(xdata, fit_y2, "k", alpha=0.3, lw=3, label="ML 2")
  #plt.plot(x0=[10,23], np.dot(np.vander(x0, 2), w), "--k", label="LS")
  #plt.plot(x0=[10,23], np.dot(np.vander(x0, 2), [m_ml, b_ml]), ":k", label="ML")
  plt.legend(fontsize=14)
  plt.xlim(10, 25)
  plt.xlabel(r'$\gamma$-ray Energy [MeV]')
  plt.ylabel("Cross Section [mb]")
  

  #now need to do the walkers for the photoabsorption cross section to get the samples and shit like that
  pos = soln.x + 1e-4 * np.random.randn(32, len(soln.x))#make sure to use the right dimensional set of walkers :)
  nwalkers, ndim = pos.shape

  sampler = emcee.EnsembleSampler(
      nwalkers, ndim, log_probability, args=(xdata, ydata, dydata)
  )
  if(len(soln.x)==3):
    sampler.run_mcmc(pos, 5000, progress=True);
  elif(len(soln.x)==6):
    sampler.run_mcmc(pos, 10000, progress=True);


  if(len(soln.x)==3):
    fig, axes = plt.subplots(3, figsize=(10, 7), sharex=True)
    samples = sampler.get_chain()
    labels = ["$\Gamma$ [MeV]", "Peak Cross Section [mb]", "Peak Energy [MeV]"]
  elif(len(soln.x)==6):
    fig, axes = plt.subplots(6,figsize=(10, 7), sharex=True)
    samples = sampler.get_chain()
    labels = ["$\Gamma$ 1 [MeV]", "Peak Cross Section 1 [mb]", "Peak Energy 1 [MeV]", "$\Gamma$ 2 [MeV]", "Peak Cross Section 2 [mb]", "Peak Energy 2 [MeV]"]
  for i in range(ndim):
      ax = axes[i]
      ax.plot(samples[:, :, i], "k", alpha=0.3)
      ax.set_xlim(0, len(samples))
      ax.set_ylabel(labels[i])
      ax.yaxis.set_label_coords(-0.1, 0.5)

  axes[-1].set_xlabel("step number");

  tau = sampler.get_autocorr_time()
  #print(tau)

  flat_samples = sampler.get_chain(discard=100, thin=15, flat=True)
  #print(flat_samples.shape)

  if(len(soln.x)==3):
    fig = corner.corner(
        flat_samples, labels=labels, truths=[wid_fit_opt, sig_opt, em_opt]
    );
  if(len(soln.x)==6):
    fig = corner.corner(
        flat_samples, labels=labels, truths=[wid_fit1_opt, sig1_opt, em1_opt, wid_fit2_opt, sig2_opt, em2_opt]
    );

  outputFigName = 'figures/'
  outputFigName += NucleiName
  outputFigName += 'CornerPlot.pdf'
  plt.savefig(outputFigName)

  outputFigName = 'figures/'
  outputFigName += NucleiName
  outputFigName += 'CornerPlot.png'
  plt.savefig(outputFigName)
  plt.clf()
  #plt.ion()

  #fig4 = plt.figure(4)

  plot_xdata = []
  xdata_range = xdata[len(xdata)-1] - xdata[0]
  Energy = xdata[0]
  while Energy < 25:
    plot_xdata.append(Energy)
    Energy += 0.001

  #still don't understand this need to convert the array but whatevs
  plot_xdata = np.array(plot_xdata)

  #making nicer fitted data to plot (it's the same function and fit parameters but more x-points so it looks smooooooother)
  if(len(soln.x)==3):
    plot_fit_y = model([wid_fit_opt, sig_opt, em_opt],plot_xdata)
  elif(len(soln.x)==6):
    plot_fit_y = model([wid_fit1_opt, sig1_opt, em1_opt, wid_fit2_opt, sig2_opt, em2_opt],plot_xdata)
    plot_fit_y1 = model([wid_fit1_opt, sig1_opt, em1_opt],plot_xdata)
    plot_fit_y2 = model([wid_fit2_opt, sig2_opt, em2_opt],plot_xdata)

  plt.errorbar(xdata, ydata, yerr=dydata, fmt=".k", capsize=0)
  if(len(soln.x)==3):
    plt.plot(plot_xdata, plot_fit_y, "k", alpha=0.3, lw=3, label="ML")
  elif(len(soln.x)==6):
    plt.plot(plot_xdata, plot_fit_y1, "k", alpha=0.3, lw=3, label="ML 1")
    plt.plot(plot_xdata, plot_fit_y2, "r", alpha=0.3, lw=3, label="ML 2")
    plt.plot(plot_xdata, plot_fit_y, "b", alpha=0.3, lw=3, label="ML Combined")
  #draw some of the ranges of fits onto the figure - not working right now :(
  inds = np.random.randint(len(flat_samples), size = 100)
  for ind in inds:
    sample = flat_samples[ind]
    #print(sample)
    plt.plot(plot_xdata,model(sample,plot_xdata), "C1", alpha = 0.1)#trying to draw on fitting parameters and stuff


  plt.ylabel(r'$\sigma$ [mb]')
  plt.xlabel(r"$E_{\gamma}$ [MeV]")

  outputFigName = 'figures/'
  outputFigName += NucleiName
  outputFigName += 'Fitted.png'
  plt.savefig(outputFigName)
  
  outputFigName = 'figures/'
  outputFigName += NucleiName
  outputFigName += 'Fitted.pdf'
  plt.savefig(outputFigName)

  #plt.errorbar(xdata,ydata,yerr=dydata, fmt=".k", capsize= 0)
  #plt.xlabel("Egamma [MeV]")
  #plt.ylabel("Cross section [mb]")

  for i in range(ndim):
    mcmc = np.percentile(flat_samples[:, i], [16, 50, 84])
    q = np.diff(mcmc)
    txt = "\mathrm{{{3}}} = {0:.3f}_{{-{1:.3f}}}^{{{2:.3f}}}"
    txt = txt.format(mcmc[1], q[0], q[1], labels[i])
    display(Math(txt))
  #print("Phil is trying to work out where we've got to in the code")
  #display(sampler) # displaying peak cross section and peak energy
  #print("Phil is trying to work out where we've got to in the code 2")
  #display(flat_samples) #this is where the samples that Aaron was printing out are
  #display(samples)

  #putting an easy way to change the limits for the integrations!
  lower_limit = plot_xdata[0]
  lower_limit = 6
  upper_limit = 40

  #this is Phil dicking around with the code to see what happens
  integral_result_sigma_minus2 = integrate.quad(lambda x:model_minus2(soln.x,x),lower_limit,upper_limit)
  print("integral result for the best fit values")
  print(integral_result_sigma_minus2)

  integral_result_array = []
  integral_result_array_TRK = []
  integral_result_array_TRK_vs_Energy = []
  integral_result_array_sigma2_vs_Energy = []

  for i in range(len(flat_samples[:,1])):
    integral_result_array.append(integrate.quad(lambda x:model_minus2(flat_samples[i,:],x),lower_limit,upper_limit))

  for i in range(len(flat_samples[:,1])):
    integral_result_array_TRK.append(integrate.quad(lambda x:model(flat_samples[i,:],x),lower_limit,upper_limit))

  #print(integral_result_array)
  #display(integral_result_array)
  for i in range(len(plot_xdata)):
    integral_result_array_TRK_vs_Energy.append(integrate.quad(lambda x:model(soln.x,x),lower_limit,plot_xdata[i]))
    integral_result_array_sigma2_vs_Energy.append(integrate.quad(lambda x:model_minus2(soln.x,x),lower_limit,plot_xdata[i]))

  integral_result_array_TRK_vs_Energy = np.array(integral_result_array_TRK_vs_Energy)
  integral_result_array_sigma2_vs_Energy = np.array(integral_result_array_sigma2_vs_Energy)

  plt.clf()
  plt.plot(plot_xdata,integral_result_array_sigma2_vs_Energy[:,0])
  plt.xlabel('$E_{max}$ [MeV]')
  plt.ylabel(r'$\sigma_{-2}$ [mb/MeV]')
  plt.axhline(y=integral_result_sigma_minus2[0],xmin=0.01,xmax=0.99,color='blue',linestyle=':',alpha=1.0,label="Proper Result")

  outputFigName = 'figures/'
  outputFigName += NucleiName
  outputFigName += 'DipolePolExhaustionPlot.png'
  plt.savefig(outputFigName)
  plt.clf()
  #plt.ion()

  integral_result_array= np.array(integral_result_array)
  integral_result_array_TRK = np.array(integral_result_array_TRK)

  #trying to plot a histogram
  dummyy, dummyx, _ = plt.hist(integral_result_array[:,0],bins=200,histtype='step')
  plt.draw()

  percentiles = np.percentile(integral_result_array[:,0],[16,50,84])
  #print("percentiles values")
  #display(percentiles)

  percentiles_TRK = np.percentile(integral_result_array_TRK[:,0],[16,50,84])
  #display(percentiles_TRK)

  #alternative TRK comparison
  TRK_evaluation = 0
  if(len(soln.x)==3):
    TRK_evaluation = 0.5*np.pi * soln.x[0] * soln.x[1]
  elif(len(soln.x)==6):
    TRK_evaluation = 0.5*np.pi * (soln.x[0] * soln.x[1] + soln.x[4] * soln.x[5])

  print("TRK_evaluation",TRK_evaluation)

  y_range = plt.ylim()

  plt.plot([integral_result_sigma_minus2[0],integral_result_sigma_minus2[0]],[0.5*y_range[1],y_range[1]])
  #plt.plot([percentiles[0],percentiles[0]],[0,dummyy.max()],color='blue', linestyle=':',linewidth=2,alpha=0.75)
  #plt.plot([percentiles[1],percentiles[1]],[0,dummyy.max()],color='blue', linestyle=':',linewidth=2,alpha=0.75)
  #plt.plot([percentiles[2],percentiles[2]],[0,dummyy.max()],color='blue', linestyle=':',linewidth=2,alpha=0.75)
  plt.plot([percentiles[1],percentiles[1]],[0,0.5*y_range[1]],color='blue')

  rect = patches.Rectangle((percentiles[0],y_range[0]),percentiles[2]-percentiles[0],0.5*(y_range[1]-y_range[0]),alpha=0.3,color='blue')#adding a box to show the percentiles region
  plt.gca().add_patch(rect)

  plt.xlabel(r'$\sigma_{-2}$ [mb/MeV]')
  plt.ylabel("Counts per bin");

  plt.draw()
  #plt.show()

  outputFigName = 'figures/'
  outputFigName += NucleiName
  outputFigName += 'PercentilesPlot.pdf'
  plt.savefig(outputFigName)

  outputFigName = 'figures/'
  outputFigName += NucleiName
  outputFigName += 'PercentilesPlot.png'
  plt.savefig(outputFigName)
  plt.clf()

  #plt.ion()

  #want to save the plots and the output values into a file at this point as well

  #print(NucleiName)
  MassNumberArray.append(numberA)
  #print(numberA)
  #print(MassNumberArray)
  ElementNumberArray.append(ElementNumber[0])
  #print(ElementNumber[0])
  #PolarValues.append(percentiles[1])
  PolarValues.append(percentiles[1])
  #print(percentiles[1])
  #print(PolarValues)
  dPolarValues.append(percentiles[1]-percentiles[0])
  TRKValues.append(percentiles_TRK[1])
  dTRKValues.append(percentiles_TRK[1]-percentiles_TRK[0])
#for loop should end here!

ConversionConstant = 2*pow(np.pi,2.)/197.327*10 #conversion constant for alpha_D to sigma(-2) (*10 to go from fm^2 to mb)
#add Tin values from Bassauer++ arXiv 2007.06010
RCNPMassNumberArray = []
RCNPPolarValues = []
RCNPdPolarValues = []
RCNPPolarValuesRatio = []
RCNPdPolarValuesRatio = []

RCNPMassNumberArray.append(112)
RCNPPolarValues.append(7.19*ConversionConstant)
RCNPdPolarValues.append(0.50*ConversionConstant)

RCNPMassNumberArray.append(114)
RCNPPolarValues.append(7.29*ConversionConstant)
RCNPdPolarValues.append(0.58*ConversionConstant)

RCNPMassNumberArray.append(116)
RCNPPolarValues.append(7.52*ConversionConstant)
RCNPdPolarValues.append(0.51*ConversionConstant)

RCNPMassNumberArray.append(118)
RCNPPolarValues.append(7.91*ConversionConstant)
RCNPdPolarValues.append(0.87*ConversionConstant)

RCNPMassNumberArray.append(120)
RCNPPolarValues.append(8.08*ConversionConstant)
RCNPdPolarValues.append(0.60*ConversionConstant)

RCNPMassNumberArray.append(124)
RCNPPolarValues.append(7.99*ConversionConstant)
RCNPdPolarValues.append(0.56*ConversionConstant)

RCNPMassNumberArray.append(208)#Tamii-san 208Pb PRL
RCNPPolarValues.append(20.1*ConversionConstant)
RCNPdPolarValues.append(0.6*ConversionConstant)

#convert the array to numpy cos it's more useful
MassNumberArray = np.array(MassNumberArray)
#print(PolarValues)
PolarValues = np.array(PolarValues)
#print(PolarValues)
dPolarValues = np.array(dPolarValues)

#sort according to mass - why did I do this?!
#MassNumberArray, PolarValues, dPolarValues = zip(*sorted(zip(MassNumberArray,PolarValues,dPolarValues)))

#arrays for the ratio values
PolarValuesRatio = []
dPolarValuesRatio = []
DBPolarValuesRatio = []
GorielyPolarRatio = []
dGorielyPolarRatio = []

#compute the ratio values!
for i in range(len(PolarValues)):
  PolarValuesRatio.append(1000*PolarValues[i]/(2.4*pow(MassNumberArray[i],5./3.)))
  dPolarValuesRatio.append(1000*PolarValues[i]/(2.4*pow(MassNumberArray[i],5./3.))*pow(pow(dPolarValues[i]/PolarValues[i],2.) + pow(0.1/2.4,2.),0.5))

for i in range(len(RCNPPolarValues)):
  RCNPPolarValuesRatio.append(1000*RCNPPolarValues[i]/(2.4*pow(RCNPMassNumberArray[i],5./3.)))
  RCNPdPolarValuesRatio.append(1000*RCNPPolarValues[i]/(2.4*pow(RCNPMassNumberArray[i],5./3.))*pow(pow(RCNPdPolarValues[i]/RCNPPolarValues[i],2.) + pow(0.1/2.4,2.),0.5))

for i in range(len(DBMassArray)):
  DBPolarValuesRatio.append(1000*DBPolarValues[i]/(2.4*pow(DBMassArray[i],5./3.)))

for i in range(len(GorielyMassArray)):
  GorielyPolarRatio.append(1000*GorielyPolarValues[i]/(2.4*pow(GorielyMassArray[i],5./3.)))
  dGorielyPolarRatio.append(1000*GorielyPolarValues[i]/(2.4*pow(GorielyMassArray[i],5./3.))*pow(pow(dGorielyPolarValues[i]/GorielyPolarValues[i],2.) + pow(0.1/2.4,2.),0.5))


#spread out values slightly in x - this is solely so people can see WTF is going on
DBMassArrayPlotting = [x + 0.2 for x in DBMassArray]
GorielyMassArrayPlotting = [x + 0.1 for x in GorielyMassArray]
RCNPMassNumberArrayPlotting = [x - 0.1 for x in RCNPMassNumberArray]

fig, ax = plt.subplots(1)
ax.errorbar(MassNumberArray,PolarValues, yerr=dPolarValues,fmt=".", capsize=0,label="Present Evaluation",color='red')
ax.set_aspect(0.75)
plt.plot(DBMassArrayPlotting,DBPolarValues,".",color='black',label="Dietrich and Berman")
plt.errorbar(GorielyMassArrayPlotting,GorielyPolarValues,yerr=dGorielyPolarValues,fmt=".",capsize=0,color='green',label="Goriely et al.",cap=1)
plt.errorbar(RCNPMassNumberArrayPlotting,RCNPPolarValues, yerr=RCNPdPolarValues,fmt=".",color='purple',capsize=0,label="RCNP Data",cap=1)
plt.xlabel('Mass Number')
plt.ylabel(r'$\sigma_{-2}$ [mb/MeV]');
plt.savefig('CombinedPolarPlot.pdf')
plt.savefig('CombinedPolarPlot.png')
plt.clf()

#now plot this with a ratio plot because that's more reasonable
#plt.figure(6)

#plt.plot(MassNumberArray,PolarValuesRatio)

fig2, ax2 = plt.subplots(figsize=[320/25.4, 190/25.4])
ax2.errorbar(MassNumberArray, PolarValuesRatio, yerr=dPolarValuesRatio,fmt=".", capsize=0,label="Present Evaluation",color='red')
ax2.set_aspect(100)
ax2.axhline(y=1.0,xmin=0.01,xmax=0.99,color='blue',linestyle=':',alpha=1.0)#the xmin and xmax go from 0 to 1 for each part of the graph (thanks John)
ax2.axhline(y=2.5/2.4,xmin=0.01,xmax=0.99,color='blue',linestyle=':',alpha=0.75)
ax2.axhline(y=2.3/2.4,xmin=0.01,xmax=0.99,color='blue',linestyle=':',alpha=0.75)
ax2.plot(DBMassArrayPlotting,DBPolarValuesRatio,".",color='black',label="Dietrich and Berman")
ax2.errorbar(GorielyMassArrayPlotting,GorielyPolarRatio,yerr=dGorielyPolarRatio,fmt=".",capsize=0,color='green',label="Goriely et al.")
ax2.errorbar(RCNPMassNumberArrayPlotting, RCNPPolarValuesRatio, yerr=RCNPdPolarValuesRatio,fmt=".",color='purple', capsize=0,label="RCNP Data")



y_range = plt.ylim()
#print('y_range',y_range)

rect = patches.Rectangle((136,y_range[0]),8,y_range[1]-y_range[0],alpha=0.3,color='blue')#adding the region of the N=82 shell closure
plt.gca().add_patch(rect)
rect2 = patches.Rectangle((86,y_range[0]),6,y_range[1]-y_range[0],alpha=0.3,color='blue')#adding the region of the N=50 shell closure
plt.gca().add_patch(rect2)
rect3 = patches.Rectangle((208,y_range[0]),2,y_range[1]-y_range[0],alpha=0.3,color='blue')#adding the region of the N=126 shell closure
plt.gca().add_patch(rect3)
rect_z1 = patches.Rectangle((112,y_range[0]),12,y_range[1]-y_range[0],alpha=0.3,color='red')#adding the Z=50 shell closure
plt.gca().add_patch(rect_z1)
rect_z2 = patches.Rectangle((204,y_range[0]),4,y_range[1]-y_range[0],alpha=0.3,color='red')#adding the Z=82 shell closure
plt.gca().add_patch(rect_z2)
plt.xlabel('Mass Number',fontsize=16)
plt.ylabel(r'$\sigma_{-2}$ / 2.4 $A^{5/3}$',fontsize=16)
plt.legend()
plt.savefig('CombinedRatioPlot.pdf')
plt.savefig('CombinedRatioPlot.png')
plt.clf()
#plt.ion()


print('Polarisation values from the current work')
#print(PolarValues)
for i in range(len(PolarValues)):
  print(i,'Nuclei Name:',listOfNuclei[i],'Dipole Polarisability Value:',PolarValues[i],'+-',dPolarValues[i])

print('TRK exhaustion from the current work')
for i in range(len(TRKValues)):
  kappa = 0.0
  print('MassNumberArray',MassNumberArray[i],'ElementNumberArray',ElementNumberArray[i],'Neutrons!',MassNumberArray[i]-ElementNumberArray[i])
  TRKCalculation = 60*(MassNumberArray[i] - ElementNumberArray[i]) * ElementNumberArray[i]/ MassNumberArray[i] * (1+kappa) #in MeV mb, 60NZ/A(1+k)
  print('Nuclei Name:',listOfNuclei[i],'TRKValues',TRKValues[i],'TRKCalculation',TRKCalculation,'TRK Sum Value',TRKValues[i]/TRKCalculation)

#make LaTeX table for paper
for i in range(len(PolarValues)):
    superstring =  "$^{"
    superstring += str(MassNumberArray[i])
    superstring += "}$"
    superstring += str(ElementSymbolArray[i])
    superstring += " & "
    superstring += str(StoreDBResultsForLaTeXTable[i])
    superstring += " & "
    superstring += str(StoreCeboNicoResultsForLaTeXTable[i])
    superstring += " & "
    
    if(dPolarValues[i]<0.01):
        superstring += "{0:.3f}".format(PolarValues[i])
    elif(dPolarValues[i]<0.1):
        superstring += "{0:.2f}".format(PolarValues[i])
    elif(dPolarValues[i]<1):
        superstring += "{0:.1f}".format(PolarValues[i])
    else:
        superstring += "{0:.0f}".format(PolarValues[i])
    superstring += "("
    
    if(dPolarValues[i]<0.01):
        superstring += str(round(dPolarValues[i]*1000))
    elif(dPolarValues[i]<0.1):
        superstring += str(round(dPolarValues[i]*100))
    elif(dPolarValues[i]<1):
        superstring += str(round(dPolarValues[i]*10))
    else:
        superstring += str(round(dPolarValues[i]))
        
    superstring += ")"
    
    superstring += " & "
    
    TRKCalculation = 60*(MassNumberArray[i] - ElementNumberArray[i]) * ElementNumberArray[i]/ MassNumberArray[i] * (1+kappa) #in MeV mb, 60NZ/A(1+k)
    
    if(dTRKValues[i]/TRKCalculation<0.01):
        superstring += "{0:.3f}".format(TRKValues[i]/TRKCalculation)
    elif(dTRKValues[i]/TRKCalculation<0.1):
        superstring += "{0:.2f}".format(TRKValues[i]/TRKCalculation)
    elif(dTRKValues[i]/TRKCalculation<1):
        superstring += "{0:.1f}".format(TRKValues[i]/TRKCalculation)
    else:
        superstring += str(round(TRKValues[i])/TRKCalculation)
    superstring += "("
    
    if(dTRKValues[i]/TRKCalculation<0.01):
        superstring += str(round(dTRKValues[i]*1000/TRKCalculation))
    elif(dTRKValues[i]/TRKCalculation<0.1):
        superstring += str(round(dTRKValues[i]*100/TRKCalculation))
    elif(dTRKValues[i]/TRKCalculation<1):
        superstring += str(round(dTRKValues[i]*10/TRKCalculation))
    else:
        superstring += str(round(dTRKValues[i]/TRKCalculation))
        
    superstring += ") \\\\"
    
    print(superstring)

"""# New Section"""

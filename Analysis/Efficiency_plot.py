import uproot
import awkward as ak
import matplotlib.pyplot as plt
import hist
from hist import Hist
from coffea.nanoevents import NanoEventsFactory, BaseSchema
import coffea.processor as processor
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import numpy as np
import mplhep as hep
from Selection import *


#fname   = "/eos/user/b/bchitrod/HHH/NANOAOD/TRSM_XToHY_6b_M3_2000_M2_1100_NANOAOD.root" #on lxplus
fname = "/STORE/ferencek/TRSM_XToHY_6b/2017/13TeV/NANOAOD/TRSM_XToHY_6b_M3_2000_M2_1100_NANOAOD.root" 

MX = [400,800,1200,1600,2000,2400,2800,3200,3600,4000]
MY = [260,300,700,1100,1500,1900,2300,2700,3100,3500,3900]

boosted_eff = [0,0]
semiboosted_eff = [0,0]
Mass_X = [0,4000]
Mass_Y = [-100,4000]

for mx in MX:
    for my in MY:
        if my+130<mx:
            fname   = "/STORE/ferencek/TRSM_XToHY_6b/2017/13TeV/NANOAOD/TRSM_XToHY_6b_M3_{0}_M2_{1}_NANOAOD.root".format(mx,my)
            oFile   = "{0}_{1}".format(mx,my)

            boosted_fatjets = boosted(fname,oFile,processLabel="MX{0}_MY{1}".format(mx,my),eventsToRead=None)
            boosted_efficiency = ak.num(boosted_fatjets,axis=0)/100
            boosted_eff.append(boosted_efficiency)
            
            semiboosted_fatjets = semiboosted(fname,oFile,processLabel="MX{0}_MY{1}".format(mx,my),eventsToRead=None)
            semiboosted_efficiency = ak.num(semiboosted_fatjets[1],axis=0)/100
            semiboosted_eff.append(semiboosted_efficiency)

            Mass_X.append(mx)
            Mass_Y.append(my)

        elif my+100==mx:
            my = my-40
            fname   = "/STORE/ferencek/TRSM_XToHY_6b/2017/13TeV/NANOAOD/TRSM_XToHY_6b_M3_{0}_M2_{1}_NANOAOD.root".format(mx,my)
            oFile   = "{0}_{1}".format(mx,my)
            boosted_fatjets = boosted(fname,oFile,processLabel="MX{0}_MY{1}".format(mx,my),eventsToRead=None)
            boosted_efficiency = ak.num(boosted_fatjets,axis=0)/100
            boosted_eff.append(boosted_efficiency)

            semiboosted_fatjets = semiboosted(fname,oFile,processLabel="MX{0}_MY{1}".format(mx,my),eventsToRead=None)
            semiboosted_efficiency = ak.num(semiboosted_fatjets[1],axis=0)/100
            semiboosted_eff.append(semiboosted_efficiency)

            Mass_X.append(mx)
            Mass_Y.append(my)

print("boosted_eff = ", boosted_eff)
print("semiboosted_eff = ", semiboosted_eff)
print("Mass_X = ",Mass_X )
print("Mass_Y = ",Mass_Y )

fig, ax = plt.subplots()
ax.set_aspect("equal")
hist, xbins, ybins, im = ax.hist2d(Mass_X, Mass_Y, bins=11,weights=boosted_eff)
ax.set_title("Boosted Efficiency(%)", fontsize = 20)
ax.set_xlabel('X mass', size = 15)
ax.set_ylabel('Y mass', size = 15)
for i in range(len(ybins)-1):
    for j in range(len(xbins)-1):
        ax.text(xbins[j]+200,ybins[i]+200, round(hist.T[i,j],2),color="blue", ha="center", va="center", fontweight="bold")
fig.set_size_inches(10.5, 10.5)
fig.show()
fig.savefig('Boosted_Eff.png', dpi=100)

fig, ax = plt.subplots()
ax.set_aspect("equal")
hist, xbins, ybins, im = ax.hist2d(Mass_X, Mass_Y, bins=11,weights=semiboosted_eff)
ax.set_title("SemiBoosted Efficiency(%)", fontsize = 20)
ax.set_xlabel('X mass', size = 15)
ax.set_ylabel('Y mass', size = 15)
for i in range(len(ybins)-1):
    for j in range(len(xbins)-1):
        ax.text(xbins[j]+200,ybins[i]+200, round(hist.T[i,j],2), color="blue", ha="center", va="center", fontweight="bold")
fig.set_size_inches(10.5, 10.5)
fig.show()
fig.savefig('SemiBoosted_Eff.png', dpi=100)

combined = []
for (i,j) in zip(boosted_eff,semiboosted_eff):
    combined.append(i+j)

fig, ax = plt.subplots()
ax.set_aspect("equal")
hist, xbins, ybins, im = ax.hist2d(Mass_X, Mass_Y, bins=11,weights=(combined))
ax.set_title("Combined Efficiency(%)", fontsize = 20)
ax.set_xlabel('X mass', size = 15)
ax.set_ylabel('Y mass', size = 15)
for i in range(len(ybins)-1):
    for j in range(len(xbins)-1):
        ax.text(xbins[j]+200,ybins[i]+200, round(hist.T[i,j],2), color="blue", ha="center", va="center", fontweight="bold")
fig.set_size_inches(10.5, 10.5)
fig.show()
fig.savefig('Combined_Eff.png', dpi=100)

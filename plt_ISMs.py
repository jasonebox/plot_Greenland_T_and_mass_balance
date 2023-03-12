#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 06:35:25 2023

@author: jason box, GEUS, jeb@geus.dk

https://zenodo.org/record/3939037#.ZA1jruzMIQ-

Variables per file:

scalars_mm_cr_GIS ----------------- Greenland wide numbers 

oarea - assumed ocean area [m2]
rhof - model specific freshwater density [kg m-3]
rhoi - model specific ice density [kg m-3]
rhow - model specific ocean water density [kg m-3]

time - time, typically in days since X
iarea - Fraction of grid cell covered by land ice [1]
iareagr - Fraction of grid cell covered by grounded ice sheet
iareafl - Fraction of grid cell covered by ice sheet flowing over seawater

ivol - ice volume [m3]
ivolgr - grounded ice volume [m3]
ivolfl - floating ice volume [m3]
ivaf - ice volume above flotation [m3]

lim - ice mass [kg]
limgr - grounded ice mass [kg]
limfl - floating ice mass [kg]
limaf - ice mass above flotation [kg]

sle - sea-level equivalent mass [m] !! decreases with mass loss !! 
smb - spatially integrated surface mass balance anomaly [kg s-1]


scalars_rm_cr_GIS ----------------- IMBIE2-Rignot basins xx=[no,ne,se,sw,cw,nw]

oarea - assumed ocean area [m2]
rhof - model specific freshwater density [kg m-3]
rhoi - model specific ice density [kg m-3]
rhow - model specific ocean water density [kg m-3]

time - time, typically in days since X
ivaf_xx - ice volume above flotation [m3]
smb_xx - spatially integrated surface mass balance anomaly [kg s-1]
limaf_xx - ice mass above flotation [kg]
sle_xx - sea-level equivalent mass [m] !! decreases with mass loss !! 


scalars_zm_cr_GIS ----------------- IMBIE2-Zwally basins xx=[z11,z12,z13,z14,z21,z22,z31,z32,z33,z41,z42,z43,z50,z61,z62,z71,z72,z81,z82]

oarea - assumed ocean area [m2]
rhof - model specific freshwater density [kg m-3]
rhoi - model specific ice density [kg m-3]
rhow - model specific ocean water density [kg m-3]

time - time, typically in days since X
ivaf_xx - ice volume above flotation [m3]
smb_xx - spatially integrated surface mass balance anomaly [kg s-1]
limaf_xx - ice mass above flotation [kg]
sle_xx - sea-level equivalent mass [m] !! decreases with mass loss !! 


"""
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from glob import glob

# plot settings
th=2 # line thickness
formatx='{x:,.3f}' ; fs=16
plt.rcParams["font.size"] = fs
plt.rcParams['axes.facecolor'] = 'w'
plt.rcParams['axes.edgecolor'] = 'k'
plt.rcParams['axes.grid'] = False
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.8
plt.rcParams['grid.color'] = "#cccccc"
plt.rcParams["legend.facecolor"] ='w'
plt.rcParams["mathtext.default"]='regular'
plt.rcParams['grid.linewidth'] = th/2
plt.rcParams['axes.linewidth'] = 1
plt.rcParams['figure.figsize'] = 12, 20

path_ISM='/Users/jason/Dropbox/NREE/Goelzer/v7_CMIP5_pub/'

# data reader
def get_ISM(path_ISM,institution,model,run):
    fn=path_ISM+institution+'/'+model+'/'+run+'_05/scalars_mm_GIS_'+institution+'_'+model+'_'+run+'.nc' ; print(fn)
    ds=xr.open_dataset(fn)
    # list(ds.keys())
    if institution!='IMAU':
        x=pd.to_datetime(ds.indexes['time'].to_datetimeindex())
    else:
        x=pd.to_datetime(ds.time.values)
        x=np.array(x.strftime('%Y').astype(int))
        
    sle=ds.sle.values*-1000 # convert to mm sea level rise units

    return(x,sle)

# obtain lists
runs=['historical','ctrl_proj']

paths = sorted(glob(path_ISM+'*'))
institutions=[]
for path in paths:
    institutions.append(path.split('/')[-1])

# --------- figure settings
fig, ax = plt.subplots(figsize=(10, 6))

colors=['r','b','k']
linestyles=['-','--']

for institution in institutions:
    # if institution=='UCIJPL':
    # if institution=='IMAU':
    if institution=='AWI':
        paths = sorted(glob(path_ISM+institution+'/*'))
        models=[]
        for path in paths:
            models.append(path.split('/')[-1])
        for j,model in enumerate(models):
            for i,run in enumerate(runs):
                x,sle=get_ISM(path_ISM,institution,model,run)
                if i==0: # historical
                    sle=sle-sle[-1]
                    temp=sle
                if i==1: # projection
                    sle=sle-sle[0]+temp[-1]
                # plot result
                plt.plot(x,sle,color=colors[j],linestyle=linestyles[i],label=institution+' '+model+' '+run)

        plt.ylabel('mm eustatic SLE')
        plt.title('Greenland ice sea level contribution after Goelzer et al 2020')
        plt.legend()
        
        ly='p'
        
        if ly =='p':
            DPI = 150
            figpath='/Users/jason/Dropbox/NREE/Goelzer/Figs/'
            figname=figpath+institution+'_historical_ctrl_proj.png'
            plt.savefig(figname, bbox_inches='tight', dpi=DPI)
            # os.system('open '+figname)
                
        if ly == 'x':
            plt.show()

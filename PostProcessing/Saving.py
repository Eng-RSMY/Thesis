#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 08:21:14 2019

@author: Sergio Ribeiro
Description: Module to store simulation Saving Parameters
"""
import os
import csv
import sys
sys.path.append(os.path.abspath('.'))
from PostProcessing.Plotting import *

class Paths():
    def __init__(self):
        # Main Directories
        self.geopath = './PreProcessing/Geometry/'
        self.meshpath = './PreProcessing/Mesh/'
        self.postpath = './PostProcessing/Cases/'
        self.imagespath = '/Images/'
        self.parapath = '/Paraview/'
    
def assemblePaths(inputs):
    
    mainPaths = Paths()
    # Subdirectories where image and paraview Results are saved
    imagespath = mainPaths.imagespath
    parapath = mainPaths.parapath
    postpath = mainPaths.postpath
    
    # Full Paths Definition
    paraFullPath = postpath+inputs.caseId+parapath
    imFullPath = postpath+inputs.caseId+imagespath

    # Main Directories
    geopath = mainPaths.geopath
    meshpath = mainPaths.meshpath
    postpath = mainPaths.postpath
    
    return meshpath, paraFullPath, imFullPath,parapath, imagespath,geopath,  \
    postpath

def createDirectories(inputs):
    meshpath, paraFullPath, imFullPath,parapath, imagespath, geopath, \
    postpath = assemblePaths(inputs)
    
    # Get Existing Cases
    caseList=[]
    for case in os.listdir(postpath):
        caseList.append(case)
    
    if not(any(inputs.caseId == casei for casei in caseList)):
        print('New Case')
        os.mkdir(postpath+inputs.caseId)
        os.mkdir(paraFullPath)
    elif os.path.exists(paraFullPath):
        print('Case Overwritten')
        ## Clear Old Result Files from Case
        for fileName in os.listdir(paraFullPath):
            os.remove(os.path.join(paraFullPath,fileName))
    else:
        os.mkdir(paraFullPath)
        
    if not(os.path.exists(imFullPath)):
        os.mkdir(imFullPath)

def createCSVOutput(outputCSV,fieldnames, delimiter = ','):
    with open(outputCSV, 'w') as writeFile:
        writer = csv.DictWriter(writeFile, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()

def writeCSVLine(outputCSV,line):
    with open(outputCSV, 'a') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(line) 

def savingCheckings(inputs,mainPaths):    
    meshFile = inputs.meshFile;
    caseId = inputs.caseId;
    
    meshpath, paraFullPath, imFullPath,parapath, imagespath,geopath,  \
    postpath = assemblePaths(inputs)
    
    # Check Result Folders exist, and create them
    if not os.path.exists(meshpath):
        raise ValueError('Directory '+meshpath+' does not exist.')
    else:
        count = 0
        meshFile = ''
        for fname in os.listdir(meshpath):
            if fname.endswith('.xml'):
                count+=1
                if len(meshFile)==0 or len(fname) < len(meshFile):
                    meshFile = fname
        if count < 1:
            raise ValueError('No mesh files in '+meshpath+' directory')
        elif count == 3:
            return
        else:
            raise ValueError(meshpath+ \
            ' directory must contain exactly three files with .XML extension.')
    
    
def savingPreparation(paraFullPath,ParaViewFilenames):
    from dolfin import File
    
    # Create New Result Files (Paraview Files: .pvd)
    fileNames = []
    paraFiles = []
    for i in range(0,len(ParaViewFilenames)): # ParaViewFilenames defined in Problem Imputs
        fileNames.append(ParaViewFilenames[i]+".pvd")
        paraFiles.append(File(paraFullPath+fileNames[i]))

    return paraFiles

def saveResults(results,paraFiles,ParaViewFilenames,ParaViewTitles):
    # Save Data for Paraview
    for i in range(0,len(results)):
        # Rename output Titles
        results[i].rename(ParaViewFilenames[i],ParaViewTitles[i])
        paraFiles[i] << results[i]

def logResults(t,results,listId,inputs,meshObj,cbarU=0,cbarP=0):
    # Save Data into CSV to later plot
    outletFlowRate = results[3]
    line = [t,outletFlowRate]
    
    writeCSVLine(inputs.outputCSV,line)
    if listId < len(inputs.plotTimeList) and t >= inputs.plotTimeList[listId]:
        ui = results[0]
        pi = results[1]
        ci = results[2]
        dicTitle = {1:'Pressure',2:'Concentration',3:'Velocity'}
        cbarU, cbarP, uXYValues, lValues, pValues, nVertices = prettyplot(1,meshObj,t,ui,pi,ci,dicTitle, resultspath='./PostProcessing/Cases/'+inputs.caseId,tag='/Images/',cbarU=cbarU,cbarP=cbarP,cbarDirection = 0)
        listId += 1

    return cbarU, cbarP, listId
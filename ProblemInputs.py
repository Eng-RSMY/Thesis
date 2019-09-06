#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 08:21:14 2019

@author: Sergio Ribeiro
Description: Problem Definitions: Input Dictionary
"""
from dolfin import *
import math

# Sigmoid Function S(x) = (dtMax-dtMin)/(1+exp(Inclination*(-t+t0)))+dtMin
def dynamicTimestep(t,dtMax,dtMin,t0): 
    Inclination = 3
    return (dtMax-dtMin)/(1+math.exp(Inclination*(-t+t0)))+dtMin

def autoTimestep(no_iterations,dt,inputs,limitIterations=3,increment=2):
    # Check if 
    if no_iterations < limitIterations:
        dt = min(increment*dt,inputs.dtMax)
    else:
        dt = max((1/increment)*dt,inputs.dtMin)
    
    return dt

class Inputs():
    def __init__(self):
        #%%############ Case Definition    ##############################
        self.caseId = 'TransAdvectedInterf_ReinitShortTest' ## If name already exists in folder ./PostProcessing/Cases, 
                         ## old data will be overwritten.
        
        # Output Variables
        self.ParaViewFilenames = []; self.ParaViewTitles = []
        self.ParaViewFilenames.append("velocity"); self.ParaViewTitles.append('Velocity (m/s)')
        self.ParaViewFilenames.append("pressure"); self.ParaViewTitles.append('Pressure (Pa)')
        self.ParaViewFilenames.append("concentration"); self.ParaViewTitles.append('Mass Fraction (Fluid Tags)')
        
        #%%############ Gravitationa Field ##############################
        # Gravity Acceleration (m/s²)
        self.g = 9.81
        
        #%%############ Fluids' Properties ##############################
        # Tags
        self.FluidTags = [0,1]
                
        # Density (kg/m³)
        self.rho_values = [1000, 1000]
        
        # Initial Interface position
        self.InterfaceX0 = 0.05
        # self.InterfaceY0 = 0.01
        
        # Diffusity of Between species (m²/s)
        self.D = 0.0000001
        
        # Rheology
        # Newtonian Viscosity (Pa.s)
        self.mu_values = [0.2, 0.02]
        
        #%%############ Time Parameters #################################
        # Start Time
        self.t0 = 0 # s
        
        # Simulation Time
        self.tEnd = 50 # s
        
        # Variable time step
        self.dtMin = 0.1    # s
        self.dtMax = 10  # s
        self.tChange = 0   # point in time of sigmoid inflection occurs (s)
        self.dt = 1
#        self.dt = dynamicTimestep(self.t0,self.dtMax,self.dtMin,self.tChange)    # s
        
        #%%############ Logging Options   ###############################
        # Result Saving time step
        self.savedt = 1 # s
        
        #%%############ Problem Geometry   ##############################
        ## Mesh File
        self.meshFile = 'MacroParallelPlates'
        ## Mesh Elements
        # Velocity
        self.velocityElementfamily = 'Lagrange'
        self.velocityElementOrder = 2
        # Pressure
        self.pressureElementfamily = 'Lagrange'
        self.pressureElementOrder = 1
        # Advected Scalar Field
        self.scalarFieldElementfamily = 'Lagrange'
        self.scalarFieldElementOrder = 1
        
        #%%############ Boundary Conditions
        
        ## No slip Boundaries
        self.noSlipBCs = []
        self.noSlipBCs.append('TopWall')
        self.noSlipBCs.append('BottomWall')
        #noSlipBoundaries.append('InnerWalls')
        
        ## Pressure Inputs
        self.pressureBCs = {}
        self.pressureBCs.update({'Inlet' : 0.1}) # Pa
        self.pressureBCs.update({'Outlet' : 0}) # Pa
        
        ## Advected Scalar Field Inputs
        self.scalarFieldBCs = {}
        self.scalarFieldBCs.update({'Inlet' : Constant(self.FluidTags[0])}) # % of Fluid 0
        #self.scalarFieldBCs.update({'TopWall': self.TTopWall}) # T
        
        ## Velocity Inputs
        self.velocityBCs = []
        #velocityBCs.update({'Inlet' : Constant(5.0)}) # m/s
        
        #%%############ Solver parameters ###############################
        # Absolute Tolerance    
        self.absTol = 1e-12
        
        # Relative Tolerance
        self.relTol = 1e-10
        
        # Maximum Iterations
        self.maxIter = 200
        
        # Linear Solver
        self.linearSolver = 'mumps'
            
        # Relaxation Factors
        self.alpha = 1
        self.alphaC = 1
            
        #%% Possible Solvers
        # Solver method  |  Description    
        # -----------------------------------------------------------
        # bicgstab       |  Biconjugate gradient stabilized method                      
        # cg             |  Conjugate gradient method                                   
        # default        |  default linear solver                                       
        # gmres          |  Generalized minimal residual method                         
        # minres         |  Minimal residual method                                     
        # mumps          |  MUMPS (MUltifrontal Massively Parallel Sparse direct Solver)
        # petsc          |  PETSc built in LU solver                                    
        # richardson     |  Richardson method                                           
        # superlu        |  SuperLU                                                     
        # tfqmr          |  Transpose-free quasi-minimal residual method                
        # umfpack        |  UMFPACK (Unsymmetric MultiFrontal sparse LU factorization) 
        #
        # LU method  |  Description                                                 
        # --------------------------------------------------------------------------
        # default    |  default LU solver                                           
        # mumps      |  MUMPS (MUltifrontal Massively Parallel Sparse direct Solver)
        # petsc      |  PETSc built in LU solver                                    
        # superlu    |  SuperLU                                                     
        # umfpack    |  UMFPACK (Unsymmetric MultiFrontal sparse LU factorization) 
        #
        # Krylov method  |  Description                                 
        # --------------------------------------------------------------
        # bicgstab       |  Biconjugate gradient stabilized method      
        # cg             |  Conjugate gradient method                   
        # default        |  default Krylov method                       
        # gmres          |  Generalized minimal residual method         
        # minres         |  Minimal residual method                     
        # richardson     |  Richardson method                           
        # tfqmr          |  Transpose-free quasi-minimal residual method
        # 
        # 
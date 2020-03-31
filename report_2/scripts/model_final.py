# -*- coding: utf-8 -*-
"""Policy Priority Inference for Sustainable Development

Authors: Omar A. Guerrero & Gonzalo Castañeda
Written in Pyhton 3.7
Acknowledgments: This product was developed through the sponsorship of the
    United Nations Development Programme (bureau for Latin America) 
    and with the support of the National Laboratory for Public Policies (Mexico City), 
    the Centro de Investigación y Docencia Económica (CIDE, Mexico City), 
    and The Alan Turing Institute (London).

This file contains all the necessary functions to reproduce the analysis presented
in the methodological and technical reports. The accompanying data can be 
obtained from the public repository: https://github.com/oguerrer/PPI4SD. 
There are two functions in this script:
    
    run_ppi : the main function that simulates the policymaking process and
    generates synthetic development-indicator data.
    get_targets : a support function to transform a collection of series 
    where one or more targets are less or equals to the initial value of the series.

Further information can be found in each function's code.


Example
-------
To run PPI in a Python script, just add the following line:

    tsI, tsC, tsF, tsP, tsD, tsS, ticks, H = run_ppi(I0, T)
    
This will simulate the policymaking process for initial values I0 and targets T.
This example assumes no network of spillovers. All other arguments can be
passed as explained in the function run_ppi.


Rquired external libraries
--------------------------
- Numpy


"""

# import necessary libraries
from __future__ import division, print_function
import numpy as np
import copy
import warnings
warnings.simplefilter("ignore")


def run_ppi(I0, T, A=None, alpha=.1, phi=.5, tau=.5, R=None, 
            gov_func=None, P0=None, H0=None, PF=None, pf=1, RD=None, 
            B=1., bs=None, betas=None, beta=1., tolerance=1e-3, node=None, time=None):
    """Function to run one simulation of the Policy Priority Inference model.

    Parameters
    ----------
        I0: numpy array 
            Initial values of the development indicators.
        T: numpy array 
            Target values for development indicators. These values represent 
            the government's goals or aspirations. For a retrospective analysis, 
            it is usually assumed that the targets correspond to the final values 
            of the series. They should be higher than I0 or the model will not 
            converge.
        A:  2D numpy array
            The adjacency matrix of the spillover network of development 
            indicators. If not given, the model assumes a zero-matrix, so there 
            are no spillovers.
        alpha: float, optional
            A vector of growth factors in (0,1).
        phi: float, optional
            Scalar in [0,1] or numpy array (a vector) with values in [0,1] that 
            represent the quality of the government's monitoring mechanisms.
        tau: float, optional 
            Scalar in [0,1] or numpy array (a vector) with values in [0,1] that 
            represent the quality of the rule of law.
        R: numpy array, optional
            Binary vector indicating which nodes are instrumental (value 1) and 
            which are not (value 0). If not provided, it is assumed that all
            nodes are instrumental (a vector of ones).
        gov_func: python function, optional
            A custom function that that returns the policy priority of the government
        P0: numpy array, optional
            An array with the initial allocation profile.
        H0: numpy array, optional
            The initial vector of historical inefficiencies
        PF: numpy array, optional
            An exogenous vector of policy priorities.
        pf: float, optional
            The probability with which the exogenous priorities are followed
            each period. It must be in [0,1].
        RD: numpy array, optional
            A vector indicating the level of fiscal rigidity of each instrumental
            indicator. RD should be provided together with PF, and each element 
            of RD should be at most as big as the corresponding element in PF.
        B: float, optional
            A factor for the overall size of the total budget.
            It should only be used in counterfactual analysis where the baseline
            estimation has a B=1, so if B=0.9, it means that the overall budget
            for transformative resources shrinked 10% with respect to the
            baseline estimation.
        b: numpy array, optional
            A vector with expenditure factors.
        tolerance: float, optional
            The precision to consider that an indicator has reached its goal.
            Unless you understand very well how PPI works, this should not be
            changed.
        
    Returns
    -------
        tsI: 2D numpy array
            Matrix with the time series of the simulated indicators. Each column 
            corresponds to a simulation step.
        tsC: 2D numpy array
            Matrix with the time series of the simulated contributions. Each column 
            corresponds to a simulation step.
        tsF: 2D numpy array 
            Matrix with the time series of the simulated agents' benefits. Each column 
            corresponds to a simulation step.
        tsP: 2D numpy array 
            Matrix with the time series of the simulated resource allocations. 
            Each column corresponds to a simulation step.
        tsD: 2D numpy array 
            Matrix with the time series of the simulated inefficiencies. Each column 
            corresponds to a simulation step.
        tsS: 2D numpy array 
            Matrix with the time series of the simulated spillovers. Each column 
            corresponds to a simulation step.
        ticks: numpy array
            A vector with the simulation step in which each indicator reached its target.
        H: numpy array
            A vector with historical inefficiencies,
    """
       
    N = len(I0) # number of indicators
    
    # transform indicators of instrumental variables into boolean types
    if R is None:
        R = np.ones(N).astype(bool)
    else:
        R[R!=1] = 0
        R = R.astype(bool)
    Rnum = np.sum(R)
    
    # if no network is provided, create a zero-matrix
    if A is None:
        A = np.zeros((N,N))
    else:
        A = copy.deepcopy(A)
        np.fill_diagonal(A, 0)
    
    n = np.sum(R) # number of instrumental nodes
    
    tsI = [] # stores time series of indicators
    tsC = [] # stores time series of contributions
    tsF = [] # stores time series of benefits
    tsP = [] # stores time series of allocations
    tsD = [] # stores time series of corruption
    tsX = [] # stores time series of actions
    tsS = [] # stores time series of spillovers
    tsb = [] # stores time series of exogenous budget
    
    qs = np.ones(n) # propensities to allocate resources (initially homogeneous)
    pp = np.random.rand(n) # random initial allocation profile
    P = B*pp/np.sum(pp) # vector of allocations (initially homogeneous)
    C = np.random.rand(n)*P # vector of contributions
    F = np.random.rand(n) # vector of benefits
    Ft = np.random.rand(n) # vectors of lagged benefits
    I = copy.deepcopy(I0) # vector of indicators
    It = np.random.rand(N)*I0 # vector of lagged indicators
    X = np.random.rand(n)-.5 # vector of actions
    Xt = np.random.rand(n)-.5 # vector of lagged actions
    H = 1 + np.random.rand(n) # vector of historical inefficiencies
    signt = np.sign(np.random.rand(n)-.5) # vector of previous signs for directed learning
    changeFt = np.random.rand(n)-.5 # vector of changes in benefits
    gaps0 = T-I0 # initial target-indicator gaps
    b = np.ones(Rnum)
    
    step = 1 # iteration counter
    ticks = np.ones(N) # simulation period in which each indicator reaches its target
    
    # in case the user provides initial allocation or historical inefficiencies
    if P0 is not None:
        P = P0/P0.sum()
    if H0 is not None:
        H = H0
    
    if PF is not None:
        P = B*PF/PF.sum()
        
#    if Y is not None:
#        Y = B*Y/Y.sum()
        
    if bs is None:
        bs = np.ones(Rnum)
    
    if betas is None:
        betas = np.ones(N)
    betas = copy.deepcopy(betas)
    betas[~R] = 0
    
    if PF is not None:
        PF = copy.deepcopy(PF)
        PF[PF==0] = 1e-12
        P = B*PF/PF.sum()
    
    finish = False # a flag to halt the simulation (activates when all indicators reach their targets)
    while not finish: # iterate until the flag indicates otherwise
        
        step += 1 # increase counter
        tsI.append(copy.deepcopy(I)) # store this period's indicators
        tsP.append(copy.deepcopy(P)) # store this period's allocations
#        tsY.append(copy.deepcopy(Y)) # store this period's engogenous allocations
        tsb.append(copy.deepcopy(b)) # store this period's exogenous allocation

        deltaIAbs = I-It # change of all indicators
        deltaIIns = deltaIAbs[R] # change of instrumental indicators
        
        # relative change of instrumental indicators
        if np.sum(deltaIIns) == 0:
            deltaIIns = np.zeros(len(deltaIIns))
        else:
            deltaIIns = deltaIIns/np.sum(np.abs(deltaIIns))
        

        ### DETERMINE CONTRIBUTIONS ###
        
        changeF = F - Ft # absolute change in benefits
        changeX = X - Xt # absolute change in actions
        sign = np.sign(changeF*changeX) # sign for the direction of the next action
        changeF[changeF==0] = changeFt[changeF==0] # if the benefit did not change, keep the last change
        sign[sign==0] = signt[sign==0] # if the sign is undefined, keep the last one
        Xt = copy.deepcopy(X) # update lagged actions
        X = X + sign*np.abs(changeF) # determine current action
        C = P/(1 + np.exp(-X)) # map action into contribution
        signt = copy.deepcopy(sign) # update previous signs
        changeFt = copy.deepcopy(changeF) # update previous changes in benefits
        
        tsC.append(copy.deepcopy(C)) # store this period's contributions
        tsD.append(copy.deepcopy(P-C)) # store this period's inefficiencies
        tsF.append(copy.deepcopy(F)) # store this period's benefits
        tsX.append(copy.deepcopy(X)) # store this period's actions
        
        
        ### DETERMINE BENEFITS ###
        
        D = P-C # update inefficiencies
        pp = 1/(1 + np.exp(-(D-D.min())/(D.max()-D.min()) - .5)) # social norm factor
        trial = (np.random.rand(n) < phi * pp) # monitoring outcomes
        theta = trial.astype(float) # indicator function of uncovering inefficiencies
        H[theta==1] += P[theta==1] - C[theta==1] # accumulate spotted inefficiencies
        newF = deltaIIns*C/P + (1-theta*tau)*(P-C)/P # compute benefits
        Ft = copy.deepcopy(F) # update lagged benefits
        F = newF # update benefits
        
        
        ### DETERMINE INDICATORS ###
        
        deltaM = np.array([deltaIAbs,]*len(deltaIAbs)).T # reshape deltaIAbs into a matrix
        S = np.sum(deltaM*A, axis=0) # compute spillovers
        tsS.append(S) # save spillovers
        gaps = T-I # current target-indicator gaps
        cnorm = np.zeros(N) # initialize a zero-vector to store the normalized contributions
        cnorm[R] = C # compute contributions only for instrumental nodes
        gammas = ( beta*B + betas*cnorm )/(1 + np.exp(-S/(np.mean(gaps/gaps0))) ) # compute probability of succesful growth
        succsess = (np.random.rand(N) < gammas).astype(int) # determine if there is succesful growrth
        newI = I + (T-I) * alpha * succsess # compute new indicators
        It = copy.deepcopy(I) # update lagged indicators
        I =  copy.deepcopy(newI) # update indicators
        
        
        ### DETERMINE ALLOCATIONS ###
        
        if PF is None:
        
            gap = gaps[R] # target-indicator gaps of instrumental indicators
            gap = (gap - gap.min())/(gap.max() - gap.min()) # normalize gaps
            gap = gap*(1-1e-6) + 1e-12 # make sure all gaps are greater than zero
            
            # normalize historical inefficiencies
            if np.sum(H==1) < n:
                hist = (H-H.min())/(H.max()-H.min())
            else:
                hist = np.zeros(n)
            hist = hist*(1-1e-6) + 1e-12 # make sure all elements are greater than zero
            
#            gap *= bs
            qs = gap**(1+hist) / np.sum(gap**(1+hist))
            qs_hat = qs**bs
            
            # check if exogenous priorities are given
            P = B*qs_hat/qs_hat.sum()
        
        else:
            
            P = B*PF/PF.sum()


        # update convergence ticks
        converged = np.abs(T-I) < tolerance
        ticks[~converged] = step
#        print(S[[43,44]])
#        if S[43] == 0:
#            break
        
        # check if all indicators have converged
        if converged.sum() == N:
            finish = True
            
#        if node is not None and time is not None and step-time > 5:
#            finish = True
            
        
    return np.array(tsI).T, np.array(tsC).T, np.array(tsF).T, np.array(tsP).T, np.array(tsD).T, np.array(tsS).T, ticks, H



    

def get_targets(series):
    """Transforms a collection of series where one or more targets are less or
    equals to the initial value of the series.

    Parameters
    ----------
        series: numpy 2D array 
            A matrix containing the time series of each indicator. Each row
            corresponds to a series and each column to a period.
        
    Returns
    -------
        I0: numpy array
            The initial values of each series.
        T: numpy array 
            The transformed targets (final values) of each series.
    """
    
    gaps = series[:,-1]-series[:,0]
    I0 = series[:,0]
    if np.sum(gaps<0) > 0:
        T = series[:,-1] + np.abs(np.min(gaps)) + max([np.min(gaps[gaps>0]), .01])
    elif np.min(gaps) < .01:
        T = series[:,-1] + .01
    else:
        T = series[:,-1]
    
    return I0, T





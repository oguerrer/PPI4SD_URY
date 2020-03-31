
# import necessary libraries
from __future__ import division, print_function
import numpy as np
import copy
from joblib import Parallel, delayed
import scipy.optimize as opt
import scipy.stats as st
import pickle as pk

# the model_final.py file should be in the same folder
from model_final import * 




############################
#                          #
# SIMULTANEOUS CALIBRATION #
#                          #
############################



def run_sim(I0, T, A, R, alphas, phi, tau, B, bs, betas, beta, sample_size):
    all_tsP = []
    all_times = []
    for intera in range(sample_size):
        outputs = run_ppi(I0, T, A=A, alpha=alphas, R=R, phi=phi, tau=tau, B=B, bs=bs, betas=betas, beta=beta)
        tsI, tsC, tsF, tsP, tsD, tsS, times, H = outputs
        all_tsP.append(tsP)
        all_times.append(times)
    all_times = np.array(all_times).T
    times = all_times.mean(axis=1)
    P = np.mean([Ps[:,1::].mean(axis=1) for Ps in all_tsP], axis=0)
    return times, P


def wrap_b(b, I0, T, A, R, alphas, phi, tau, Pb, B, bs, betas, beta, sample_size, node):
    est_bs = copy.deepcopy(bs)
    est_bs[node] = b
    times, P = run_sim(I0, T, A, R, alphas, phi, tau, B, est_bs, betas, beta, sample_size)
    error = np.abs(P[node] - Pb[node])/2
    return error


def wrap_alpha(alpha, I0, T, A, R, alphas, phi, tau, B, bs, betas, beta, sample_size, node, steps):
    est_alphas = copy.deepcopy(alphas)
    est_alphas[node] = alpha
    times, P = run_sim(I0, T, A, R, est_alphas, phi, tau, B, bs, betas, beta, sample_size)
    error = np.abs(times[node] - steps)
    return error


def search_b(I0, T, A, R, alphas, phi, tau, Pb, B, bs, betas, beta, sample_size, node, bounds):
    sol = opt.minimize_scalar(wrap_b, args=(I0, T, A, R, alphas, phi, tau, Pb, B, bs, betas, beta, sample_size, node), bounds=bounds, method='Bounded')
    return sol.x


def search_alpha(I0, T, A, R, alphas, phi, tau, B, bs, betas, beta, sample_size, node, steps):
    sol = opt.minimize_scalar(wrap_alpha, args=(I0, T, A, R, alphas, phi, tau, B, bs, betas, beta, sample_size, node, steps), bounds=[0,1], method='Bounded')
    return sol.x


def sim_cal(I0, T, A, R, alphas, phi, tau, Pb, B, bs, betas, beta, sample_size, node, steps, bounds_b, correct_alpha, correct_b):
    R_indis = dict( zip(np.where(R==1)[0], range(R.sum())) )
    
    if node not in R_indis:
        if correct_alpha:
            return [search_alpha(I0, T, A, R, alphas, phi, tau, B, bs, betas, beta, sample_size, node, steps)]
        else:
            return [alphas[node]]
    else:
        if correct_b:
            best_b = search_b(I0, T, A, R, alphas, phi, tau, Pb, B, bs, betas, beta, sample_size, R_indis[node], bounds_b)
        else:
            best_b = bs[R_indis[node]]
        if correct_alpha:
            best_alpha = search_alpha(I0, T, A, R, alphas, phi, tau, B, bs, betas, beta, sample_size, node, steps)
        else:
            best_alpha = alphas[node]
        
        return [best_alpha, best_b]
           
    
def multi_cal(I0, T, A, R, alphas, phi, tau, Pb, B, bs, betas, beta, sample_size, steps, bounds_b, parallel_processes, to_correct_alpha, to_correct_b):
    nodes = list(range(len(I0)))
    R_indis = dict( zip(np.where(R==1)[0], range(R.sum())) )
    bound_b = [bounds_b[R_indis[node]] if R[node]==1 else [0,1] for node in nodes]
    
    solutions = np.array(Parallel(n_jobs=parallel_processes, verbose=0)(delayed(sim_cal)(I0, T, A, R, alphas, phi, tau, Pb, B, bs, betas, beta, sample_size, node, steps, bound_b[node], to_correct_alpha[node], to_correct_b[node]) for node in nodes))
    
    alphas_sol = []
    bs_sol = []
    
    for sol in solutions:
        alphas_sol.append(sol[0])
        if len(sol) == 2:
            bs_sol.append(sol[1])
        
    return np.array(alphas_sol), np.array(bs_sol)


def estimate(I0, T, A, R, alphas, phi, tau, Pb, B, bs, betas, beta, 
             sample_size, steps, parallel_processes, tol_alpha, tol_b,
             path=None):
    error_alpha, error_b = 100, 100
    alphas_sol = copy.deepcopy(alphas)
    bs_sol = copy.deepcopy(bs)
    bounds_b = [[0, 1] for b in bs]
    to_correct_alpha = np.ones(len(T)) == 1
    to_correct_b = R == True
    
    while error_alpha > tol_alpha or error_b > tol_b:
        alphas_sol, bs_sol = multi_cal(I0, T, A, R, alphas_sol, phi, tau, 
                                       Pb, B, bs_sol, betas, beta, sample_size, steps, 
                                       bounds_b, parallel_processes, to_correct_alpha, to_correct_b)
        bounds_b = [[.75*b, 1.25*b] for b in bs_sol]
        times, P = run_sim(I0, T, A, R, alphas_sol, phi, tau, B, bs_sol, betas, beta, sample_size)
        
        error_by_node_alpha = np.abs(times - steps)
        to_correct_alpha = error_by_node_alpha > tol_alpha
        error_alpha = error_by_node_alpha.mean()
        
        error_by_node_b = np.abs(P/P.sum() - Pb/Pb.sum())/2
        to_correct_b[np.where(R)[0]] = error_by_node_b > tol_b/R.sum()
        error_b = error_by_node_b.sum()
        
        
        print('Trying number of steps', steps)
        print('Error alpha:', error_alpha, 'Error b:', error_b)
        
        if path is not None:
            all_outs = {'alphas':alphas_sol, 'steps':steps, 'bs':bs_sol}
            ff = open(path+'/calibrated_inter_'+str(int(100*error_alpha))+'_'+str(int(100*error_b))+'.pk', 'wb')
            pk.dump(all_outs, ff)
            ff.close()
        
    return alphas_sol, bs_sol
        

def find_steps(I0, T, A, R, alphas, phi, tau, Pb, B, bs, betas, beta, sample_size, steps, 
               parallel_processes, tol_alpha, tol_b, vola_emp):
    cont_T = True
    rec_alphas = []
    rec_volas = []
    rec_bs = []
    rec_steps = []
    
    est_alphas = np.ones(len(I0))
    est_bs = np.ones(R.sum())
    
    while cont_T:
        
        est_alphas, est_bs = estimate(I0, T, A, R, est_alphas, phi, tau, Pb, B, est_bs, betas, beta,
                                        sample_size, steps, parallel_processes, tol_alpha, tol_b)
        
        all_tsI = []
        for intera in range(sample_size):
            outputs = run_ppi(I0, T, A=A, alpha=est_alphas, R=R, phi=phi, tau=tau, B=B, bs=est_bs, betas=betas, beta=beta)
            tsI, tsC, tsF, tsP, tsD, tsS, times, H = outputs
            all_tsI.append(tsI)
        
        nchs_sim_dist = []
        for ts in all_tsI:
            chs_sim = ts[:,1:]-ts[:,0:-1]
            nchs_sim_dist += chs_sim.flatten().tolist()
        est_vola = np.std(nchs_sim_dist)
        
        
        rec_alphas.append(est_alphas)
        rec_bs.append(est_bs)
        rec_volas.append(est_vola)
        rec_steps.append(steps)
        
        print('Difference in volatility:', est_vola - vola_emp)
        
        steps += 1
        if est_vola < vola_emp:
            cont_T = False
            
    return rec_alphas, rec_bs, rec_volas, rec_steps































































from functions import *
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import scipy.stats as sc
import matplotlib.patches as mpatches
import pandas as pd
import matplotlib.pylab as pylab

params = {'axes.labelsize': 14,
         'axes.titlesize':16}
pylab.rcParams.update(params)

fig_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..', 'Figures','tmp_figs'))

print("------------------------------------")
print("          Parameter recovery")
print("------------------------------------")

cpt_parameter_recovery_files = ['parameter_recovery_CPT_chunk_1.mat', 'parameter_recovery_CPT_chunk_2.mat','parameter_recovery_CPT_chunk_3.mat']
cpt_ground_truth_file         = "Choices_simulated_from_CPT.mat"

LML_parameter_recovery_files = ['parameter_recovery_LML_chunk_1.mat','parameter_recovery_LML_chunk_2.mat','parameter_recovery_LML_chunk_3.mat']

x = np.linspace(0,1,300)
n_chunks = len(cpt_parameter_recovery_files)

show_cpt   = True
show_lml   = True
show_plots = True

A      = [0,1,2,3]
marker = ['^','s','o','v']
color  = ['r','b','g','m']

if show_cpt:
    print("\n\n------------------------------------")
    print("Evaluating CPT data...")
    print("---\n")
    print("Reading output...")

    beta_cpt  = [None]*n_chunks
    delta_cpt = [None]*n_chunks
    gamma_cpt = [None]*n_chunks
    for c in range(n_chunks):
        _,beta_cpt[c],   delta_cpt[c],   gamma_cpt[c]    = read_output(cpt_parameter_recovery_files[c],'parameter_recovery')
    _,beta_cpt_true,delta_cpt_true,gamma_cpt_true = read_output(cpt_ground_truth_file,'parameter_recovery')

    n_agents = np.shape(beta_cpt[0])[0]
    n_samples = np.shape(beta_cpt[0])[1]
    n_chains = np.shape(beta_cpt[0])[2]

    print('---')
    print(f"Number of agents = {n_agents}")
    print(f"Number of chains = {n_chains}")
    print(f"Number of samples = {n_samples}")
    print(f"Number of chunks = {n_chunks}")
    print('---')

    #--------delta----------#
    print("\nProcessing Delta...")
    map_agent_cpt_delta = [None]*n_chunks
    for c in range(n_chunks):
        _,map_agent_cpt_delta[c] = process_params(delta_cpt[c], n_agents, n_chains, n_samples, output="map")
        corr,_ = sc.pearsonr(map_agent_cpt_delta[c],delta_cpt_true[:,0,0])
        print(f"Pearson correlation coefficient for Delta in chunk {c+1}: {corr:.3f}")

    plt.figure()
    # plt.suptitle("True delta vs estimated delta",fontsize=18)
    colors = ['b','r','g']
    for c in range(n_chunks):
        for i in range(n_agents):
            if i in A:
                plt.scatter(delta_cpt_true[i,0,0],map_agent_cpt_delta[c][i], marker=marker[i], edgecolor=colors[c], facecolors='none', s=80)
            else:
                plt.scatter(delta_cpt_true[i,0,0],map_agent_cpt_delta[c][i], marker='x', c=colors[c], s=80)
            plt.ylim([0,1.8])
            plt.xlim([0,1.8])
        #Dummies for legend
        plt.scatter(10,10,c=colors[c],label=f"Chunk {c+1}", marker=">")
    plt.scatter(10,10, facecolors='none',label=" ")
    plt.scatter(10,10,label="Agent 1", marker=marker[0], edgecolor='k', facecolors='none')
    plt.scatter(10,10,label="Agent 2", marker=marker[1], edgecolor='k', facecolors='none')
    plt.scatter(10,10,label="Agent 3", marker=marker[2], edgecolor='k', facecolors='none')
    plt.scatter(10,10,label="Agent 4", marker=marker[3], edgecolor='k', facecolors='none')
    plt.scatter(10,10,marker='x',c='k',label="Agents 5-10")
    plt.xlabel("$\\delta_{'Ground-truth'}$")
    plt.ylabel("$\delta_e$")
    plt.legend(loc='upper left')
    plt.savefig(os.path.join(fig_path,"results-cpt-delta.png"))

    #--------gamma----------#
    print("\nProcessing Gamma...")
    map_agent_cpt_gamma = [None]*n_chunks
    for c in range(n_chunks):
        _,map_agent_cpt_gamma[c] = process_params(gamma_cpt[c], n_agents, n_chains, n_samples, output="map")
        corr,_ = sc.pearsonr(map_agent_cpt_gamma[c],gamma_cpt_true[:,0,0])
        print(f"Pearson correlation coefficient for Gamma in chunk {c+1}: {corr:.3f}")

    plt.figure()
    colors = ['b','r','g']
    # plt.suptitle("True gamma vs estimated gamma",fontsize=18)
    for c in range(n_chunks):
        for i in range(n_agents):
            # plt.subplot(1,2,1)
            if i in A:
                plt.scatter(gamma_cpt_true[i,0,0],map_agent_cpt_gamma[c][i], marker=marker[i], edgecolor=colors[c], facecolors='none', s=80)
            else:
                plt.scatter(gamma_cpt_true[i,0,0],map_agent_cpt_gamma[c][i], marker='x', c=colors[c], s=80)
            plt.ylim([0,1.8])
            plt.xlim([0,1.8])
        #Dummies for legend
        plt.scatter(10,10,c=colors[c],label=f"Chunk {c+1}", marker=">")
    plt.scatter(10,10, facecolors='none',label=" ")
    plt.scatter(10,10,label="Agent 1", marker=marker[0], edgecolor='k', facecolors='none')
    plt.scatter(10,10,label="Agent 2", marker=marker[1], edgecolor='k', facecolors='none')
    plt.scatter(10,10,label="Agent 3", marker=marker[2], edgecolor='k', facecolors='none')
    plt.scatter(10,10,label="Agent 4", marker=marker[3], edgecolor='k', facecolors='none')
    plt.scatter(10,10,marker='x',c='k',label="Agents 5-10")
    plt.xlabel("$\\gamma_{'Ground-truth'}$")
    plt.ylabel("$\gamma_e$")
    plt.legend(loc='upper left')
    plt.savefig(os.path.join(fig_path,"results-cpt-gamma.png"))

    # #--------PW----------#
    print("\nProcessing w...")
    plt.figure()
    colors = ['b','r','g']
    # plt.suptitle("Estimated delta vs estimated gamma",fontsize=18)
    for c in range(n_chunks):
        for i in range(n_agents):
            # plt.subplot(1,2,1)
            if i in A:
                plt.scatter(map_agent_cpt_gamma[c][i],map_agent_cpt_delta[c][i], marker=marker[i], edgecolor=colors[c], facecolors='none', s=80)
            else:
                plt.scatter(map_agent_cpt_gamma[c][i],map_agent_cpt_delta[c][i], marker='x', c=colors[c], s=80)
            plt.xlim([0,1.8])
            plt.ylim([0,1.8])
        #Dummies for legend
        plt.scatter(10,10,c=colors[c],label=f"Chunk {c+1}", marker=">")
    plt.scatter(10,10, facecolors='none',label=" ")
    plt.scatter(10,10,label="Agent 1", marker=marker[0], edgecolor='k', facecolors='none')
    plt.scatter(10,10,label="Agent 2", marker=marker[1], edgecolor='k', facecolors='none')
    plt.scatter(10,10,label="Agent 3", marker=marker[2], edgecolor='k', facecolors='none')
    plt.scatter(10,10,label="Agent 4", marker=marker[3], edgecolor='k', facecolors='none')
    plt.scatter(10,10,marker='x',c='k',label="Agents 5-10")
    plt.ylabel("$\\delta_e$")
    plt.xlabel("$\gamma_e$")
    plt.legend(loc='upper right')
    plt.savefig(os.path.join(fig_path,"results-cpt-params.png"))
  
    w_1_diff = []
    w_2_diff = []
    w_3_diff = []

    for i in range(n_agents): #agents
        plt.figure(figsize=(12,15))
        plt.suptitle(f"Probability Weighting function for CPT-Agent {i+1}", fontsize=18)
        w_true = cpt_weighting_function(x, delta_cpt_true[i,0,0], gamma_cpt_true[i,0,0])
        w = [None]*n_chunks
        for c in range(n_chunks):
            plt.subplot(3,2,(c*2)+1)
            if c == 0: plt.title("Parameter space", fontsize=14)
            plt.scatter(map_agent_cpt_gamma[c][i],map_agent_cpt_delta[c][i], edgecolor='b', facecolors='none', marker='^', label="Estimated", s=100)
            plt.scatter(gamma_cpt_true[i,0,0],delta_cpt_true[i,0,0], edgecolor='r',facecolor='none', label="'Ground truth'", s=100)
            
            plt.xlim([0,1.8])
            plt.ylim([0,1.8])
            plt.ylabel("$\\delta$")
            plt.xlabel("$\\gamma$")
            plt.legend(prop={'size':8}, markerscale=0.7)
           
            w[c] = cpt_weighting_function(x, map_agent_cpt_delta[c][i],map_agent_cpt_gamma[c][i])

            if c == 0: 
                w_1_diff.append([a_i - b_i for a_i, b_i in zip(w_true,w[c])])
            elif c == 1:
                w_2_diff.append([a_i - b_i for a_i, b_i in zip(w_true,w[c])])
            else:
                w_3_diff.append([a_i - b_i for a_i, b_i in zip(w_true,w[c])])

            plt.subplot(3,2,(c*2)+2)
            if c == 0: plt.title("Weighting function", fontsize=14)
            plt.plot(x,w[c], 'b--', label="Estimated")
            plt.plot(x,w_true, 'r-.', label="'Ground truth'")
            plt.plot(x,x,'k-', label="No weighting")
            plt.xlabel("$\hat{p}(x)$",fontsize=14)
            plt.ylabel("$w(x)$",fontsize=14)
            plt.legend(loc='upper left', prop={'size':8})

        plt.subplots_adjust(wspace=0.3,hspace=0.3)
        plt.savefig(os.path.join(fig_path,f"results-cpt-w-agent{i+1}.png"))

    diff = [w_1_diff,w_2_diff,w_3_diff]
    fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(7,10))
    plt.setp(ax, xticks=[0, 150, 300], xticklabels=['0', '0.5', '1'], yticks=[-0.1, 0, 0.1])
    for c in range(n_chunks):
        df = pd.DataFrame(diff[c])
        df = pd.melt(frame = df, var_name = '$\hat{p}(x)$', value_name = '$\hat{p}(x)-w(x)$')
        sns.lineplot(ax = ax[c],data = df,ci=95,x = '$\hat{p}(x)$', y = '$\hat{p}(x)-w(x)$')
        ax[c].collections[0].set_label('95 pct. confidence interval')
        ax[c].hlines(y=0, xmin=0, xmax=len(x), color='k', linestyle='--')
        ax[c].set_title(f"Chunk {c+1}", fontsize = 14)
        ax[c].legend(loc='upper left')
        ax[c].set_ylim([-0.1,0.1])
        plt.tight_layout()
    plt.savefig(os.path.join(fig_path,"results-cpt-difference.png"))

#-------------------------------------------------------------------------------------------------------------
#--------------------------------LML--------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------

if show_lml:
    print("\n\n------------------------------------")
    print("Evaluating LML data...")
    print("---\n")
    print("Reading output...")

    beta_lml = [None]*n_chunks
    delta_lml = [None]*n_chunks
    gamma_lml = [None]*n_chunks
    for c in range(n_chunks):
        _,beta_lml[c],   delta_lml[c],   gamma_lml[c]    = read_output(LML_parameter_recovery_files[c],'parameter_recovery')

    n_agents = np.shape(beta_lml[0])[0]
    n_samples = np.shape(beta_lml[0])[1]
    n_chains = np.shape(beta_lml[0])[2]

    print('---')
    print(f"Number of agents = {n_agents}")
    print(f"Number of chains = {n_chains}")
    print(f"Number of samples = {n_samples}")
    print('---')

    #--------delta----------#
    print("\nProcessing Delta...")
    map_agent_lml_delta = [None]*n_chunks
    for c in range(n_chunks):
        _,map_agent_lml_delta[c] = process_params(delta_lml[c], n_agents, n_chains, n_samples, output="map")

    #--------gamma----------#
    print("\nProcessing Gamma...")
    map_agent_lml_gamma = [None]*n_chunks
    for c in range(n_chunks):
        _,map_agent_lml_gamma[c] = process_params(gamma_lml[c], n_agents, n_chains, n_samples, output="map")

    #--------PW----------#
    print("\nProcessing w...")
    colors = ['b','r','g']
    plt.figure()
    # plt.suptitle("Estimated delta vs estimated gamma", fontsize=18)
    for c in range(n_chunks):
        for i in range(n_agents):
            if i in A:
                plt.scatter(map_agent_lml_gamma[c][i],map_agent_lml_delta[c][i], marker=marker[i], edgecolor=colors[c], facecolors='none', s=50)
            else:
                plt.scatter(map_agent_lml_gamma[c][i],map_agent_lml_delta[c][i], marker='x', c=colors[c], s=50)
        plt.scatter(10,10,c=colors[c],label=f"Chunk {c+1}", marker=">")
    plt.ylabel("$\\delta_e$")
    plt.xlabel("$\gamma_e$")
    plt.xlim([0.7,1.05])
    plt.ylim([0.9,1.05])
    plt.scatter(10,10, facecolors='none',label=" ")
    plt.scatter(10,10, marker=marker[0], edgecolor='k', facecolors='none', label=f"Agent 1")
    plt.scatter(10,10, marker=marker[1], edgecolor='k', facecolors='none', label=f"Agent 2")
    plt.scatter(10,10, marker=marker[2], edgecolor='k', facecolors='none', label=f"Agent 3")
    plt.scatter(10,10, marker=marker[3], edgecolor='k', facecolors='none', label=f"Agent 4")
    plt.scatter(10,10,marker='x',c='k',label="Agents 5-10")
    plt.legend(loc='upper right')
    plt.savefig(os.path.join(fig_path,"results-lml-params.png"))

    w_1_diff = []
    w_2_diff = []
    w_3_diff = []

    chunk_len = [10,50,100]
    w_true = [None]*n_chunks
    for c in range(n_chunks):
        w_true[c] = lml_weighting_function(x,chunk_len[c])
    colors = ['b','r','g']
    for i in range(n_agents): #agents
        plt.figure(figsize=(12,15))
        plt.suptitle(f"Probability Weighting function for LML-Agent {i+1}", fontsize=18)
        w = [None]*n_chunks
        for c in range(n_chunks):
            plt.subplot(3,2,(c*2)+1)
            if c == 0: plt.title(f"Parameter space",fontsize=14)
            plt.scatter(map_agent_lml_gamma[c][i],map_agent_lml_delta[c][i], edgecolor='b', facecolors='none', marker='^', label="Estimated", s=100)
            plt.xlim([0.7,1.05])
            plt.ylim([0.9,1.05])
            plt.ylabel("$\\delta$")
            plt.xlabel("$\\gamma$")
            plt.legend(loc='upper left', prop={'size':8}, markerscale=0.7)

            w[c] = cpt_weighting_function(x, map_agent_lml_delta[c][i],map_agent_lml_gamma[c][i])

            if c == 0: 
                w_1_diff.append([a_i - b_i for a_i, b_i in zip(w_true[c],w[c])])
            elif c == 1:
                w_2_diff.append([a_i - b_i for a_i, b_i in zip(w_true[c],w[c])])
            else:
                w_3_diff.append([a_i - b_i for a_i, b_i in zip(w_true[c],w[c])])

            plt.subplot(3,2,(c*2)+2)
            if c == 0: plt.title("Weighting function", fontsize=14)
            plt.plot(x,w[c], 'b--', label="Estimated")
            plt.plot(x,w_true[c],'r-.', label="Predicted")
            plt.plot(x,x,'k-', label = "No weighting")
            plt.xlabel("$\hat{p}(x)$")
            plt.ylabel("$w(x)$")
            plt.legend(loc='upper left', prop={'size':8})
        plt.subplots_adjust(wspace=0.3,hspace=0.3)
    plt.savefig(os.path.join(fig_path,f"results-lml-w-agent{i+1}.png"))

    diff = [w_1_diff,w_2_diff,w_3_diff]
    fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(7,10))
    plt.setp(ax, xticks=[0, 150, 300], xticklabels=['0', '0.5', '1'], yticks=[-0.01, 0, 0.01])
    for c in range(n_chunks):
        df = pd.DataFrame(diff[c])
        df = pd.melt(frame = df, var_name = '$\hat{p}(x)$', value_name = '$\hat{p}(x)-w(x)$')
        sns.lineplot(ax = ax[c],data = df,ci=95,x = '$\hat{p}(x)$', y = '$\hat{p}(x)-w(x)$')
        ax[c].collections[0].set_label('95 pct. confidence interval')
        ax[c].hlines(y=0, xmin=0, xmax=len(x), color='k', linestyle='--')
        ax[c].set_title(f"Chunk {c+1}", fontsize=14)
        ax[c].legend(loc='upper left')
        plt.tight_layout()
    plt.savefig(os.path.join(fig_path,"results-LML-difference.png"))

    plt.show()
if show_plots:
    print("\nPlotting...")
    plt.show()

print("------------------------------------")
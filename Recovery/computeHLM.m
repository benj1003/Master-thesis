function computeHLM(nBurnin,nSamples,nThin,nChains,whichJAGS,mode,doParallel,nGambles,nAgents)

%% Hiercharchical Latent Mixture (HLM) model
% This is a general script for running several types of hierarchical
% bayesian model via JAGS. It can run hiearchical latent mixture models in
% which different utility models can be compared via inference on the model
% indicator variables, and it can run without latent mixtures of models for
% instance in order to estimate parameters of a given utility model. It
% takes as input the following:

% nBurnin - a number which specifies how many burn in samples to run.
% nThin - a number specifying the thinnning number
% nChains - number of chains
% mode - a numbber identifying which part of the analysis to run


%% Set paths
[startDir,~] = fileparts(mfilename('fullpath'));%specify your starting directory here (where this script runs from)
cd(startDir);%move to starting directory
jagsDir=[startDir,'/JAGS'];
addpath(fullfile(pwd,'/matjags'));%set path to include matjags folder
addpath(fullfile(pwd,'/data'));%set path to include data folder
addpath(fullfile(pwd,'/samples_stats'));%set path to include samples_stats folder

%% Set bounds of hyperpriors

switch mode
    case {1,2}
        %beta - prior on log since cannot be less than 0; note same bounds used for independent priors on all models
        muLogBetaL=-2.3;muLogBetaU=3.4; %bounds on mean of distribution log beta
        sigmaLogBetaL=0.01;sigmaLogBetaU=1.60;%bounds on the std of distribution of log beta
        
        %Alpha - prior set by dirac function to 1
        muLogAlphaL=-0.01;muLogAlphaU=0.01;%bounds on mean of distribution of log Alpha
        sigmaLogAlphaL=0.01;sigmaLogAlphaU=0.02;%bounds on std of distribution of log Alpha

        %Delta - prior on mean set by dirac function to 0.5
        muLogDeltaL=-0.21;muLogDeltaU=-0.19;%bounds on mean of distribution of log Delta
        sigmaLogDeltaL=0.49;sigmaLogDeltaU=0.50; %bounds on std of distribution of log Delta

        %Gamma - prior on mean set by dirac function to 0.4
        muLogGammaL=-0.81;muLogGammaU=-0.79;%bounds on mean of distribution of log Gamma
        sigmaLogGammaL=0.49;sigmaLogGammaU=0.50; %bounds on std of distribution of log Gamma
       
    case {3}
        %beta - prior on log since cannot be less than 0; note same bounds used for independent priors on all models
        muLogBetaL=-2.3;muLogBetaU=3.4; %bounds on mean of distribution log beta
        sigmaLogBetaL=0.01;sigmaLogBetaU=1.60;%bounds on the std of distribution of log beta
        
        %Alpha - prior set by dirac function to 1
        muLogAlphaL=-0.01;muLogAlphaU=0.01;%bounds on mean of distribution of log Alpha
        sigmaLogAlphaL=0.01;sigmaLogAlphaU=0.02;%bounds on std of distribution of log Alpha

        %Delta - prior on mean set by dirac function to 0.5
        muLogDeltaL=-0.21;muLogDeltaU=-0.19;%bounds on mean of distribution of log Delta
        sigmaLogDeltaL=0.49;sigmaLogDeltaU=0.50; %bounds on std of distribution of log Delta

        %Gamma - prior on mean set by dirac function to 1.5
        muLogGammaL=0.49;muLogGammaU=0.5;%bounds on mean of distribution of log Gamma
        sigmaLogGammaL=0.19;sigmaLogGammaU=0.20; %bounds on std of distribution of log Gamma

    case {4,5,6,7,8,9}
        %beta - prior on log since cannot be less than 0; note same bounds used for independent priors on all models
        muLogBetaL=-2.3;muLogBetaU=3.4; %bounds on mean of distribution log beta
        sigmaLogBetaL=0.01;sigmaLogBetaU=1.60;%bounds on the std of distribution of log beta
        
        %Alpha - prior set by dirac function to 1
        muLogAlphaL=-0.01;muLogAlphaU=0.01;%bounds on mean of distribution of log Alpha
        sigmaLogAlphaL=0.01;sigmaLogAlphaU=0.02;%bounds on std of distribution of log Alpha

        %Delta - prior on log since cannot be less than 0
        muLogDeltaL=-2.3;muLogDeltaU=0;%bounds on mean of distribution of log Delta
        sigmaLogDeltaL=0.01;sigmaLogDeltaU=1.60;%bounds on std of distribution of log Delta

        %Gamma - prior on log since cannot be less than 0
        muLogGammaL=-2.3;muLogGammaU=0;%bounds on mean of distribution of log Gamma
        sigmaLogGammaL=0.01;sigmaLogGammaU=1.60;%bounds on std of distribution of log Gamma
end

%% Set key variables

switch mode
    case {1,2,3,4,5,6}
        nTrials = [100];
    case {7,8,9}
        nTrials = [10,50,100];
end
doDIC=0;%compute Deviance information criteria? This is the hierarchical equivalent of an AIC, the lower the better

for trial_n = 1:length(nTrials)
    
%% Choose & load data    
switch mode
    case 1 %simulate choices with CPT
        dataSource = 'all_gambles';
        modelName = 'JAGS_CPT';
        outputName = 'Choices_simulated_from_CPT'; 
        running = 'Simulating choices from CPT';
        nSamples = 1;
        nChains = 1;
        
    case 2 %simulate choices with LML
        dataSource = 'all_gambles';
        modelName = 'JAGS_LML';
        outputName = 'Choices_simulated_from_LML';
        running = 'Simulating choices from LML';
        nSamples = 1;
        nChains = 1;
        
    case 3 %simulate choices with CPT regular-S
        dataSource = 'all_gambles';
        modelName = 'JAGS_CPT';
        outputName = 'Choices_simulated_from_CPT_regular_S';
        running = 'Simulating choices from CPT-regular-S';
        nSamples = 1;
        nChains = 1;
        
    case 4 %Model comparison on data from CPT
        dataSource = sprintf('Choices_simulated_from_CPT');
        modelName = 'JAGS';
        outputName = 'model_comparison_CPT'; 
        running = 'Model recovery on choices from CPT species';
        pz=[1/2,1/2];
        load('all_gambles');

    case 5 %Model comparison on data from LML
        dataSource = sprintf('Choices_simulated_from_LML');
        modelName = 'JAGS';
        outputName = 'model_comparison_LML'; 
        running = 'Model recovery on choices from LML species';
        pz=[1/2,1/2];
        load('all_gambles');
        
    case 6 %Model comparison on data from CPT regular-S
        dataSource = sprintf('Choices_simulated_from_CPT_regular_S');
        modelName = 'JAGS';
        outputName = 'model_comparison_CPT_regular_S'; 
        running = 'Model recovery on choices from CPT (Regular-S) species';
        pz=[1/2,1/2];
        load('all_gambles');
        
    case 7 %parameter recovery for CPT data
        dataSource = sprintf('Choices_simulated_from_CPT');
        outputName = 'parameter_recovery_CPT';
        modelName = 'JAGS_CPT';
        running = 'Parameter recovery on choices from CPT species';
        load('all_gambles');
        
    case 8 %parameter recovery for LML data
        dataSource = sprintf('Choices_simulated_from_LML');
        outputName = 'parameter_recovery_LML';
        modelName = 'JAGS_CPT';
        running = 'Parameter recovery on choices from LML species';
        load('all_gambles');
        
    case 9 %parameter recovery for CPT (regular-S) data
        dataSource = sprintf('Choices_simulated_from_CPT_regular_S');
        outputName = 'parameter_recovery_CPT_regular_S';
        modelName = 'JAGS_CPT';
        running = 'Parameter recovery on choices from CPT species';
        load('all_gambles');
end

load(dataSource)
%% Print information for user
disp('**************');
disp([running]);
disp(['With ',modelName]);
disp(['started: ',datestr(clock)]);
disp(['running on: ',dataSource]);
disp([sprintf('With %.0f Trials',nTrials(trial_n))])
disp('**************');
%% Initialise matrices
%initialise matrices with nan values of size subjects x conditions x trials
choice = nan(nAgents,nGambles,nTrials(trial_n)); %initialise choice data matrix 
dx1 = nan(nAgents,nGambles,nTrials(trial_n)); dx2 = dx1; dx3 = dx1; dx4=dx1;%initialise changes in wealth
p_a1  = nan(nAgents,nGambles,nTrials(trial_n)); p_b1 = p_a1; %initialise channges in 'probabilities'

%% Compile choice & gamble data
%split into chunks for parameter recovery (mode 5 and 6)
trialInds=1:nTrials(trial_n);%generate indices for each trial
switch mode
    case {1,2,3} %simulating choices
        for i = 1:nAgents
            for g = 1:nGambles
                
                choice(i,g,trialInds)=Data{g,i}.Choice(trialInds);%assign to temporary variables

                dx1(i,g,trialInds)=Data{g,i}.maxA(trialInds);%assign changes in wealth dx for outcome 1 (note same amount for all trials)
                dx2(i,g,trialInds)=Data{g,i}.minA(trialInds);%same for outcome 2 etc.
                dx3(i,g,trialInds)=Data{g,i}.maxB(trialInds);
                dx4(i,g,trialInds)=Data{g,i}.minB(trialInds);

                p_a1(i,g,trialInds)=Data{g,i}.p_maxA(trialInds);%assign changes in 'probability' for outcome 1
                p_b1(i,g,trialInds)=Data{g,i}.p_maxB(trialInds);
            end
        end    
           
    case {4,5,6,7,8,9} %Recovery
        for i = 1:nAgents
            for g = 1:nGambles %nChunks = 1
                choice(i,g,trialInds)=samples.y(1,1,i,g,trialInds);%assign to temporary variables

                dx1(i,g,trialInds)=Data{g,i}.maxA(trialInds);%assign changes in wealth dx for outcome 1 (note same amount for all trials)
                dx2(i,g,trialInds)=Data{g,i}.minA(trialInds);%same for outcome 2 etc.
                dx3(i,g,trialInds)=Data{g,i}.maxB(trialInds);
                dx4(i,g,trialInds)=Data{g,i}.minB(trialInds);

                p_a1(i,g,trialInds)=Data{g,i}.p_maxA(trialInds);%assign changes in 'probability' for outcome 1
                p_b1(i,g,trialInds)=Data{g,i}.p_maxB(trialInds);
            end 
        end
end
%% Configure data structure for graphical model & parameters to monitor
%everything you want JAGS to use
switch mode
    case {1,2,3} %Simulating choices
        dataStruct = struct(...
            'nAgents', nAgents,'nGambles',nGambles,'nTrials',nTrials(trial_n),...
            'dx1',dx1,'dx2',dx2,'dx3',dx3,'dx4',dx4,...
            'pa1',p_a1,'pb1',p_b1,...
            'muLogBetaL',muLogBetaL,'muLogBetaU',muLogBetaU,'sigmaLogBetaL',sigmaLogBetaL,'sigmaLogBetaU',sigmaLogBetaU,...
            'muLogAlphaL',muLogAlphaL,'muLogAlphaU',muLogAlphaU,'sigmaLogAlphaL',sigmaLogAlphaL,'sigmaLogAlphaU',sigmaLogAlphaU,...
            'muLogDeltaL',muLogDeltaL,'muLogDeltaU',muLogDeltaU,'sigmaLogDeltaL',sigmaLogDeltaL,'sigmaLogDeltaU',sigmaLogDeltaU,...
            'muLogGammaL',muLogGammaL,'muLogGammaU',muLogGammaU,'sigmaLogGammaL',sigmaLogGammaL,'sigmaLogGammaU',sigmaLogGammaU);
               
    case {4,5,6} %Model Recovery
        dataStruct = struct(...
            'nAgents', nAgents,'nGambles',nGambles,'nTrials',nTrials(trial_n),'y',choice,...
            'dx1',dx1,'dx2',dx2,'dx3',dx3,'dx4',dx4,...
            'pa1',p_a1,'pb1',p_b1,...
            'muLogBetaL',muLogBetaL,'muLogBetaU',muLogBetaU,'sigmaLogBetaL',sigmaLogBetaL,'sigmaLogBetaU',sigmaLogBetaU,...
            'muLogAlphaL',muLogAlphaL,'muLogAlphaU',muLogAlphaU,'sigmaLogAlphaL',sigmaLogAlphaL,'sigmaLogAlphaU',sigmaLogAlphaU,...
            'muLogDeltaL',muLogDeltaL,'muLogDeltaU',muLogDeltaU,'sigmaLogDeltaL',sigmaLogDeltaL,'sigmaLogDeltaU',sigmaLogDeltaU,...
            'muLogGammaL',muLogGammaL,'muLogGammaU',muLogGammaU,'sigmaLogGammaL',sigmaLogGammaL,'sigmaLogGammaU',sigmaLogGammaU,...
            'pz',pz);
        
    case {7,8,9} %Parameter Recovery
        dataStruct = struct(...
            'nAgents', nAgents,'nGambles',nGambles,'nTrials',nTrials(trial_n),'y',choice,...
            'dx1',dx1,'dx2',dx2,'dx3',dx3,'dx4',dx4,...
            'pa1',p_a1,'pb1',p_b1,...
            'muLogBetaL',muLogBetaL,'muLogBetaU',muLogBetaU,'sigmaLogBetaL',sigmaLogBetaL,'sigmaLogBetaU',sigmaLogBetaU,...
            'muLogAlphaL',muLogAlphaL,'muLogAlphaU',muLogAlphaU,'sigmaLogAlphaL',sigmaLogAlphaL,'sigmaLogAlphaU',sigmaLogAlphaU,...
            'muLogDeltaL',muLogDeltaL,'muLogDeltaU',muLogDeltaU,'sigmaLogDeltaL',sigmaLogDeltaL,'sigmaLogDeltaU',sigmaLogDeltaU,...
            'muLogGammaL',muLogGammaL,'muLogGammaU',muLogGammaU,'sigmaLogGammaL',sigmaLogGammaL,'sigmaLogGammaU',sigmaLogGammaU);
end
%everything you want JAGS to monitor
for i = 1:nChains
    switch mode  
        case {1,3}  %Simulating choices
            monitorParameters = {'y',...
                'alpha_pt','gamma_pt','delta_pt','beta_pt'};
            S=struct; init0(i)=S; %sets initial values as empty so randomly seeded

        case {2}
            monitorParameters = {'y'};
            S=struct; init0(i)=S; %sets initial values as empty so randomly seeded

        case {4,5,6}  %Model recovery
            monitorParameters = {'z'};
            S=struct; init0(i)=S; %sets initial values as empty so randomly seeded

        case {7,8,9}  %Parameter recovery
            monitorParameters = {'alpha_pt','gamma_pt','delta_pt','beta_pt'};
            S=struct; init0(i)=S; %sets initial values as empty so randomly seeded
    end
end
%% Run JAGS sampling via matJAGS
tic;
fprintf( 'Running JAGS ...\n' ); % start clock to time % display

[samples, stats] = matjags( ...
    dataStruct, ...                           % Struct that contains all relevant data
    fullfile(jagsDir, [modelName '.txt']), ...% File that contains model definition
    init0, ...                                % Initial values for latent variables
    whichJAGS,...                             % Specifies which copy of JAGS to run on
    'doparallel' , doParallel, ...            % Parallelization flag
    'nchains', nChains,...                    % Number of MCMC chains
    'nburnin', nBurnin,...                    % Number of burnin steps
    'nsamples', nSamples, ...                 % Number of samples to extract
    'thin', nThin, ...                        % Thinning parameter
    'dic', doDIC, ...                         % Do the DIC?
    'monitorparams', monitorParameters, ...   % List of latent variables to monitor
    'savejagsoutput' , 1 , ...                % Save command line output produced by JAGS?
    'verbosity' , 1 , ...                     % 0=do not produce any output; 1=minimal text output; 2=maximum text output
    'cleanup' , 0 ,...                        % clean up of temporary files?
    'rndseed',1);                             % Randomise seed; 0=no; 1=yes

disp('\n**************');
toc % end clock

%% Save stats and samples
disp('saving samples and stats...')
switch mode
    case {1,2,3,4,5,6}
        save(['samples_stats\',outputName],'stats','samples','-v7.3')
    case {7,8,9}
        save(['samples_stats\',sprintf('%s_Chunk_%.0f',outputName,trial_n)],'stats','samples','-v7.3')
end
disp('**************');

%% Print readouts
disp('stats:'),disp(stats)%print out structure of stats output
disp('samples:'),disp(samples);%print out structure of samples output

end %end wrapping of chunks
end
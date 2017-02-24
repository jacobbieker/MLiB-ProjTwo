%% Load the hidden markov model (hardcoded)
%Transitional probability
T= [0.990971 0.009029 0.000000; 0.023083 0.953090 0.023827; 0.000000 0.013759 0.986241];

%Emission probability
E= [0.043601 0.011814 0.053446 0.065541 0.049508 0.049789 0.054571 0.024191 0.055977 0.035162 0.103235 0.045007 0.029536 0.048101 0.075105 0.059634 0.068354 0.016315 0.067792 0.043319;
0.102010 0.019360 0.009680 0.011914 0.033507 0.103500 0.118392 0.003723 0.000745 0.039464 0.138496 0.014147 0.011914 0.026806 0.067014 0.012658 0.073716 0.037230 0.119136 0.056590;
0.082374 0.008415 0.059345 0.059345 0.069973 0.031001 0.049159 0.019043 0.081045 0.025244 0.068202 0.047830 0.032772 0.052259 0.073959 0.086802 0.056244 0.007086 0.062445 0.027458];

%Initial probability
I= [0.496359 0.188095 0.315546];

%% Decoding using an algorithm for each state

%Setting up constants
index = 0;
pp = 0;

%State 1
i = 1
p = log(I(i))*log(E(i,1))
for ii = 2:20
    p = p * log(T(i+1,i))*log(E(i,ii))
    if p > pp
        pp = p
        index = i
    end
end

%State 2
i = 2
p = log(I(i))*log(E(i,1))
for ii = 2:20
    p = p * log(T(1,i))*log(T(3,i))*log(E(i,ii))
    if p > pp
        pp = p
        index = i
    end
end

%State 3
i = 3
p = log(I(i))*log(E(i,1))
for ii = 2:20
    p = p * log(T(i-1,i))*log(E(i,ii))
    if p > pp
        pp = p
        index = i
    end
end

switch index
    case 1
        index = 'inside'
    case 2
        index = 'membrane'
    case 3
        index = 'outside'
end
    
fprintf('The most likely state which the observables are in is in state "%s"', index)

%% Decoding using an overall algorithm

%Setting up constants
index = 0;
pp = 0;

for i = 1:size(E,1)
    p = I(i)*E(i,1) 
    for ii = 2:20
        p = p * T(i,i+1)*E(i,ii)
    end
    if p > pp
        pp = p
        index = i
    end
end

switch index
    case 1
        index = 'inside'
    case 2
        index = 'membrane'
    case 3
        index = 'outside'
end
    
fprintf('The most likely state which the observables are in is in state "%s"', index)

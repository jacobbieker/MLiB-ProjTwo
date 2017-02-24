import csv
import os
import numpy as np

emissions_table = []
transitions_table = []
hidden = []
pi_table = []
observables = []
observables_to_index = {}
index_to_states = {}
with open(os.path.join("data","hmm-tm.txt")) as hidden_markov:
    reader = csv.reader(hidden_markov, delimiter=" ")
    # Hacky way to do it, but can't think of a better way right now
    hidden_flag = 0
    observe_flag = 0
    pi_flag = 0
    transition_flag = 0
    emission_flag = 0
    transition_index = 0
    emission_index = 0

    for line in reader:
        if hidden_flag:
            hidden = line
            index = 0
            for element in line:
                index_to_states[index] = element
                index += 1
            hidden_flag = 0
            transitions_table = []
            pi_table = []
        elif observe_flag:
            observables = line
            index = 0
            for element in line:
                # Convert to an index for accessing lists and arrays easier
                observables_to_index[element] = index
                index += 1
            observe_flag = 0
            emissions_table = []
        elif pi_flag:
            for element in line:
                pi_table.append(float(element))
            pi_flag = 0
        elif transition_flag:
            temp_line = [float(i) for i in line]
            transitions_table.append(temp_line)
            transition_index += 1
            if transition_index >= len(hidden):
                transition_flag = 0
        elif emission_flag:
            temp_line = [float(i) for i in line]
            emissions_table.append(temp_line)
            emission_index += 1
            if emission_index >= len(hidden):
                emission_flag = 0


        if "hidden" in line:
            hidden_flag = 1
        elif "observables" in line:
            observe_flag = 1
        elif "pi" in line:
            pi_flag = 1
        elif "transitions" in line:
            transition_flag = 1
        elif "emissions" in line:
            emission_flag = 1

################################### Finish converting HMM file into Python objects ####################################

sequences = []
sequence_names = []
spot = 1
with open(os.path.join("data", "test-sequences-project2.txt")) as sequence_data:
    seq_reader = csv.reader(sequence_data, delimiter=" ")
    for line in sequence_data:
        if ">" in line:
            sequence_names.append(line.split(">")[1])
            spot = 1
        elif spot == 1:
            sequences.append(line.strip())
            spot = 0

for index, item in enumerate(sequences):
    seq1 = item
    print("The test sequence: " + str(sequence_names[index]))
    print(seq1)

    # remapping of sequence to a list of numbers, so it can be easily
    # accessed as an index in an array
    sequence_index = [observables_to_index[observation] for observation in seq1]

    # Creation of the ω table:
    # Setting all the values to -inf for if the value is 0 in log space, should be -inf
    omega_table = [len(pi_table) * [float("-inf")] for index in range(len(sequence_index))]

    # Calculation of the 1st column of the ω table , which is the basis for the recursion of the algorithm:
    for j in range(len(pi_table)):
        omega_table[0][j] = np.log(pi_table[j]) + np.log(emissions_table[j][sequence_index[0]])

    # Calculation of the rest of the ω table:
    for n in range(1,len(sequence_index)):
        for k in range(len(hidden)):
            transition_value = float("-inf")
            if emissions_table[k][sequence_index[n]]!=0.0 and emissions_table[k][sequence_index[n]] != float("-inf"):
                for j in range(len(hidden)):
                    if transitions_table[j][k]!=0.0 and transitions_table[j][k] != float("-inf") :
                        if omega_table[n-1][j] + np.log(transitions_table[j][k]) > transition_value:
                            transition_value = omega_table[n-1][j] + np.log(transitions_table[j][k])
                omega_table[n][k] = np.log(emissions_table[k][sequence_index[n]]) + transition_value

    # Creation of the Z* sequence as a list, and calculation of its last element
    Z = []
    list2 = [] # list to keep the 3 elements of the last column of the omega table and
    # find their maximum
    for i in range(len(sequence_index)):
        Z.append(sequence_index[i])
        # Here we fill the Z list with the same letters of the test sequence.
        # But we could fill it with any other characters. Only its length must be the same with this of the test sequence.
        # Now just need to get the max value from the last row in omega. Need that to start
        # the backtracking
    for j in range(len(hidden)):
        list2.append(omega_table[len(omega_table) - 1][j])
    for j in range(len(hidden)):
        if omega_table[len(omega_table) - 1][j]==max(list2):
            Z[len(Z)-1]=j
    # Calculation of the rest of the Z sequence backwards, from the right to the left
    for n in range(len(Z)-1,0,-1):
        for k in range(len(hidden)):
            if transitions_table[k][Z[n]] != 0.0:
                if emissions_table[Z[n]][sequence_index[n]] != 0.0:
                    if omega_table[n-1][k] + np.log(transitions_table[k][Z[n]]) + np.log(emissions_table[Z[n]][sequence_index[n]]) == omega_table[n][Z[n]]:
                        Z[n-1] = k
    print("The Z* sequence of the hidden states:\n")
    print("".join([index_to_states[c] for c in Z])) # the Z* sequence printed as a string
    print("Log value:" + str(omega_table[-1][Z[-1]]))
    print("Finished")

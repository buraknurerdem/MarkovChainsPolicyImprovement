# This is for the ease of use when giving the transition probability matrices as input.
# It is easier to define each transition matrix for every action. Giving those matrices
# as input in a list to this function returns the wanted format for the main function.
# An example: a = policy_improvement(costs, av_ac, transtion_probability_matrix_converter([m1,m2,m3]))
# Here, m1 which is a list of lists is the transition matrix for action 1 and so on.

def transtion_probability_matrix_converter(list_of_matrices):
    final_matrix = []
    state_count = len(list_of_matrices[0][0])
    for i in range(state_count):
        temp_j = []
        for j in range(state_count):
            temp_actions = []
            for m in list_of_matrices:
                temp_actions.append(m[i][j])
            temp_j.append(temp_actions)
        final_matrix.append(temp_j)
    return(final_matrix)

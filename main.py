from sympy import symbols, Eq, linsolve, Matrix

# Explanation of parameters:

# cost_mat[i][k] should be list of lists, cost of action k in state i
# available_actions_mat[i][k] should be list of lists, (i, k)th entry should
# be 1 if action k is available in state i, 0 otherwise
# transition_mat[i][j][k] should be list of lists of lists and is the probability of 
# transition to state j from state i when action k is chosen.
# Extra argument of initial policy can be given as:
# initial_policy = [k1, k2] which means k1 is chosen at state 0 and k2 is chosen at state 1.

# The output is in terms of the index of chosen actions at which state.

class output:
    def __init__(self, policy, expected_cost):
        self.policy = policy
        self.expected_cost = expected_cost
        
# Class definition for output.
def policy_improvement(cost_mat, available_actions_mat, transition_mat, **kwargs):
    
    policy = kwargs.get("initial_policy", None)
    if policy == None:
        policy = []
        for i in available_actions_mat:
            for j, dec in enumerate(i):
                if dec == 1:
                    policy.append(j)
                    break

    while 1:
        
        # Step 1: Policy Evaluation
        
        unknowns = ["g(r)"]
        for i in range(len(cost_mat)):
            unknowns.append("v_" + str(i))
        
        # Equations are gathered to form an augmented matrix
        eq_matrix = []
        for i in range(len(cost_mat)):
            temp_list = []
            temp_list.append(-1) # coeff of g(R), send to RHS
            for j in range(len(cost_mat)): # coeff.s of v_i(R)
                if i == j:
                    temp_list.append(transition_mat[i][j][policy[i]] - 1)
                else:
                    temp_list.append(transition_mat[i][j][policy[i]])
            temp_list.append(- cost_mat[i][policy[i]]) # negative costs which are LHS
            eq_matrix.append(temp_list)
        
        # This block adds another equation which ensures that
        # v_M is equal to 0.
        temp_list = []
        temp_list.append(0) # coeff of g(R)
        for j in range(len(cost_mat)): # coeff.s of v_i(R)
            if j == len(cost_mat) - 1:
                temp_list.append(1)
            else:
                temp_list.append(0)
        temp_list.append(0) # negative costs which are RHS
        eq_matrix.append(temp_list)
        
        solutions = list(linsolve(Matrix(eq_matrix), symbols(unknowns)))
        if len(solutions) == 0:
            print("Equation system failed to give a real solution set when dedicated policy is: " + str(policy))
            return()
        
        # Step 2: Policy Improvement

        policy_new = policy.copy()
        for i in range(len(cost_mat)):
            smallest_exp_cost = solutions[0][0]
            
            for kind, k in enumerate(available_actions_mat[i]):
                if k == 0:
                    continue
                    
                new_gr = cost_mat[i][kind] + sum( transition_mat[i][j][kind] * solutions[0][j + 1]
                                                 for j in range(len(cost_mat))) - solutions[0][i + 1]
                if smallest_exp_cost > new_gr:
                    smallest_exp_cost = new_gr
                    policy_new[i] = kind
                   # print("at state", i, "changed", policy[i], "with", kind)
                    
        if policy == policy_new:
            break
        
        policy = policy_new
    
    out = output(policy, solutions[0][0])
    return(out)


# An example:

costs = [[0, 4.5, 5, None, None], [None, None, None, 50, 9]]
av_ac = [[1,1,1,0,0], [0,0,0,1,1]]
transition_mat = [[[0.9, 0.98, 1, 0, 0],
                  [0.1, 0.02, 0, 0, 0]],
                 [[0,0,0,1,0],
                 [0,0,0,0,1]]]
a = policy_improvement(costs, av_ac, transition_mat, initial_policy = [1, 4])

# Output of the example:

print(a.policy)
# >>> [0, 3]
print(a.expected_cost)
# >>> 4.54545454545454

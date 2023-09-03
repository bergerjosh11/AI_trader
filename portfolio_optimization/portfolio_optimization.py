import numpy as np
import cvxpy as cp

# Example data (returns and covariances)
returns = np.array([0.1, 0.15, 0.12, 0.08])
cov_matrix = np.array([[0.02, 0.015, 0.01, 0.005],
                       [0.015, 0.03, 0.02, 0.01],
                       [0.01, 0.02, 0.025, 0.015],
                       [0.005, 0.01, 0.015, 0.03]])

# Define variables
n = len(returns)
weights = cp.Variable(n)
expected_return = returns @ weights
risk = cp.quad_form(weights, cov_matrix)

# Define the objective function (maximize expected return while minimizing risk)
objective = cp.Maximize(expected_return - 0.5 * cp.multiply(1e-4, risk))

# Define constraints (e.g., sum of weights equals 1)
constraints = [cp.sum(weights) == 1, weights >= 0]

# Create and solve the problem
problem = cp.Problem(objective, constraints)
problem.solve()

# Optimal weights for the portfolio
optimal_weights = weights.value

import cvxpy
import numpy as np

from toqito.super_operators.partial_trace import partial_trace_cvx
from toqito.hedging.pi_perm import pi_perm


def minimize_losing_less_than_k(Q_a, n):
    Y = cvxpy.Variable((2**n, 2**n), hermitian=True)
    objective = cvxpy.Maximize(cvxpy.trace(cvxpy.real(Y)))

    a = pi_perm(n)
    b = cvxpy.kron(np.eye(2**n), Y)
    c = pi_perm(n).conj().T
    if n == 1:
        u = cvxpy.multiply(cvxpy.multiply(a, b), c)
        constraints = [cvxpy.real(u) << Q_a]
    else:
        constraints = [cvxpy.real(a @ b @ c) << Q_a]
    problem = cvxpy.Problem(objective, constraints)

    dual = problem.solve()
    print(dual)


def maximize_losing_less_than_k(Q_a, n):
    sys = list(range(1, 2*n, 2))
    if len(sys) == 1:
        sys = sys[0]
    dim = 2*np.ones((1, 2*n)).astype(int).flatten()
    dim = dim.tolist()

    X = cvxpy.Variable((4**n, 4**n), PSD=True)
    objective = cvxpy.Maximize(cvxpy.trace(Q_a.conj().T @ X))
    constraints = [partial_trace_cvx(X, sys, dim) == np.identity(2**n)]
    problem = cvxpy.Problem(objective, constraints)
   
    primal = problem.solve()
    print(primal)

    Y = cvxpy.Variable((2**n, 2**n), hermitian=True)
    objective = cvxpy.Minimize(cvxpy.trace(cvxpy.real(Y)))

    a = pi_perm(n)
    b = cvxpy.kron(np.eye(2**n), Y)
    c = pi_perm(n).conj().T

    if n == 1:
        u = cvxpy.multiply(cvxpy.multiply(a, b), c)
        constraints = [cvxpy.real(u) >> Q_a]
    else:
        constraints = [cvxpy.real(a @ b @ c) >> Q_a]
    problem = cvxpy.Problem(objective, constraints)

    dual = problem.solve()
    print(dual)
    

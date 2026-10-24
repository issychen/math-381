import numpy as np
from scipy.optimize import linprog

# Data from Model 11
cargo_wt  = [20, 16, 25, 13]        # tons of each cargo available
vol_per_t = [500, 700, 600, 400]    # cu ft per ton
profit    = [280, 360, 320, 250]    # $ per ton
comps     = ["Front", "Center", "Back"]
wt_cap    = [12, 18, 10]            # tons
sp_cap    = [7000, 9000, 5000]      # cu ft

# Decision variables x[i,j] = tons of cargo i placed in compartment j
# Flattened order: x11,x1F... index = 3*i + j  (i = cargo 0..3, j = comp 0..2)
n = 12
idx = lambda i, j: 3*i + j

# Objective: maximize sum profit_i * x_ij  ->  minimize the negative
c = np.zeros(n)
for i in range(4):
    for j in range(3):
        c[idx(i, j)] = -profit[i]

A_ub, b_ub = [], []
# (1) Can't ship more of cargo i than is offered
for i in range(4):
    row = np.zeros(n); row[[idx(i, j) for j in range(3)]] = 1
    A_ub.append(row); b_ub.append(cargo_wt[i])
# (2) Weight capacity of each compartment
for j in range(3):
    row = np.zeros(n); row[[idx(i, j) for i in range(4)]] = 1
    A_ub.append(row); b_ub.append(wt_cap[j])
# (3) Space capacity of each compartment
for j in range(3):
    row = np.zeros(n)
    for i in range(4): row[idx(i, j)] = vol_per_t[i]
    A_ub.append(row); b_ub.append(sp_cap[j])

# (4) Balance: (weight in F)/12 = (weight in C)/18 = (weight in B)/10
#     written as  18*W_F - 12*W_C = 0  and  10*W_C - 18*W_B = 0
A_eq, b_eq = [], []
for (j1, j2) in [(0, 1), (1, 2)]:
    row = np.zeros(n)
    for i in range(4):
        row[idx(i, j1)] = wt_cap[j2]
        row[idx(i, j2)] = -wt_cap[j1]
    A_eq.append(row); b_eq.append(0)

res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
              bounds=[(0, None)] * n)

print(res.message)
print(f"Maximum profit: ${-res.fun:,.2f}\n")
x = res.x.reshape(4, 3)
print(f"{'Cargo':<8}" + "".join(f"{c:>10}" for c in comps) + f"{'Total':>10}")
for i in range(4):
    print(f"{i+1:<8}" + "".join(f"{abs(x[i,j]):>10.3f}" for j in range(3)) + f"{x[i].sum():>10.3f}")
print(f"{'Weight':<8}" + "".join(f"{x[:,j].sum():>10.3f}" for j in range(3)))
print(f"{'Space':<8}" + "".join(f"{(np.array(vol_per_t) @ x[:,j]):>10.1f}" for j in range(3)))
print(f"{'Fraction of weight cap':<8}: " + ", ".join(f"{x[:,j].sum()/wt_cap[j]:.4f}" for j in range(3)))

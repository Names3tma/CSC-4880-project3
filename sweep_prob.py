import glob
import time
import csv
import statistics
import matplotlib.pyplot as plt
from upgraded_robot_solver import parse_cnf, walksat

P_VALUES = [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0]
RUNS_PER_FILE = 3
MAX_FLIPS = 20000

paths = sorted(glob.glob("problems/*.cnf"))
cnfs = [parse_cnf(p) for p in paths]
print(f"{len(paths)} files")

rows = [] #metrics
for p in P_VALUES:
    times, timeouts = [], 0
    for nv, cl, occ in cnfs:
        start = time.perf_counter()
        result = walksat(nv, cl, occ, p=p, max_flips=MAX_FLIPS)
        times.append(time.perf_counter() - start)
        if result is None:
            timeouts += 1
    mean_t = statistics.mean(times)
    rows.append((p, mean_t, timeouts, len(times)))
    print(f"p={p:.2f}: mean {mean_t:.3f}s, timeouts {timeouts}/{len(times)}")

with open("p_sweep.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["p", "mean_seconds", "timeouts", "runs"])
    w.writerows(rows)

plt.plot([r[0] for r in rows], [r[1] for r in rows], marker="o")
plt.xlabel("p (probability of a random move)")
plt.ylabel("Mean running time (seconds)")
plt.title("Running time vs. p")
plt.savefig("sweep_prob.png", dpi=150)
plt.show()
import glob
import time
import csv
import statistics
import matplotlib.pyplot as plt
from upgraded_robot_solver import parse_cnf, walksat

paths = sorted(glob.glob("problems_upgraded/*.cnf"))
print(f"found files")

rows = []
for path in paths:
    num_vars, clauses, occurences = parse_cnf(path)

    start = time.perf_counter()
    result = walksat(num_vars, clauses, occurences)
    elapsed = time.perf_counter() - start

    solved = result is not None
    rows.append((path, elapsed, solved))
    print(f"{path}: {elapsed:.2f}s {'solved' if solved else 'timed out'}")

with open("results_v3_baseline.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["file", "seconds", "solved"])
    w.writerows(rows)

times = [t for  _, t, ok in rows if ok]
timeouts = sum(1 for _, _, ok in rows if not ok)

print(f"\nSolved: {len(times)}/{len(rows)}   Timeouts: {timeouts}")
if times:
    print(f"Mean: {statistics.mean(times):.2f}s  Median: {statistics.median(times):.2f}s")

plt.hist(times, bins=20)
plt.xlabel("Solve time (seconds)")
plt.ylabel("Number of CNFs")
plt.title("Upgraded solver on Part 2 problems (p=20, q=50)")
plt.savefig("histogram_v3_baseline.png")

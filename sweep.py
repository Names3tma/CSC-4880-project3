import subprocess
import time
import upgraded_robot_generator
import statistics

def time_solver(path):
    start = time.perf_counter()
    result = subprocess.run(["python", "robot_solver.py", path], capture_output=True, text=True)
    elapsed = time.perf_counter() - start
    if result.stdout.startswith("success") == True:
        solved = True
    else:
        solved = False

    return elapsed, solved

def test_setting(p, q, count):
    folder = "sweep/p" + str(p) + "_q" + str(q)
    upgraded_robot_generator.generate_probs(count, 75, p, q, folder)
    times = []
    timeouts = 0

    for i in range(count):
        file = folder + "/problem_" + str(i) + ".cnf"
        elapsed, solved = time_solver(file)
        times.append(elapsed)
        if solved == False:
            timeouts += 1
        print("  problem", i, ":", round(elapsed, 2), "s", "solved" if solved else "TIMEOUT")

    avg = sum(times) / len(times)
    med = statistics.median(times)
    return avg, med, timeouts

def sweep_q(p, q_values, count, out_file):
    with open(out_file, "w") as f:
        f.write("q,avg_time,median_time,timeouts\n")
        for q in q_values:
            print("Testing q = " + str(q))
            avg, med, timeouts = test_setting(p, q, count)
            f.write(str(q) + "," + str(avg) + "," + str(med) + "," + str(timeouts) + "\n")

def sweep_p(q, p_values, count, out_file):
    with open(out_file, "w") as f:
        f.write("p,avg_time,median_time,timeouts\n")
        for p in p_values:
            print("Testing p = " + str(p))
            avg, med, timeouts = test_setting(p, q, count)
            f.write(str(p) + "," + str(avg) + "," + str(med) + "," + str(timeouts) + "\n")

if __name__ == "__main__":
    sweep_p(50, [0, 5, 10, 20, 40, 74], 5, "sweep_p.csv")

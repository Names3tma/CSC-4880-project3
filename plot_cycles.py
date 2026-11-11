import matplotlib.pyplot

cycles = [1, 2, 3]
p_values = [5, 20, 74]
q_values = [15, 50, 50]
changes_cycles = [2, 3]
p_changes = [15, 54]
q_changes = [35, 0]

fig, (top, bottom) = matplotlib.pyplot.subplots(2, 1, sharex=True)
top.plot(cycles, p_values, marker="o", label="p (friend pairs)")
top.plot(cycles, q_values, marker="o", label="q (enemy pairs)")
top.set_ylabel("Parameter value")
top.set_title("Generator parameters across cycles")
top.legend()

bottom.plot(changes_cycles, p_changes, marker="o", label="change in p")
bottom.plot(changes_cycles, q_changes, marker="o", label="change in q")
bottom.set_ylabel("Change from previous cycle")
bottom.set_xlabel("Cycle")
bottom.legend()

bottom.set_xticks(cycles)

matplotlib.pyplot.savefig("parameter_cycles.png")
matplotlib.pyplot.close()

import pandas
import matplotlib.pyplot


def plot_sweep(title, csv_file, param, out_png, log_x, log_y):
    data = pandas.read_csv(csv_file)
    fig, (top, bottom) = matplotlib.pyplot.subplots(2, 1, sharex=True)

    top.plot(data[param], data["median_time"], marker="o", label="median")
    top.plot(data[param], data["avg_time"], marker="o", label="mean")
    top.set_ylabel("Solve time (s)")
    top.set_title(title)
    top.legend()

    bottom.plot(data[param], data["timeouts"], marker="o")
    bottom.set_ylabel("Timeouts (of 5)")
    bottom.set_xlabel(param)

    if log_x == True:
        bottom.set_xscale("symlog", linthresh=25)
    if log_y == True:
        top.set_yscale("log")

    matplotlib.pyplot.savefig(out_png)
    matplotlib.pyplot.close()


if __name__ == "__main__":
    plot_sweep("Coarse sweep of p vs upgraded solver (q = 50)", "sweep_p_v3.csv", "p", "sweep_p_v3.png", False, True)
    plot_sweep("Fine sweep of p vs upgraded solver (q = 50)", "sweep_p_v3_fine.csv", "p", "sweep_p_v3_fine.png", False, False)

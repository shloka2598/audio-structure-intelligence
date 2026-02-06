import matplotlib.pyplot as plt

def plot_density_with_boundaries(
    section_features,
    boundaries,
    duration,
    title=None,
    save_path=None
):
    times = []
    densities = []

    for s in section_features:
        if "onset_density" in s:
            density = s["onset_density"]
        elif "density" in s:
            density = s["density"]
        else:
            continue

        mid = (s["start"] + s["end"]) / 2
        times.append(mid)
        densities.append(density)


    fig, ax = plt.subplots(figsize=(12, 4))

    ax.plot(times, densities, marker="o", linewidth=2)

    for b in boundaries:
        ax.axvline(
            x=b["time"],
            color="red",
            linestyle="--",
            alpha=0.8
        )

    ax.set_xlim(0, duration)
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Onset density")

    if title:
        ax.set_title(title)

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()
    else:
        plt.tight_layout()
        plt.show()

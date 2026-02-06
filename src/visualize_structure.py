import matplotlib.pyplot as plt

SECTION_COLORS = {
    "intro": "#9ecae1",
    "breakdown": "#fdae6b",
    "verse": "#bcbddc",
    "chorus": "#fb6a4a",
    "post_chorus": "#74c476",
    "bridge": "#fd8d3c",
    "outro": "#c7e9c0",
}

def plot_structure_timeline(labeled_sections, duration, title=None,save_path=None):
    fig, ax = plt.subplots(figsize=(12, 2))

    for sec in labeled_sections:
        start = sec["start"]
        end = sec["end"]
        label = sec["label"]

        color = SECTION_COLORS.get(label, "#cccccc")

        ax.barh(
            y=0,
            width=end - start,
            left=start,
            height=0.6,
            color=color,
            edgecolor="black"
        )

        ax.text(
            (start + end) / 2,
            0,
            label,
            ha="center",
            va="center",
            fontsize=10,
            color="black"
        )

    ax.set_xlim(0, duration)
    ax.set_yticks([])
    ax.set_xlabel("Time (seconds)")

    if title:
        ax.set_title(title)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()
    else:
        plt.show()

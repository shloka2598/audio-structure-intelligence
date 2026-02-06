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

def plot_structure_comparison(song_a, song_b):
    fig, ax = plt.subplots(figsize=(12, 3))

    for y, song in enumerate([song_a, song_b]):
        sections = song["sections"]
        duration = song["duration"]

        for sec in sections:
            start = sec["start"] / duration * 100
            end = sec["end"] / duration * 100
            label = sec["label"]
            color = SECTION_COLORS.get(label, "#cccccc")

            ax.barh(
                y=y,
                width=end - start,
                left=start,
                height=0.5,
                color=color,
                edgecolor="black"
            )

            ax.text(
                (start + end) / 2,
                y,
                label,
                ha="center",
                va="center",
                fontsize=9
            )

    ax.set_yticks([0, 1])
    ax.set_yticklabels([
    f'{song_a["name"]} ({song_a["archetype"]})',
    f'{song_b["name"]} ({song_b["archetype"]})'
])
    ax.set_xlabel("Song Progress (%)")
    ax.set_xlim(0, 100)
    ax.set_title("Structure Comparison")

    plt.tight_layout()
    plt.show()

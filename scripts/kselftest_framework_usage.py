import matplotlib.pyplot as plt
import pandas as pd
import sys

colors = ["#344964", "#B1D9E5", "#ACB2BC", "#F6F6F6", "#475EA5"]
data = pd.read_csv("test_counts.csv")
data = data[data["Target"] != "Total"]

usage = "Kselftest Framework Usage (%)"
title_percentage = "Kselftest Framework Usage (%)"
title_count = "Kselftest Framework Usage Counts"
save_path = "kselftest.png"
if sys.argv[1] == "kselftest":
    data[usage] = (
        data["C Files with kselftest.h"] / data["C Files with main/_start"] * 100
    )
elif sys.argv[1] == "harness":
    usage = "Kselftest Harness Usage (%)"
    title_percentage = "Kselftest Harness Usage (%)"
    title_count = "Kselftest Harness Usage Counts"
    save_path = "harness.png"
    data[usage] = (
        data["C Files with kselftest_harness.h"]
        / data["C Files with main/_start"]
        * 100
    )
else:
    print("Invalid argument")
    sys.exit(1)
bins = [0, 20, 40, 60, 80, 100]
labels = ["0-20%", "21-40%", "41-60%", "61-80%", "81-100%"]
data["Usage Group"] = pd.cut(data[usage], bins=bins, labels=labels, right=False)

usage_percentages = data["Usage Group"].value_counts(normalize=True) * 100
usage_percentages = usage_percentages.reindex(labels)

usage_counts = data["Usage Group"].value_counts(normalize=False)
usage_counts = usage_counts.reindex(labels)

fig, axs = plt.subplots(1, 2, figsize=(16, 8))


def custom_autopct(pct):
    return ("%1.1f%%" % pct) if pct > 0 else ""


patches, texts, autotexts = axs[1].pie(
    usage_percentages,
    labels=None,
    autopct=custom_autopct,
    startangle=140,
    colors=colors,
)
axs[1].set_title(title_percentage, fontsize=16, fontweight="bold")

axs[0].legend(
    patches,
    labels,
    title="Usage framework\nwithin subsystem",
    loc="upper right",
    bbox_to_anchor=(0.97, 0.97),
)

for text in texts:
    text.set_fontsize(14)
    text.set_weight("bold")

for autotext in autotexts:
    autotext.set_fontsize(14)
    autotext.set_weight("bold")

bars = axs[0].bar(usage_counts.index, usage_counts, color=colors)
axs[0].set_title(title_count, fontsize=16, fontweight="bold")
axs[0].tick_params(axis="x", rotation=45)

for bar in bars:
    height = bar.get_height()
    axs[0].annotate(
        f"{height}",
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 3),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=12,
        fontweight="bold",
    )

plt.tight_layout()
plt.savefig(save_path, bbox_inches="tight")
plt.show()

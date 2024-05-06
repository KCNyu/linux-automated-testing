import matplotlib.pyplot as plt
import numpy as np


# Data for plotting
# categories = ["Real Time (s)", "User Time (s)", "System Time (s)"]
# old_version = [10.235, 10.669, 3.328]
# new_version = [2.069, 1.584, 0.519]

categories = ["Real Time (s)"]
old_version = [10.235]
new_version = [2.069]

categories_test = ["Pass test", "Total test"]
old_test_version = [128, 227]
new_test_version = [1007, 1165]

all_categories = categories + categories_test

x = np.arange(len(all_categories))  # the label locations
fig, ax = plt.subplots(figsize=(8, 4))  # Width, Height in inches
width = 0.35
colors_old = ["#C7DFF0"]
colors_new = ["#377483"]

rects1 = ax.bar(
    x[: len(categories)] - width / 2,
    old_version,
    width,
    label="Linaro/test-definitions",
    color=colors_old,
)
rects2 = ax.bar(
    x[: len(categories)] + width / 2,
    new_version,
    width,
    label="Developed (ISP RAS - in use)",
    color=colors_new,
)

ax.set_ylabel("Time (seconds)")
ax.tick_params(axis="y")
ax.set_xticks(x)
ax.set_xticklabels(all_categories)

ax.set_ylim([0, max(old_version + new_version) * 1.1])

# Place legend in the center
legend = ax.legend(
    fontsize="small",
    title="Version",
    title_fontsize="small",
    edgecolor="black",
    bbox_to_anchor=(0.5, 1.05),
    loc="lower center",
    fancybox=True,
    shadow=True,
    ncol=5,
)
for text in legend.get_texts():
    text.set_fontweight("bold")


def add_labels(rects, is_time=True):
    for rect in rects:
        height = rect.get_height()
        if is_time:
            ax.annotate(
                f"{round(height, 3)} s",
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha="center",
                va="bottom",
            )
        else:
            ax2.annotate(
                f"{height}",
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha="center",
                va="bottom",
            )


# Adding labels to both old and new version bars
add_labels(rects1)
add_labels(rects2)


# Create a second y-axis for the number of tests
ax2 = ax.twinx()
ax2.set_ylim([0, max(old_test_version + new_test_version) * 1.1])

# Create bar chart for test data
rects3 = ax2.bar(
    x[len(categories) :] - width / 2,
    old_test_version,
    width,
    label="Old Version - Tests",
    color=colors_old,
)
rects4 = ax2.bar(
    x[len(categories) :] + width / 2,
    new_test_version,
    width,
    label="New Version - Tests",
    color=colors_new,
)

# Adding labels to both old and new version test bars
add_labels(rects3, is_time=False)
add_labels(rects4, is_time=False)

ax2.set_ylabel("Number of tests")
ax2.tick_params(axis="y")

plt.tight_layout()
plt.savefig("performance_comparison.pdf", format="pdf", bbox_inches="tight")

plt.show()

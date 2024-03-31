import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("test_counts.csv")
data = data[data["Target"] != "Total"]

kselftest_h_count = data["C Files with kselftest.h"].sum()
kselftest_harness_h_count = data["C Files with kselftest_harness.h"].sum()
main_start_count = data["C Files with main/_start"].sum()

categories = [
    "Normal Test Files",
    "Test Files with kselftest.h",
    "Test Files with kselftest_harness.h",
    "Sum of kselftest Files",
]
counts = [
    main_start_count,
    kselftest_h_count,
    kselftest_harness_h_count,
    kselftest_h_count + kselftest_harness_h_count,
]
colors = ["#ACB2BC", "#344964", "#B1D9E5", "#475EA5"]

fig, axs = plt.subplots(1, 2, figsize=(14, 7))

for i, (category, count) in enumerate(zip(categories, counts)):
    bar = axs[0].bar(category, count, color=colors[i], label=category)
    axs[0].text(bar[0].get_x() + bar[0].get_width() / 2, count, f'{count}', ha='center', va='bottom', fontsize=10, fontweight='bold')

axs[0].set_title("Number of Test Files", fontdict={'fontsize': 14, 'fontweight': 'bold'})
axs[0].set_ylabel("Counts", fontdict={'fontsize': 12, 'fontweight': 'bold'})
axs[0].set_xticks([])
axs[0].set_ylabel("Counts", fontdict={'fontsize': 12, 'fontweight': 'bold'})
axs[0].tick_params(axis="x", labelsize=10)

axs[0].set_xticklabels([])

axs[0].legend(loc="upper right", title="Categories")

percentages = [count / counts[0] * 100 for count in counts[1:3]]
percentages.append(100 - sum(percentages))

def custom_autopct(pct):
    return ('%1.1f%%' % pct) if pct > 0 else ''

categories_pie = [
    "Test Files with kselftest.h",
    "Test Files with kselftest_harness.h",
    "Others",
]
colors_pie = ["#344964", "#B1D9E5", "#ACB2BC"]

patches, texts, autotexts = axs[1].pie(
    percentages, labels=None, autopct=custom_autopct, startangle=140, colors=colors_pie,
    textprops={'fontsize': 12, 'weight': 'bold'}
)
axs[1].set_title("Percentage of Test Files", fontdict={'fontsize': 14, 'fontweight': 'bold'})

plt.tight_layout()
plt.savefig("test_files.png")
plt.show()

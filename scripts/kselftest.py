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
colors = ["#ffbb78", "#1f77b4", "#98df8a", "#aec7e8"]

fig, axs = plt.subplots(1, 2, figsize=(14, 7))
axs[0].bar(categories, counts, color=colors)
axs[0].set_title("Number of Test Files", fontdict={'fontsize': 14, 'fontweight': 'bold'})
axs[0].set_ylabel("Counts", fontdict={'fontsize': 12, 'fontweight': 'bold'})
axs[0].tick_params(axis="x", rotation=45, labelsize=10, labelrotation=45)

percentages = [count / counts[0] * 100 for count in counts[1:3]]
percentages.append(100 - sum(percentages))

def custom_autopct(pct):
    return ('%1.1f%%' % pct) if pct > 0 else ''

categories = [
    "Test Files with kselftest.h",
    "Test Files with kselftest_harness.h",
    "Others",
]
colors = ["#1f77b4", "#98df8a", "#ffbb78"]
axs[1].pie(
    percentages, labels=categories, autopct=custom_autopct, startangle=140, colors=colors,
    textprops={'fontsize': 12, 'weight': 'bold'}
)
axs[1].set_title("Percentage of Test Files", fontdict={'fontsize': 14, 'fontweight': 'bold'})

plt.tight_layout()
plt.savefig("test_files.png")
plt.show()

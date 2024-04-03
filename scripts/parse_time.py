import matplotlib.pyplot as plt

# Data for plotting
categories = ['Real Time (s)', 'User Time (s)', 'System Time (s)']
old_version = [10.235, 10.669, 3.328]
new_version = [2.069, 1.584, 0.519]

x = range(len(categories)) 


fig, ax = plt.subplots()
bar_width = 0.35
colors_old = ['#C7DFF0'] 
colors_new = ['#377483'] 

rects1 = ax.bar(x, old_version, bar_width, label='Old Version', color=colors_old)
rects2 = ax.bar([p + bar_width for p in x], new_version, bar_width, label='New Version', color=colors_new)

ax.set_ylabel('Time (seconds)')
# ax.set_title('Performance Comparison between Old and New Submitter Versions')
ax.set_xticks([p + bar_width / 2 for p in x])
ax.set_xticklabels(categories)
ax.legend()

def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(round(height, 3)),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

# Adding labels to both old and new version bars
add_labels(rects1)
add_labels(rects2)

plt.tight_layout()

plt.savefig('performance_comparison.png')
plt.show()



import matplotlib.pyplot as plt
import numpy as np
import json

# Read Json file

data = None

with open("./data/log.json") as f:
    data = json.load(f)

names = []
sds = []
aads = []
avr_excs = []
mins = []
maxs = []

for key, value in data.items():
    names.append(key)
    sds.append(value["sd"])
    aads.append(value["aad"])
    avr_excs.append(value["avr_exc"])
    mins.append(value["min"])
    maxs.append(value["max"])

# fig, axs = plt.subplots(1, 8, sharex=True, sharey=True)
# test_size = len(data[names[0]]["cases"])

# axs[0].plot(data[names[0]]["cases"])
# axs[0].plot([data[names[0]]["avr"]] * test_size)
# axs[0].set_title(names[0])

# axs[1].plot(data[names[1]]["cases"])
# axs[1].plot([data[names[1]]["avr"]] * test_size)
# axs[1].set_title(names[1])

# axs[2].plot(data[names[2]]["cases"])
# axs[2].plot([data[names[2]]["avr"]] * test_size)
# axs[2].set_title(names[2])

# axs[3].plot(data[names[3]]["cases"])
# axs[3].plot([data[names[3]]["avr"]] * test_size)
# axs[3].set_title(names[3])

# axs[4].plot(data[names[4]]["cases"])
# axs[4].plot([data[names[4]]["avr"]] * test_size)
# axs[4].set_title(names[4])

# axs[5].plot(data[names[5]]["cases"])
# axs[5].plot([data[names[5]]["avr"]] * test_size)
# axs[5].set_title(names[5])

# axs[6].plot(data[names[6]]["cases"])
# axs[6].plot([data[names[6]]["avr"]] * test_size)
# axs[6].set_title(names[6])

# axs[7].plot(data[names[7]]["cases"])
# axs[7].plot([data[names[7]]["avr"]] * test_size)
# axs[7].set_title(names[7])

# for ax in axs.flat:
#     ax.label_outer()

# fig.text(0.5, 0.04, "Cases", ha="center")
# fig.text(0.04, 0.5, "Accuracy", va="center", rotation="vertical")
# plt.show()

# X_axis = np.arange(len(names))
# plt.bar(X_axis - 0.2, sds, 0.2, label="Standard Deviation")
# plt.bar(X_axis, aads, 0.2, label="Average Absolute Deviation")

# plt.xticks(X_axis, names)
# plt.xlabel("Combinations")
# plt.ylabel("Value")
# plt.legend()
# plt.show()

# X_axis = np.arange(len(names))
# plt.bar(X_axis, avr_excs, 0.2, label="Average Exec Time")
# plt.xticks(X_axis, names)
# plt.ylabel("Value")
# plt.legend()
# plt.show()


X_axis = np.arange(len(names))
plt.bar(X_axis - 0.2, mins, 0.2, label="Min Value")
plt.bar(X_axis, maxs, 0.2, label="Max Value")

plt.xticks(X_axis, names)
plt.xlabel("Min_Max")
plt.ylabel("Value")
plt.legend()
plt.show()

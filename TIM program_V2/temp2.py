
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv(r'C:/Users/jmajor/Desktop/DAQ_data.txt')

df2 = df.iloc[:,2:]

ten_minute_count = 1
for i in df.iloc[::-1, 0]:
    if df.iloc[-1, 0] - i > 600:
        break
    ten_minute_count +=1


np.std(df2.iloc[:50,0])

new_std = []

for i in range(len(df2.iloc[:,3])):
    if i < ten_minute_count:
        std = np.mean([np.std(df2.iloc[:i,0]),np.std(df2.iloc[:i,1]),np.std(df2.iloc[:i,2]),np.std(df2.iloc[:i,3])])
        new_std.append(std)

    else:
        new_std.append(np.std(df2.iloc[i-ten_minute_count:i,3]))

x = range(len(new_std))


fig, ax1 = plt.subplots()

ax1.plot(new_std, label = 'Moving STD')
ax1.plot(df['STD'])
ax1.legend(loc=0)
ax1.set_ylabel('STD')



ax2 = ax1.twinx()
ax2.plot(df2.iloc[:,0], label = "T1", color = 'red')
ax2.plot(df2.iloc[:,1], label = "T2", color = 'black')
ax2.plot(df2.iloc[:,2], label = "T3", color = 'green')
ax2.plot(df2.iloc[:,3], label = "T4", color = 'yellow')
ax2.plot(x[-ten_minute_count:],[i + .5 for i in df2.iloc[-ten_minute_count:,3]], label = "Saved Data", color = 'purple')
ax2.set_ylabel('Temperature')
ax2.legend()


plt.show()
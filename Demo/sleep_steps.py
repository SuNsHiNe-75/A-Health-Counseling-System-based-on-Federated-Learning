#下面是收資料，一天一次，時間看是要早上請使用者輸入體重的同時背景邊把arduino插著電腦收資料這樣處理可以嗎
#或者是能再開一個功能叫做收資料?

#下面這邊是圖表，如果有需要可以分割到其他地方

import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv("steps.csv")
df.index = df.index + 1
plt.plot(df)
plt.title("")
plt.ylabel("steps") 
plt.xlabel("days")
plt.show()
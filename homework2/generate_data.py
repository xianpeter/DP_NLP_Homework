import numpy as np
import time
import csv

s = [0.3, 0.3, 0.4]
p = [0.6, 0.4, 0.5]
headers = ["结果", "类别"]
classes = ["1", "2", "3"]
with open('data.csv', 'a', newline='') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
for i in range(10000):
    row = []
    seed = int(time.time())
    jieguo = np.random.multinomial(1, s)
    for j,item in enumerate(jieguo):
      if item:
          row.append(classes[j])
          jieguo=np.random.binomial(1,p[j])
          row.append(jieguo)
    with open('data.csv', 'a', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(row)


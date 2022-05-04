import csv
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np

# 抛掷概率
pqr_ture = [0.6, 0.4, 0.5]
pqr_now = [0.4, 0.5, 0.6]
p = [0.4]
q = [0.5]
r = [0.6]
# 硬币分布
s_ture = [0.3, 0.3, 0.4]
s_now = [0.1, 0.4, 0.5]

tolerance = 0.0000001  # 迭代限度
font = {'family': 'Times New Roman', 'weight': 'normal', 'size': 15}  # 画图字体

with open('data.csv', 'r', encoding='UTF-8') as file:
    reader = csv.reader(file)
    column = [row[1:11] for row in reader]
del column[0]
flag = 1
epoch = 2000
length = len(column)
s1 = np.empty([length,1], dtype = float)
s2 = np.empty([length,1], dtype = float)
s3 = np.empty([length,1], dtype = float)
theta = 1
#  EM算法
for a in range(epoch):
    # E-step
    for i in range(length):
        temp = [1, 1, 1]
        zhengmian = 0
        for k in range(10):
            zhengmian = float(column[i][k])+zhengmian
        for j in range(3):
            temp[j] = temp[j]*s_now[j]*pow(pqr_now[j],zhengmian)*pow(1-pqr_now[j],10-zhengmian)
        s1[i] = temp[0]/(temp[0]+temp[1]+temp[2])
        s2[i] = temp[1]/(temp[0]+temp[1]+temp[2])
        s3[i] = temp[2]/(temp[0]+temp[1]+temp[2])
    s_now = [0, 0, 0]
    pqr_now = [0, 0, 0]
    # M-step
    for i in range(length):
        s_now[0] = s_now[0]+s1[i]
        s_now[1] = s_now[1]+s2[i]
        s_now[2] = s_now[2]+s3[i]
        zhengmian = 0
        for k in range(10):
            zhengmian = float(column[i][k])+zhengmian
        pqr_now[0] = pqr_now[0]+s1[i]*zhengmian/10
        pqr_now[1] = pqr_now[1]+s2[i]*zhengmian/10
        pqr_now[2] = pqr_now[2]+s3[i]*zhengmian/10
    pqr_now[0] = pqr_now[0]/s_now[0]
    pqr_now[1] = pqr_now[1]/s_now[1]
    pqr_now[2] = pqr_now[2]/s_now[2]
    s_now[0] = s_now[0]/length
    s_now[1] = s_now[1]/length
    s_now[2] = s_now[2]/length
    theta = abs(pqr_now[0]-pqr_ture[0])+abs(pqr_now[1]-pqr_ture[1])+abs(pqr_now[2]-pqr_ture[2])
    print(pqr_now)
    p.append(pqr_now[0])
    q.append(pqr_now[1])
    r.append(pqr_now[2])
print(s_now,pqr_now)
#  绘制变化
epoch = np.linspace(1, epoch+1, epoch+1)
plt.title('The PQR Expect', fontdict=font)
plt.xlabel("epoch", fontdict=font)
plt.ylabel("y", fontdict=font)
plt.grid()
plt.plot(epoch, p, label='p')
plt.plot(epoch, q, label='q')
plt.plot(epoch, r, label='r')
plt.legend()
plt.savefig('pqr.svg')
plt.close()

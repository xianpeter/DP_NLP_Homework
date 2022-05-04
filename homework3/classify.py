from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
import joblib
from sklearn import metrics
import numpy as np
import csv
with open('theta.csv') as f:
    f_csv = csv.reader(f)
    feature = []
    for line in f_csv:
        feature.append(line)
label = [int(i/40) for i in range(len(feature))]
X_train, X_test, y_train, y_test = train_test_split(feature, label, test_size=.2, random_state=0)
# 训练模型
model = OneVsRestClassifier(svm.SVC(kernel='linear', probability=True))
print("[INFO] Successfully initialize a new model !")
print("[INFO] Training the model…… ")
clt = model.fit(X_train, y_train)
print("[INFO] Model training completed !")
# 保存训练好的模型，下次使用时直接加载就可以了
joblib.dump(clt, "classify.pkl")
print("[INFO] Model has been saved !")

y_test_pred = clt.predict(X_test)
ov_acc = metrics.accuracy_score(y_test_pred, y_test)
print("overall accuracy: %f" % (ov_acc))
print("===========================================")
acc_for_each_class = metrics.precision_score(y_test, y_test_pred, average=None)
print("acc_for_each_class:\n", acc_for_each_class)
print("===========================================")
avg_acc = np.mean(acc_for_each_class)
print("average accuracy:%f" % (avg_acc))

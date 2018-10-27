import pandas as pd
import numpy as np
import os

from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import Imputer
from sklearn.metrics import roc_auc_score
from sklearn.metrics import f1_score
from sklearn.linear_model import LogisticRegression

import statsmodels.api as sm

train = pd.read_csv("C:\\Users\\Devin\\Google 드라이브\\빅콘관련\\challenge_data\\Data_set2.csv", engine = 'python')

train_target = train.TARGET
train = train[['TOT_LNIF_AMT',
               'CPT_LNIF_AMT',
               'LTST_CRDT_GRAD',
               'AUTR_FAIL_MCNT',
               'NUM_DAY_SUSP',
               'LT1Y_MXOD_AMT',
               'CRDT_CARD_CNT',
               'SPART_LNIF_CNT',
               'SPTCT_OCCR_MDIF']]

imp = Imputer()
imp.fit(train)

train = imp.transform(train)

X_train,X_test,y_train,y_test = train_test_split(train, train_target.apply(lambda x: 1 if x>0 else 0),
                                                 test_size=0.3, random_state=42)


clf = LogisticRegression(penalty='l1')
clf.fit(X_train,y_train)

# print(roc_auc_score(y_test,clf.predict_proba(X_test)[:,1]))

clf = LogisticRegression(penalty='l2')
clf.fit(X_train,y_train)

# print(roc_auc_score(y_test,clf.predict_proba(X_test)[:,1]))

clf = LogisticRegression(C=1e20,penalty='l2')
clf.fit(X_train,y_train)

# print(roc_auc_score(y_test,clf.predict_proba(X_test)[:,1]))

glm = sm.GLM(y_train,X_train,sm.families.Binomial())

results = glm.fit()

print(roc_auc_score(y_test,results.predict(X_test)))

# AUC_L1 = clf.predict_proba(X_test)[:,1]
# np.array(AUC_L1).tolist()
# print(AUC_L1)
# AUC_L1 = pd.DataFrame(np.array(AUC_L1))
# AUC_L1.columns = ['AUC']

GLM = list((results.predict(X_test)))
GLM = pd.DataFrame(np.array(GLM))
GLM.columns = ['GLM']

for i in range(30070):
    if GLM.values[i] > 0.1: #0.323874546618
        GLM.values[i] = 1
    else:
        GLM.values[i] = 0

print(f1_score(y_test, GLM, labels=None, pos_label=1, average='binary'))

test = pd.read_csv("C:\\Users\\Devin\\Google 드라이브\\빅콘관련\\Devin\\최종\\Test_set2.csv", engine = 'python')

test_target = test.TARGET
test = test[['TOT_LNIF_AMT',
               'CPT_LNIF_AMT',
               'LTST_CRDT_GRAD',
               'AUTR_FAIL_MCNT',
               'NUM_DAY_SUSP',
               'LT1Y_MXOD_AMT',
               'CRDT_CARD_CNT',
               'SPART_LNIF_CNT',
               'SPTCT_OCCR_MDIF']]

imp = Imputer()
imp.fit(test)

test = imp.transform(test)

glm2 = sm.GLM(y_train,X_train,sm.families.Binomial())

results = glm2.fit()

GLM2 = list((results.predict(test)))
GLM2 = pd.DataFrame(np.array(GLM2))
GLM2.columns = ['GLM']

for i in range(2019):
    if GLM2.values[i] > 0.2: #0.323874546618
        GLM2.values[i] = 1
    else:
        GLM2.values[i] = 0

# GLM2.to_csv("C:\\Users\\Devin\\Google 드라이브\\빅콘관련\\Devin\\최종\\GLM3.csv")
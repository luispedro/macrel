import pandas as pd
from sklearn import metrics, ensemble
from os import makedirs
import pickle
import gzip

makedirs('models/', exist_ok=True)
def report(name, y_true, y_pred):
    print(f"# {name} CLASSIFIER ")
    print("Accuracy: {:.3}".format(metrics.accuracy_score(y_true, y_pred)))
    print("MCC: {:.3}".format(metrics.matthews_corrcoef(y_true, y_pred)))

    print()
    print("Confusion matrix:")
    print(metrics.confusion_matrix(y_true, y_pred))
    print()
    print(metrics.classification_report(y_true, y_pred, digits=3))
    print("\n")

ampep_train = pd.read_table('data/AMP.train.tsv', index_col=0)
xiao_test = pd.read_table('data/AMP.test.tsv', index_col=0)

rf_w_oob = ensemble.RandomForestClassifier(
        n_estimators=101,
        oob_score=True,
        random_state=12345,
        n_jobs=8)

# We train a model without the OOB predictions to save to disk
rf_wout_oob = ensemble.RandomForestClassifier(
        n_estimators=101,
        random_state=12345,
        n_jobs=8)
rf_w_oob.fit(ampep_train.iloc[:, 3:], ampep_train['group'])
rf_wout_oob.fit(ampep_train.iloc[:, 3:], ampep_train['group'])

# In testing, using joblib.dump was actually slightly worse than standard pickle in
# terms of diskspace
pickle.dump(rf_wout_oob, gzip.open('models/AMP.pkl.gz', 'wb'))


oob_pred = rf_w_oob.classes_[(rf_w_oob.oob_decision_function_.T[1] > .5).astype(int)]
xiao_pred = rf_w_oob.predict(xiao_test.iloc[:, 3:])

# As xiao_test & ampep_test overlap in sequences, we need to do a bit of
# surgery to the predictions. Namely, we replace the test predictions on those
# by the out-of-bag predictions:

# index by sequence
xiao_pred = pd.Series(xiao_pred, index=xiao_test.sequence).to_dict()
oob_pred  = pd.Series(oob_pred,  index=ampep_train.sequence).to_dict()
pred = xiao_test.sequence.map(lambda seq: oob_pred.get(seq, xiao_pred[seq]))

report('AMP (unbalanced training)', xiao_test['group'], pred)

xiao_train = pd.read_table('data/AMP.train_bench.tsv', index_col=0)
rf_wout_oob.fit(xiao_train.iloc[:,3:], xiao_train['group'])
xiao_pred = rf_wout_oob.predict(xiao_test.iloc[:, 3:])
report('AMP (benchmark training)', xiao_test['group'], xiao_pred)

hemo_train = pd.read_table('data/Hemo.train.tsv', index_col=0)
hemo_test = pd.read_table('data/Hemo.test.tsv', index_col=0)
rf_w_oob.fit(hemo_train.iloc[:,3:], hemo_train['group'])
rf_wout_oob.fit(hemo_train.iloc[:,3:], hemo_train['group'])
pickle.dump(rf_wout_oob, gzip.open('models/Hemo.pkl.gz', 'wb'))


report('Hemo', hemo_test['group'], rf_w_oob.predict(hemo_test.iloc[:, 3:]))

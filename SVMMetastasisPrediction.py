import pandas as pd

from sklearn import metrics
from sklearn.svm import SVC  # import Support Vector Machine Classifier
from sklearn.metrics import confusion_matrix

#from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# Evaluation function
def evaluation(y_true, y_pred):
    # Print Accuracy, Recall, F1 Score, and Precision metrics.
    print('Evaluation Metrics:')
    print('Accuracy: ' + str(metrics.accuracy_score(y_true, y_pred)))
    print('Recall: ' + str(metrics.recall_score(y_true, y_pred)))
    print('F1 Score: ' + str(metrics.f1_score(y_true, y_pred)))
    print('Precision: ' + str(metrics.precision_score(y_true, y_pred)))

    # Print Confusion Matrix
    print('\nConfusion Matrix:')
    print(' TN,  FP, FN, TP')
    print(confusion_matrix(y_true, y_pred).ravel())


if __name__=="__main__":
    df_dataset=pd.read_excel('/Users/thaarun/PythonProjects/TCGAProject/output/ML/Dataset.xlsx')

    df_x_train=df_dataset[df_dataset["TrainSplit"]=="Train"]
    df_x_train.drop(['TrainSplit', 'Metastasis','sites'], axis=1, inplace=True)

    df_y_train=df_dataset[df_dataset["TrainSplit"]=="Train"]["Metastasis"]

    df_x_test=df_dataset[df_dataset["TrainSplit"]=="Test"]
    df_x_test.drop(['TrainSplit', 'Metastasis','sites'], axis=1, inplace=True)

    df_y_test=df_dataset[df_dataset["TrainSplit"]=="Test"]["Metastasis"]
    print("Expected values to be predicted")
    print(df_y_test.tolist())



    # Support Vector Machine Classifier
    svm = SVC(C=100, class_weight='balanced')


    # Fitting Model to the train set
    #svm.fit(df_x_train, df_y_train)
    svm.fit(X_resampled, y_resampled)

    # Predicting on the test set
    y_pred = svm.predict(df_x_test)
    print("Actual values predicted")
    print(y_pred)

    # Evaluating model
    evaluation(df_y_test, y_pred)


    # Prediting for more M0
    df_x_predict0 = df_dataset[df_dataset["TrainSplit"] == "Predict0"]
    df_x_predict0.drop(['TrainSplit', 'Metastasis', 'sites'], axis=1, inplace=True)

    df_y_predict0 = df_dataset[df_dataset["TrainSplit"] == "Predict0"]["Metastasis"]
    print("Expected values to be predicted for Predict0")
    print(df_y_predict0.tolist())

    # Predicting on Predict0
    y_predict0 = svm.predict(df_x_predict0.fillna(0))
    print("Actual values predicted for Predict0")
    print(y_predict0)


    # Prediting for more MX
    df_x_predictx = df_dataset[df_dataset["TrainSplit"] == "PredictX"]
    df_x_predictx.drop(['TrainSplit', 'Metastasis', 'sites'], axis=1, inplace=True)

    df_y_predictx = df_dataset[df_dataset["TrainSplit"] == "PredictX"]["Metastasis"]
    print("Expected values to be predicted for PredictX")
    print(df_y_predictx.tolist())

    # Predicting on PredictX
    y_predictx = svm.predict(df_x_predictx)
    print("Actual values predicted for PredictX")
    print(y_predictx)

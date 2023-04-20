import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_auc_score
import pickle


def training_saving_model():
    """
    Function to train and save model
    args:
        None
    Returns:
        True: for succesfull trainging and saving of model
        False: for failure
    """
    try:
        flights_needed_data = pd.read_csv('data/final_data.csv').iloc[:,1:]
        data = flights_needed_data
        X, y = data.iloc[:,:-1], data.iloc[:,-1]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42,stratify=y)
        clf = DecisionTreeClassifier() # our trained model name is clf
        print("traingin_model")
        clf = clf.fit(X_train,y_train)
        filename = 'finalized_model.sav'
        pickle.dump(clf, open(filename, 'wb'))
        return "Done"
    except:
        raise Exception

def model_prediction(X_test):
    """
        Function to laod saved model and predict
        args:
            X_test: pandas.series
                    A single row containing all the values in the required fields to predict
        return:
            returns prdicted value
            0 -> flight not delayed
            1 -> flight delayed
    """
    try:
        # load the model from disk
        loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
        return loaded_model.predict(X_test)[0]
    except:
        raise Exception

if __name__ == "__main__":
    training_saving_model()
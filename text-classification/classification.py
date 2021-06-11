from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.naive_bayes import GaussianNB, MultinomialNB, CategoricalNB
from sklearn import svm
import glob
from sklearn.metrics import confusion_matrix

reviews = list()
classes = list()
classes_9 = list()


def analyze_data(vect, reviews_):
    matrix = vect.fit_transform(reviews_)
    freqs = zip(vect.get_feature_names(), matrix.sum(axis=0).tolist()[0])

    sorted_features = sorted(freqs, key=lambda x: -x[1])
    print("Najczęściej występujące słowo: ", sorted_features[0])
    print("Drugie najczęściej występujące słowo: ", sorted_features[1], sorted_features[2], sorted_features[3],
          sorted_features[4])
    print(len(sorted_features))

    single_occurrence_count = 0
    for i in range(len(sorted_features) - 1, 0, -1):
        if sorted_features[i][1] == 1:
            single_occurrence_count += 1
        else:
            break
    print("Liczba słów występujących tylko raz: ", single_occurrence_count)
    print("Jedno z najrzadziej występujących słów: ", sorted_features[len(sorted_features) - 1],
          sorted_features[len(sorted_features) - 2], sorted_features[len(sorted_features) - 3],
          sorted_features[len(sorted_features) - 4], sorted_features[len(sorted_features) - 5])
    review_length_avg = int(sum(map(len, reviews)) / len(reviews))
    print("Średnia długość recenzji: ", review_length_avg)


def load_data_from_files():
    global reviews, classes, classes_9
    for file in glob.glob('./scaledata/reviews/*'):
        with open(file, "r") as review_file:
            for line in review_file:
                reviews.append(line)

    for file in glob.glob('./scaledata/labels_3/*'):
        with open(file, "r") as classes_file:
            for line in classes_file:
                classes.append(line.strip())

    for file in glob.glob('./scaledata/labels_9/*.Scott+Renshaw'):
        with open(file, "r") as classes_file_9:
            for line in classes_file_9:
                classes_9.append(round(float(line.strip()), 1))

    # classes_count = dict()
    # for elem in classes:
    #     if elem in classes_count:
    #         classes_count[elem] += 1
    #     else:
    #         classes_count[elem] = 1
    #
    # classes_9_count = dict()
    # for elem in classes_9:
    #     if elem in classes_9_count:
    #         classes_9_count[elem] += 1
    #     else:
    #         classes_9_count[elem] = 1

    # print("Częstość występowania poszczególnych klas: ", classes_count)
    # print("Częstość występowania poszczególnych klas (rating): ", classes_9_count)


def get_normalized_data():
    # vect = CountVectorizer(stop_words='english')
    vect = TfidfVectorizer(analyzer='word', stop_words='english', norm='l2', min_df=0.009, max_df=0.3)
    all_features = vect.fit_transform(reviews)
    occ = all_features.toarray()
    return occ


def run_prediction_bayes(normalized_data):
    global reviews, classes, classes_9
    X_train, X_test, y_train, y_test = train_test_split(normalized_data, classes, test_size=0.1, random_state=109)
    gnb = MultinomialNB()
    y_pred = gnb.fit(X_train, y_train).predict(X_test)
    print(gnb.score(X_test, y_test))
    print("Number of mislabeled points out of a total %d points : %d" % (X_test.shape[0], (y_test != y_pred).sum()))
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    print('TP=', cm[0, 0], '\nTN=', cm[1, 1], '\nFP=', cm[0, 1], '\nFN=', cm[1, 0])
    res = cross_val_score(gnb, normalized_data, classes, cv=10, scoring="accuracy", verbose=2)
    print(res.mean())
    print(res)


def run_prediction_svm(normalized_data):
    global reviews, classes, classes_9
    clf = svm.SVC()
    X_train, X_test, y_train, y_test = train_test_split(normalized_data, classes, test_size=0.1, random_state=109)
    y_pred = clf.fit(X_train, y_train).predict(X_test)
    print(clf.score(X_test, y_test))
    print("Number of mislabeled points out of a total %d points : %d" % (X_test.shape[0], (y_test != y_pred).sum()))
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    res = cross_val_score(clf, normalized_data, classes, cv=10, scoring="accuracy", verbose=2)
    print(res.mean())
    print(res)


def grid_search(classifier, data, parameters):
    global reviews, classes
    print('[3/3] Starting GridSearch')
    gs = GridSearchCV(
        classifier,
        parameters,
        cv=10,
        verbose=3
    )
    gs.fit(data, classes)
    return gs.best_score_, gs.best_params_, gs.cv_results_['mean_test_score']


if __name__ == '__main__':
    load_data_from_files()
    normalized_data = get_normalized_data()
    clf = MultinomialNB()
    clf2 = svm.SVC()
    hyperSvc = {
        'C': [0.3, 0.5, 0.7, 1],
        'degree': [1, 2, 3, 4],
        'kernel': ['rbf', 'poly']
    }
    hyperBayes = {
        'alpha': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        'fit_prior': [True, False]
    }
    # a, b, c = grid_search(clf2, normalized_data, hyperSvc)
    # print('Best score: ',  a)
    # print('Best params: ', b)
    # print('Avgs: ', c)
    run_prediction_bayes(normalized_data)
    # run_prediction_svm(normalized_data)

from sklearn.feature_extraction.text import CountVectorizer
import glob

reviews = list()
classes = list()
classes_9 = list()

for file in glob.glob('./scaledata/reviews/*.Steve+Rhodes'):
    with open(file, "r") as review_file:
        for line in review_file:
            reviews.append(line)

for file in glob.glob('./scaledata/labels/*.Steve+Rhodes'):
    with open(file, "r") as classes_file:
        for line in classes_file:
            classes.append(line.strip())

for file in glob.glob('./scaledata/labels_9/*.Steve+Rhodes'):
    with open(file, "r") as classes_file_9:
        for line in classes_file_9:
            classes_9.append(round(float(line.strip()), 1))

classes_count = dict()
for elem in classes:
    if elem in classes_count:
        classes_count[elem] += 1
    else:
        classes_count[elem] = 1

classes_9_count = dict()
for elem in classes_9:
    if elem in classes_9_count:
        classes_9_count[elem] += 1
    else:
        classes_9_count[elem] = 1

print("Częstość występowania poszczególnych klas: ", classes_count)
print("Częstość występowania poszczególnych klas (rating): ", classes_9_count)

vect = CountVectorizer(stop_words='english')
all_features = vect.fit_transform(reviews)
occ = all_features.toarray()

matrix = vect.fit_transform(reviews)
freqs = zip(vect.get_feature_names(), matrix.sum(axis=0).tolist()[0])

sorted_features = sorted(freqs, key=lambda x: -x[1])
print("Najczęściej występujące słowo: ", sorted_features[0])
print("Drugie najczęściej występujące słowo: ", sorted_features[1], sorted_features[2], sorted_features[3], sorted_features[4])
print(len(sorted_features))

single_occurrence_count = 0
for i in range(len(sorted_features) - 1, 0, -1):
    if sorted_features[i][1] == 1:
        single_occurrence_count += 1
    else:
        break
print("Liczba słów występujących tylko raz: ", single_occurrence_count)
print("Jedno z najrzadziej występujących słów: ", sorted_features[len(sorted_features) - 1], sorted_features[len(sorted_features) - 2], sorted_features[len(sorted_features) - 3], sorted_features[len(sorted_features) - 4], sorted_features[len(sorted_features) - 5])
review_length_avg = int(sum(map(len, reviews)) / len(reviews))
print("Średnia długość recenzji: ", review_length_avg)

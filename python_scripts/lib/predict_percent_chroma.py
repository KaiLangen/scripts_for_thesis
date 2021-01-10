from numpy import genfromtxt
from sklearn.model_selection import train_test_split
from sklearn import datasets
from sklearn.linear_model import LinearRegression


data = genfromtxt('test_data.csv', delimiter=',')
y = data[:, 0]
X = data[:, 1:]

X_train, X_test, y_train, y_test = train_test_split(
             X, y, test_size=0.4, random_state=0)

X_train.shape, y_train.shape
((90, 4), (90,))
X_test.shape, y_test.shape
((60, 4), (60,))

clf = LinearRegression().fit(X_train, y_train)
score = clf.score(X_test, y_test)
print(score)

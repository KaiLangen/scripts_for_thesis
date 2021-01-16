from numpy import genfromtxt
from sklearn.model_selection import train_test_split
from sklearn import datasets
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score, cross_val_predict, KFold
from sklearn.metrics import r2_score as r2

from lib.build_test_data import *


train_file = "train_data.csv" 
test_file = "test_data.csv" 

def train_model():
    data = genfromtxt(train_file, delimiter=',')
    y = data[:, 0]
    X = data[:, 1:]

    model = LinearRegression()
    get_cross_val_score(model, X, y)
    model.fit(X, y)
    return model


def get_cross_val_score(model, X, y):
    pred = cross_val_predict(model, X, y, cv=len(X), n_jobs=-1)
    print("TRAINING SCORES: ", r2(pred,y))

def test_model(model):
    data = genfromtxt(test_file, delimiter=',')
    y = data[:, 0]
    X = data[:, 1:]
    print("TEST SCORE:", model.score(X, y))


def build_and_write_data(output_filename, bitrate_dir, si_ti_dir):
    si_data = get_normalized_si_ratios(si_ti_dir)
    percent_chroma_data, qps = get_true_percent_chroma_data(bitrate_dir)
    qp_data = {}
    for k,v in qps.items():
        qp_data[k] = get_normalized_qp(v)
    if is_qp_used:
        write_data_to_file(output_filename, percent_chroma_data, si_data, qp_data)
    else:
        write_data_to_file(output_filename, percent_chroma_data, si_data, None)


if __name__ == '__main__':
    if not len(sys.argv) == 6:
        print("Usage: python train_y test_y train_X test_X is_qp_used")
        sys.exit(1)

    is_qp_used = sys.argv[5] == "True"
    build_and_write_data(train_file, sys.argv[1], sys.argv[3])
    build_and_write_data(test_file, sys.argv[2], sys.argv[4])

    model = train_model()
    test_model(model)

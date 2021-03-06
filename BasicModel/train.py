# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time     : 2021/3/17 16:07
# @Author   : Yuan Chuxuan
# @File     : train.py

import joblib
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.pyplot import MultipleLocator
from mpl_toolkits.mplot3d import Axes3D
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit, GridSearchCV
from sklearn.svm import SVC

# setting font
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

model_paths = []  # outlook this global para


def display_RF(data: list):
    # draw a fig for rf
    data = np.array(data)
    x_data = data[:, 0]
    y_data = data[:, 1]
    z_data = data[:, 2]
    weight = data[:, 3]
    color = []
    for i in weight:  # setting colors
        if i > 0.93:
            color.append('#DC143C')
        elif i > 0.91:
            color.append('#FF1493')
        elif i > 0.88:
            color.append('#FF69B4')
        elif i > 0.86:
            color.append('#EE82EE')
        elif i > 0.84:
            color.append('#FF00FF')
        elif i > 0.78:
            color.append('#9400D3')
        elif i > 0.74:
            color.append('#6A5ACD')
        elif i > 0.70:
            color.append('#0000CD')
        elif i > 0.66:
            color.append('#4169E1')
        elif i > 0.62:
            color.append('#1E90FF')
        elif i > 0.58:
            color.append('#B0E0E6')
        elif i > 0.54:
            color.append('#7FFFAA')
        elif i > 0.50:
            color.append('#00FF7F')
        elif i > 0.46:
            color.append('#3CB371')
        else:
            color.append('#008000')

    fig = plt.figure()
    ax = Axes3D(fig)  # draw a 3D fig
    x_major_locator = MultipleLocator(1)
    ax.xaxis.set_major_locator(x_major_locator)
    ax.invert_xaxis()
    ax.scatter(x_data, y_data, z_data, c=color, label='parameter adjustment demonstration')

    ax.set_zlabel('md')
    ax.set_ylabel('mid')
    ax.set_xlabel('ne')

    address = '/home/ubuntu/CryptoClassification/verify_result/RF/parameter adjustment demonstration.png'  # attention ??????????????????
    plt.savefig(address)
    plt.show()
    return address


def RF_conv_test(dataset, ne, mid, md, fea_num, flag, crypto_list):
    """
    ????????? RF????????????

    :param dataset: ????????????
    :param ne: n_estimators
    :param mid: min_impurity_decrease
    :param md: max_depth
    :param fea_num: ??????????????????????????????????????????
    :param flag: True ????????????
    :param crypto_list: ??????????????????
    :return: ?????????
    """
    feature = []
    target = []
    for tmp in dataset:
        feature.append(tmp[0:fea_num])
        target.append(tmp[fea_num])
    # ???????????????????????????
    Xtrain, Xtest, Ytrain, Ytest = train_test_split(feature, target, test_size=0.3)

    # ????????????????????????
    rfc = RandomForestClassifier(n_estimators=ne, min_impurity_decrease=mid, criterion='gini', max_features='auto',
                                 oob_score=False,
                                 max_depth=md)
    # ????????????????????????????????????
    rfc = rfc.fit(Xtrain, Ytrain)
    # ??????
    feature_imp = rfc.feature_importances_
    score_r = rfc.score(Xtest, Ytest)
    # ????????????????????????
    if flag:
        s = ""
        for i in range(0, len(crypto_list)):
            s += crypto_list[i]
            if i != len(crypto_list) - 1:
                s += '_'
        joblib.dump(rfc, '/home/ubuntu/CryptoClassification/self_model/RF/' + s + '.model')
        model_paths.append('/home/ubuntu/CryptoClassification/self_model/RF/' + s + '.model')

    return score_r, feature_imp  # feature_imp is unused


def SVM_test(dataset, gamma_range, c_range, dimension, crypto_list):
    """
    ????????? SVM????????????

    :param dataset: ????????????
    :param gamma_range: gamma???????????????
    :param c_range: ?????????????????????
    :param dimension: ???????????? Attention????????????????????????????????????
    :param crypto_list: ??????????????????
    :return: ??????????????????c,gamma???????????????
    """
    feature = []
    target = []
    for tmp in dataset:
        feature.append(tmp[0:dimension])
        target.append(tmp[dimension])
    # ????????????
    train_data, test_data, train_target, test_target = train_test_split(feature, target, test_size=0.3)

    param_dic = dict(gamma=gamma_range, C=c_range)
    estimator = SVC(kernel='rbf')
    # ????????????
    cv = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=0)
    estimate = GridSearchCV(estimator, param_grid=param_dic, cv=cv)  # unused
    # ????????????
    fig_data = []
    bg = 0
    bc = 0
    max = 0
    for gamma in gamma_range:
        for c in c_range:
            estimator = SVC(kernel='rbf', gamma=gamma, C=c)
            estimator.fit(train_data, train_target)
            score = estimator.score(test_data, test_target)
            fig_data.append([gamma, c, score])
            if score > max:
                max = score
                bg = gamma
                bc = c
    fig_data = np.array(fig_data)

    x_data = fig_data[:, 0]
    y_data = fig_data[:, 1]
    z_data = fig_data[:, 2]
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x_data, y_data, z_data, c='b', label='parameter adjustment demonstration')
    ax.set_zlabel('acc')
    ax.set_ylabel('gamma')
    ax.set_xlabel('c')
    address = '/home/ubuntu/CryptoClassification/verify_result/SVM/parameter adjustment demonstration.png'
    plt.savefig(address)
    plt.show()

    return bg, bc, address


def SVM(dataset, g, c, dimension, crypto_list):
    """
    ??????????????????????????????????????????????????????

    :param dataset: ????????????
    :param g: same as gamma(best)
    :param c: same as C(best)
    :param dimension: ????????????
    :param crypto_list: ??????????????????
    :return: ?????????
    """
    feature = []
    target = []
    for tmp in dataset:
        feature.append(tmp[0:dimension])
        target.append(tmp[dimension])
    # ????????????
    train_data, test_data, train_target, test_target = train_test_split(feature, target, test_size=0.3)

    estimator = SVC(kernel='rbf', C=c, gamma=g)
    # ????????????
    estimator.fit(train_data, train_target, sample_weight=[])
    # ???????????????
    test_target_predict = estimator.predict(test_data)  # unused
    score = estimator.score(test_data, test_target)
    s = ""
    for i in range(0, len(crypto_list)):
        s += crypto_list[i]
        if i != len(crypto_list) - 1:
            s += '_'
    joblib.dump(estimator, '/home/ubuntu/CryptoClassification/self_model/SVM/' + s + '.model')
    model_paths.append('/home/ubuntu/CryptoClassification/self_model/SVM/' + s + '.model')
    return score


def load_data(crypto_list, model_name):
    col = []
    d = 192
    # d???????????????
    for i in range(1, d + 2):
        col.append(i)
    # ????????????
    with open('/home/ubuntu/CryptoClassification/static/feature/conv_feature_train.csv') as f:
        df = pd.read_csv(f, usecols=col)
        data = np.array(df).tolist()
    return data, d


def train(model_name, crypto_list):
    """
    ?????????????????????????????????

    :param model_name: ????????????
    :param crypto_list: ?????????????????????
    :return: ???????????????????????????????????????
    """
    fig_paths = ''
    if model_name == 'RF':
        fig_data = []
        bne = 0
        bmid = 0
        bmd = 0
        data, dimension = load_data(crypto_list, 'RF')
        max = 0
        for ne in range(110, 160, 4):
            for mid in np.linspace(0.01, 0.2, 10):
                for md in range(2, 18, 2):
                    tmp_score = RF_conv_test(data, ne, mid, md, dimension, flag=False, crypto_list=crypto_list)[0]
                    fig_data.append([ne, mid, md, tmp_score])
                    if tmp_score > max:
                        max = tmp_score
                        bne = ne
                        bmid = mid
                        bmd = md
        fig_paths = display_RF(fig_data)
        acc = RF_conv_test(data, bne, bmid, bmd, dimension, flag=True, crypto_list=crypto_list)[0]

    elif model_name == 'SVM':
        data, dimension = load_data(crypto_list, 'SVM')
        gamma_range = np.linspace(0.00001, 0.001, 20)
        C_range = np.linspace(1, 10, 20)
        bestg, bestc, fig_paths = SVM_test(data, gamma_range, C_range, dimension=dimension, crypto_list=crypto_list)
        acc = SVM(data, bestg, bestc, dimension, crypto_list)

    return acc, fig_paths, model_paths[0]  # ???????????????[0]

# pylint: disable-all

import numpy as np
import math
from scipy.io import loadmat
from .localanchorembedding import AnchorGraph
from sklearn.metrics import pairwise_distances
from sklearn.neighbors import KNeighborsClassifier
from scipy.spatial.distance import directed_hausdorff
from scipy.spatial.distance import pdist, squareform
from scipy.optimize import minimize
from sklearn.neighbors import NearestNeighbors
from scipy.linalg import norm
from sklearn import preprocessing

from numba import jit

from scipy.io import savemat
from scipy.sparse import csr_matrix
import os
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def CohortDistance(Data, DataLabel, linkC='average', metricC='euclidean'):
    """
    Need to be fixed: different LinkC, UPGMA, Hausdoff
    :param Data: cohort data points
    :param DataLabel: label of data points belong to different clusters
    :param linkC: type of distance between clusters: single, complete, average, Hausdoff
    :param metricC: type of distance between data points
    :return: distance matrix between clusters
    """
    u_Label = np.unique(DataLabel)
    l_label = len(u_Label)
    dCluster = np.zeros(shape=(l_label, l_label))
    DistData = pairwise_distances(Data, metric=metricC)
    for i in range(l_label):
        if len(DataLabel.shape) > 1:
            if DataLabel.shape[0] > DataLabel.shape[1]:
                tempi = np.squeeze(np.argwhere(
                    np.squeeze(DataLabel, axis=1) == u_Label[i]))
            else:
                tempi = np.squeeze(np.argwhere(
                    np.squeeze(DataLabel, axis=0) == u_Label[i]))
        else:
            tempi = np.squeeze(np.argwhere(DataLabel == u_Label[i]))
        for j in range(l_label):
            if i == j:
                dCluster[i, j] = 0
            else:
                tempj = np.squeeze(np.argwhere(
                    np.squeeze(DataLabel) == u_Label[j]))
                Dist_ij = DistData[np.ix_(tempi, tempj)]
                if linkC == 'single':
                    np.fill_diagonal(Dist_ij, float('inf'))
                    dCluster[i, j] = Dist_ij.min()
                    dCluster[j, i] = dCluster[i, j]
                    if Dist_ij.min() == float('inf'):
                        break
                elif linkC == 'complete':
                    dCluster[i, j] = Dist_ij.max()
                    dCluster[j, i] = dCluster[i, j]
                elif linkC == 'average':
                    ni = len(tempi)
                    nj = len(tempj)
                    dCluster[i, j] = np.sum(Dist_ij) / (ni * nj)
                    dCluster[j, i] = dCluster[i, j]
                elif linkC == 'Hausdoff':
                    tempCluster_i = Data[tempi, :]
                    tempCluster_j = Data[tempj, :]
                    dCluster[i, j] = directed_hausdorff(
                        tempCluster_i, tempCluster_j)[0]
                    dCluster[j, i] = dCluster[i, j]
                else:
                    print('Wrong Information')
                    break
    return dCluster


def Ad_cohort_order_chg(A_order, anchorlabel, linkage_order, k, param):
    lk = k.shape[0]
    l = A_order.shape[0]
    cohort_chg = int(np.ceil(param * lk))
    A_order_ad = np.zeros((l, l))
    for i in range(l):
        certain_label = anchorlabel[i]
        label_order = anchorlabel[A_order[i, :]]
        count = 0
        temp_Ai = A_order[i, :]
        temp_labelorder = label_order
        for j in range(cohort_chg):
            temp_label = k[linkage_order[k == certain_label, j]]
            i_same_location = np.where(label_order == temp_label)[0]
            temp_same_location = np.where(temp_labelorder == temp_label)[0]
            l_i_same_location = i_same_location.shape[0]
            A_order_ad[i, count: count +
                       l_i_same_location] = A_order[i, i_same_location]
            temp_Ai = np.delete(temp_Ai, temp_same_location)
            temp_labelorder = np.delete(temp_labelorder, temp_same_location)
            count = count + l_i_same_location
        A_order_ad[i, count: l] = temp_Ai

    return A_order_ad


def AdjacencyMatrix(Data, neighbor=10, weight=1, metric='euclidean'):
    # nbrs = NearestNeighbors(n_neighbors=neighbor + 1).fit(Data)
    # Aj = nbrs.kneighbors_graph(Data).toarray()
    Adis = squareform(pdist(Data, metric))
    # if metric == 'euclidean':
    # Adis = - (np.max(Adis) - Adis)
    Aj = k_nearest_neighbor(Adis, neighbor, weight, direction=0)
    # Aj = Aj * Adis
    # n = Data.shape[0]
    # Aj[range(n), range(n)] = 0
    # Aj = Aj / sum(sum(Aj))
    return Aj


def k_nearest_neighbor(disgraph, k=10, weight=1, direction=0):
    l = disgraph.shape[0]
    simgraph = np.zeros([l, l])
    for i in range(l):
        dis_sort = disgraph[i, :]
        dis_ascend = np.argsort(dis_sort)
        if weight == 1:
            simgraph[i, dis_ascend[1: k + 1]
                     ] = abs(dis_sort[dis_ascend[1: k + 1]])
        else:
            simgraph[i, dis_ascend[1: k + 1]] = 1
    if direction == 0:
        for i in range(l):
            for j in range(l):
                if i != j:
                    if simgraph[i, j] != simgraph[j, i]:
                        if simgraph[i, j] == 0:
                            simgraph[i, j] = simgraph[j, i]
                        if simgraph[j, i] == 0:
                            simgraph[j, i] = simgraph[i, j]
    return simgraph


def k_nearest_neighbor_disturb(disgraph, k=10, weight=1, direction=0):
    l = disgraph.shape[0]
    simgraph = np.zeros([l, l])
    dis_sort = np.sort(disgraph, axis=1)
    if k + 2 < l:
        temp_dis_min = dis_sort[:, k + 2] - dis_sort[:, k + 1]
        temp_num = sum(temp_dis_min) / l
        temp_count = 0
        while temp_num < 1:
            tempm = 2
            while temp_num == 0:
                tempm = tempm + 1
                if tempm <= l - k:
                    temp_dis_min_temp = dis_sort[:,
                                                 k + tempm] - dis_sort[:, k+1]
                    temp_num = sum(temp_dis_min_temp) / l
            temp_num = temp_num * 10
            temp_count = temp_count + 1
        if temp_num > 5:
            temp_count = np.round(np.power(10, temp_count - 1))
        else:
            temp_count = np.round(np.power(10, temp_count))
        delta = 1 / temp_count
    else:
        delta = 0

    for i in range(l):
        dis_sort = disgraph[i, :]
        dis_ascend = np.argsort(dis_sort)
        if weight == 1:
            simgraph[i, dis_ascend[1: k + 1]
                     ] = abs(dis_sort[dis_ascend[1: k + 1]])
        else:
            simgraph[i, dis_ascend[1: k + 1]] = 1
        if delta > 0:
            disminus = 0
            count = 1
            while(disminus <= delta):
                temp_disturb = dis_ascend[k + 1 + count]
                largest_dis = dis_ascend[k + 1]
                disminus = abs(temp_disturb - largest_dis)
                if disminus <= delta:
                    temp_k = np.squeeze(np.where(dis_sort == temp_disturb))
                    if weight == 1:
                        simgraph[i, temp_k] = temp_disturb
                    else:
                        simgraph[i, temp_k] = 1
                count = count + 1
                if k + 1 + count > l:
                    break

    if direction == 0:
        for i in range(l):
            for j in range(l):
                if i != j:
                    if simgraph[i, j] != simgraph[j, i]:
                        if simgraph[i, j] == 0:
                            simgraph[i, j] = simgraph[j, i]
                        if simgraph[j, i] == 0:
                            simgraph[j, i] = simgraph[i, j]
    return simgraph

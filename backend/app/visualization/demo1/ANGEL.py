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

from .FunctionFile import CohortDistance, Ad_cohort_order_chg
from .SOEmbedding import SOE, disForOE, Rtheta, Sscal

from scipy.io import savemat
from scipy.sparse import csr_matrix
import os
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def AnchorPointGeneration(
        Data,
        DataLabel,
        sparsity=0.1,
        t=3,
        metric='euclidean',
        cn=10):
  """
  Anchor point generation based on K-means method.
  Relationship matrix Z is obtained by LAE approach using t-nearest anchor points.

  :param Data: input data matrix in the high-dimensional space
  :param DataLabel: input label column
  :param sparsity: determine the number of the anchor points
  :param t: determine the t-nearest anchor points used to reconstruct each data point
  :param cn: # of iterations for LAE, usually set to 5-20;
  :param metric: type of distance
  :return:
  AnchorPoint: generated anchor points in the high-dimensional space
  AnchorLabel: label of AnchorPoints
  Z: weight matrix stores the relation between anchor points and data points
  """
  [l, D] = Data.shape
  diffLabel = np.unique(DataLabel)
  num_label = len(diffLabel)
  AnchorPoint = np.empty([0, D])
  AnchorLabel = np.empty([0, 1])
  Zset = {}
  for i in range(num_label):
    num_point = len(np.where(DataLabel == diffLabel[i])[0])
    numOfAnchor_temp = np.floor(num_point * sparsity)
    while numOfAnchor_temp <= 3:
      numOfAnchor_temp = numOfAnchor_temp * 2
    numOfAnchor_temp = int(numOfAnchor_temp)
    gtemp = Data[np.squeeze(DataLabel == diffLabel[i]), :]
    temp_Index = KMeans(n_clusters=numOfAnchor_temp, n_init=5).fit(gtemp)
    Anchortemp = temp_Index.cluster_centers_
    AnchorLabeltemp = diffLabel[i] * np.ones([numOfAnchor_temp, 1])
    AnchorPoint = np.concatenate((AnchorPoint, Anchortemp), axis=0)
    AnchorLabel = np.concatenate((AnchorLabel, AnchorLabeltemp), axis=0)
    Ztemp = AnchorGraph(gtemp, Anchortemp, 3, 10, metric)
    Zset[str(i)] = Ztemp

  # plt.scatter(AnchorPoint[:, 0], AnchorPoint[:, 1], c=AnchorLabel)
  # plt.show()
  Z = np.zeros([l, len(AnchorLabel)])
  for i in range(num_label):
    if DataLabel.shape[1] == l:
      DataLabel = DataLabel.transpose()
    datalocation = np.argwhere(
        np.squeeze(
            DataLabel,
            axis=1) == diffLabel[i])
    anchorlocation = np.argwhere(
        np.squeeze(AnchorLabel, axis=1) == diffLabel[i])
    Z[np.ix_(np.squeeze(datalocation, axis=1), np.squeeze(
      anchorlocation, axis=1))] = Zset[str(i)]
  return AnchorPoint, AnchorLabel, Z


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
      simgraph[i, dis_ascend[2: k + 1]
               ] = abs(dis_sort[dis_ascend[2: k + 1]])
    else:
      simgraph[i, dis_ascend[2: k + 1]] = 1
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


def AnchorEmbedding(
        Anchor,
        anchorlabel,
        flagMove=0,
        lamb=0.0,
        dim=2,
        init=0,
        flagDistanceMatrix=0,
        T=500,
        metric="euclidean",
        cohortmetric="average",
        scale=1):
  [l, D] = Anchor.shape
  if init == 0:
    init = np.random.random_sample((l, dim))
  if flagDistanceMatrix == 0:
    A = squareform(pdist(Anchor, metric))
  else:
    A = Anchor
  A_order = np.argsort(A, axis=1).astype(int)
  k = np.unique(anchorlabel)
  if lamb > 0:
    d_cohort = CohortDistance(Anchor, anchorlabel)
    linkage_order = np.argsort(d_cohort, axis=-1)
    A_order = Ad_cohort_order_chg(
        A_order, anchorlabel, linkage_order, k, lamb).astype(int)

  anchor0 = SOE(A_order.astype(int), anchorlabel, T=T, scale=scale)
  # plt.scatter(anchor0[:, 0], anchor0[:, 1], c=anchorlabel)
  # plt.show()

  if flagMove != 0:
    d_cohort = CohortDistance(Anchor, anchorlabel)
    C_order = np.argsort(d_cohort, axis=-1).astype(int)
    C = SOE(C_order.astype(int), k)
    # plt.scatter(C[:, 0], C[:, 1], c=k)
    # plt.show()
    C = C / (np.max(np.max(C)) / np.max(np.max(anchor0)))
    Param = SOE(A_order, anchorlabel, C=C, anchor=anchor0, flagMove=1)
    # SOE(Matrix, DataLabel, C=0, anchor=0, dim=2, Init=0, metric='euclidean', flagMove=0, T=500, eps=1e-6, scale=1)
    anchor = np.zeros((l, dim))
    aDelta = np.zeros((l, dim))
    for i in range(k.shape[0]):
      tempi = np.squeeze(anchorlabel == k[i])
      aDelta[tempi, :] = anchor0[tempi, :] - \
          np.mean(anchor0[tempi, :], axis=0)
      Theta = Rtheta(Param[i, 0])
      Scal = Sscal(Param[i, 1])
      anchor[tempi, :] = (
          Theta @ Scal @ aDelta[tempi, :].transpose()).transpose() + C[i, :]
    # plt.scatter(anchor[:, 0], anchor[:, 1], c=anchorlabel)
    # plt.show()
    # print(anchor)
  else:
    anchor = anchor0
    C = 0
  return anchor, anchor0, C


# def disForLOE(x):
#     # n = int(x.shape[0] / 2)
#     # x0 = np.reshape(x, (n, 2))
#     n = x.shape[0]
#     x0 = x
#     Del = 0.01
#     disgraph = squareform(pdist(x0, 'euclidean'))
#     return n, x0, Del, disgraph


def ErrLOE(x, A_order):
  n, x0, Del, disgraph = disForOE(x)
  tempj = np.argwhere(A_order > 0)
  lj = tempj.shape[0]
  templ = np.argwhere(A_order == 0)
  ll = templ.shape[0]
  E = ErrLOE_loop(n, Del, tempj, lj, templ, ll, disgraph)
  return E


@jit(nopython=True)
def ErrLOE_loop(n, Del, tempj, lj, templ, ll, disgraph):
  E = 0
  for i in range(0, lj):
    for j in range(0, ll):
      if tempj[i, 0] == templ[j, 0] and tempj[i, 0] != tempj[i, 1]:
        if templ[j, 0] != templ[j, 1]:
          temp = disgraph[tempj[i, 0], tempj[i, 1]] + \
              Del - disgraph[templ[j, 0], templ[j, 1]]
          if temp > 0:
            E = E + temp * temp
  return E


def GradLOE(x, A_order):
  n, x0, Del, disgraph = disForOE(x)
  tempj = np.argwhere(A_order > 0)
  lj = tempj.shape[0]
  templ = np.argwhere(A_order == 0)
  ll = templ.shape[0]
  gradX = GradLOE_loop(x0, n, Del, tempj, lj, templ, ll, disgraph)
  gradX0 = np.squeeze(np.reshape(gradX, (x.shape[0], 1)))
  return gradX0


@jit(nopython=True)
def GradLOE_loop(x0, n, Del, tempj, lj, templ, ll, disgraph):
  gradX = np.zeros((n, 2))
  for i in range(0, lj):
    for j in range(0, ll):
      if tempj[i, 0] == templ[j, 0] and tempj[i, 0] != tempj[i, 1]:
        if templ[j, 0] != templ[j, 1]:
          if disgraph[tempj[i, 0], tempj[i, 1]] + Del - \
                  disgraph[templ[j, 0], templ[j, 1]] > 0:
            temp = 1e-5
            if disgraph[tempj[i, 0], tempj[i, 1]] < temp:
              d_ij = temp
            else:
              d_ij = disgraph[tempj[i, 0], tempj[i, 1]]
            if disgraph[templ[j, 0], templ[j, 1]] < temp:
              d_ik = temp
            else:
              d_ik = disgraph[templ[j, 0], templ[j, 1]]
            x_i = x0[tempj[i, 0], :]
            x_j = x0[tempj[i, 1], :]
            x_k = x0[templ[j, 1], :]
            gradX[tempj[i, 0], :] = gradX[tempj[i, 0], :] + 2 * (
                disgraph[tempj[i, 0], tempj[i, 1]] -
                disgraph[templ[j, 0], templ[j, 1]] + Del) * ((x_i - x_j) / d_ij - (x_i - x_k) / d_ik)
            gradX[tempj[i, 1], :] = gradX[tempj[i, 1], :] - 2 * (
                disgraph[tempj[i, 0], tempj[i, 1]] -
                disgraph[templ[j, 0], templ[j, 1]] + Del) * ((x_i - x_j) / d_ij)
            gradX[templ[j, 1], :] = gradX[templ[j, 1], :] + 2 * (
                disgraph[tempj[i, 0], tempj[i, 1]] -
                disgraph[templ[j, 0], templ[j, 1]] + Del) * ((x_i - x_k) / d_ik)
  return gradX


def ANGEL_embedding(
        Data,
        anchor,
        Z,
        W,
        optType='constrained',
        dim=2,
        init=0,
        eps=0.05,
        metric='euclidean',
        T=80):
  [l, D] = Data.shape
  if init == 0:
    init = np.random.random_sample((l * dim, 1))
  LAEstart = Z @ anchor

  additional = W
  initstart = np.reshape(LAEstart, (l * dim, 1))
  if optType == 'constrained':

    bnds1 = [(LAEstart[i, 0] - eps, LAEstart[i, 0] + eps)
             for i in range(0, l)]
    bnds2 = [(LAEstart[i, 1] - eps, LAEstart[i, 1] + eps)
             for i in range(0, l)]
    bnds = []
    for i in range(0, l):
      bnds.append(bnds1[i])
      bnds.append(bnds2[i])
    x = minimize(
        ErrLOE,
        init,
        method='SLSQP',
        args=additional,
        jac=GradLOE,
        bounds=bnds,
        options={
            'disp': True,
            'maxiter': T})
    x = np.reshape(x.x, (l, dim))

  elif optType == 'fast':
    T = 5
    x = minimize(
        ErrLOE,
        initstart,
        method='BFGS',
        args=additional,
        jac=GradLOE,
        options={
            'disp': True,
            'maxiter': T})
    x = np.reshape(x.x, (l, dim))
  else:
    x = 0
    print('error')
  return x


# Main function


def angel():
  fullData = loadmat('./app/visualization/Data/OneFlower.mat')
  scaler = preprocessing.MinMaxScaler()
  # x = csr_matrix(fullData.get('newsdata')).toarray()

  # MY CODE For sampling
  SAMPLE_SIZE = 200
  sample = np.array(fullData.get('g'))[:SAMPLE_SIZE, :]
  scaler.fit(sample)
  g = scaler.transform(sample)
  label = np.array(fullData.get('label'))[:SAMPLE_SIZE].transpose()
  # ---- My code finished ----

  [AnchorPoint, AnchorLabel, Z] = AnchorPointGeneration(g, label)
  anchorpoint, anchor0, C = AnchorEmbedding(
      AnchorPoint, AnchorLabel, flagMove=0, lamb=0)
  scaler.fit(anchorpoint)
  anchorpoint = scaler.transform(anchorpoint)
  W = AdjacencyMatrix(g, neighbor=10, weight=0, metric='euclidean')
  result = ANGEL_embedding(g, anchorpoint, Z, W)
  if result.shape[1] == 2:
    zeros = b = np.zeros((result.shape[0], 1))
    result = np.hstack((result, zeros))

  return result, label


"""
neighbour: 341 | > 1 int DISPLAY
flagMove: 338 | 0 or 1 DISPLAY
lamb: 338 | 0 to 1 float DISPLAY
epsilone: 342 | 0 to 1 float DISPLAY
Embedding: 386 | 3-4 choices [from cova]
opttype: 400 | 2 choices [from cova] (2 choices not 3)
sparcityOfAnchorPoints: 0 to 0.5 float
metric: a choice of metric from scipy.spatial.distance
cohortmetric: average, single, complete, Hausdoff, central
"""

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


# x = Init
# if D == l and flagMove == 0:
#     H = 0.5
#     Del = 0.01
#     Err = []
#     disgraph = squareform(pdist(x, 'euclidean'))
#     E = ErrSOE(x, Del, Matrix, disgraph)
#     Err.append(E)
#     t = 1
#     while t < T:
#         gradX = GradSOE(x, Del, Matrix, disgraph)
#         tempE = E + 1
#         tempH = H
#         gradNorm = sum(sum(np.square(gradX)))
#         left = E - Del * tempH * gradNorm
#         xtemp = np.zeros((l, 2))
#         while left < tempE:
#             xtemp = x - Del * tempH * gradX
#             tempdisgraph = squareform(pdist(xtemp, 'euclidean'))
#             tempH = tempH * H
#             tempE = ErrSOE(xtemp, Del, Matrix, tempdisgraph)
#             left = E - Del * tempH * gradNorm
#         x = xtemp
#         disgraph = squareform(pdist(x, 'euclidean'))
#         E = ErrSOE(x, Del, Matrix, disgraph)
#         Err.append(E)
#         if np.abs(Err[t] - Err[t-1]) > eps:
#             print(t, 'error is', E)
#             t = t + 1
#             continue
#         else:
#             break


# @jit(nopython=True)
# def ErrSOE(x, Del, A_order, disgraph):
#     n = x.shape[0]
#     E = 0
#     count = 0
#     for i in range(0, n):
#         for j in range(1, n - 1):
#             for k in range(j + 1, n):
#                 temp = disgraph[A_order[i, 0], A_order[i, j]] + Del - disgraph[A_order[i, 0], A_order[i, k]]
#                 if temp > 0:
#                     E = E + np.square(temp)
#     return E


# @jit(nopython=True)
# def GradSOE(x, Del, A_order, disgraph):
#     n = x.shape[0]
#     gradX = np.zeros((n, 2))
#     for i in range(0, n):
#         for j in range(1, n - 1):
#             for k in range(j + 1, n):
#                 if disgraph[A_order[i, 0], A_order[i, j]] + Del - disgraph[A_order[i, 0], A_order[i, k]] > 0:
#                     temp = 1e-5
#                     if disgraph[A_order[i, 0], A_order[i, j]] < temp:
#                         d_ij = temp
#                     else:
#                         d_ij = disgraph[A_order[i, 0], A_order[i, j]]
#                     if disgraph[A_order[i, 0], A_order[i, k]] < temp:
#                         d_ik = temp
#                     else:
#                         d_ik = disgraph[A_order[i, 0], A_order[i, k]]
#                     x_i = x[A_order[i, 0], :]
#                     x_j = x[A_order[i, j], :]
#                     x_k = x[A_order[i, k], :]
#                     gradX[A_order[i, 0], :] = gradX[A_order[i, 0], :] + 2 * (
#                             disgraph[A_order[i, 0], A_order[i, j]] -
#                             disgraph[A_order[i, 0], A_order[i, k]] + Del) * ((x_i - x_j) / d_ij - (x_i - x_k) / d_ik)
#                     gradX[A_order[i, j], :] = gradX[A_order[i, j], :] - 2 * (
#                             disgraph[A_order[i, 0], A_order[i, j]] -
#                             disgraph[A_order[i, 0], A_order[i, k]] + Del) * ((x_i - x_j) / d_ij)
#                     gradX[A_order[i, k], :] = gradX[A_order[i, k], :] + 2 * (
#                             disgraph[A_order[i, 0], A_order[i, j]] -
#                             disgraph[A_order[i, 0], A_order[i, k]] + Del) * ((x_i - x_k) / d_ik)
#     return gradX


# def CohortDistance(Data, DataLabel, linkC='average', metricC='euclidean'):
#     """
#     Need to be fixed: different LinkC, UPGMA, Hausdoff
#     :param Data: cohort data points
#     :param DataLabel: label of data points belong to different clusters
#     :param linkC: type of distance between clusters: single, complete, average, Hausdoff
#     :param metricC: type of distance between data points
#     :return: distance matrix between clusters
#     """
#     u_Label = np.unique(DataLabel)
#     l_label = len(u_Label)
#     dCluster = np.zeros(shape=(l_label, l_label))
#     DistData = pairwise_distances(Data, metric=metricC)
#     for i in range(l_label):
#         tempi = np.squeeze(np.argwhere(np.squeeze(DataLabel, axis=1) == u_Label[i]), axis=1)
#         for j in range(l_label):
#             if i == j:
#                 dCluster[i, j] = 0
#             else:
#                 tempj = np.squeeze(np.argwhere(np.squeeze(DataLabel, axis=1) == u_Label[j]), axis=1)
#                 Dist_ij = DistData[np.ix_(tempi, tempj)]
#                 if linkC == 'single':
#                     np.fill_diagonal(Dist_ij, float('inf'))
#                     dCluster[i, j] = Dist_ij.min()
#                     dCluster[j, i] = dCluster[i, j]
#                     if Dist_ij.min() == float('inf'):
#                         break
#                 elif linkC == 'complete':
#                     dCluster[i, j] = Dist_ij.max()
#                     dCluster[j, i] = dCluster[i, j]
#                 elif linkC == 'average':
#                     ni = len(tempi)
#                     nj = len(tempj)
#                     dCluster[i, j] = np.sum(Dist_ij) / (ni * nj)
#                     dCluster[j, i] = dCluster[i, j]
#                 elif linkC == 'Hausdoff':
#                     tempCluster_i = Data[tempi, :]
#                     tempCluster_j = Data[tempj, :]
#                     dCluster[i, j] = directed_hausdorff(tempCluster_i, tempCluster_j)[0]
#                     dCluster[j, i] = dCluster[i, j]
#                 else:
#                     print('Wrong Information')
#                     break
#     return dCluster


# def SOE(Matrix, DataLabel, C=0, anchor=0, dim=2, Init=0, metric='euclidean', flagMove=0, T=500, eps=1e-6, scale=1):
#     [l, D] = Matrix.shape
#     if Init == 0:
#         Init = np.random.random_sample((l, dim))
#     if flagMove == 1:
#         # l1 = -0.5 * np.pi * np.ones((C.shape[0], 1))
#         # u1 = 0.5 * np.pi * np.ones((C.shape[0], 1))
#         # l2 = np.zeros((C.shape[0], 1))
#         # u2 = scale * np.ones((C.shape[0], 1))
#         # b1 = np.concatenate((l1, l2), axis=0)
#         # b2 = np.concatenate((u1, u2), axis=0)
#         Init = np.random.random_sample((C.shape[0], dim))
#
#         bnds1 = [(-0.5 * np.pi, 0.5 * np.pi) for i in range(0, C.shape[0])]
#         bnds2 = [(0, scale) for i in range(0, C.shape[0])]
#         bnds = bnds1 + bnds2
#
#         additional = (Matrix, anchor, C, DataLabel)
#         # init = np.reshape(Init, (2*C.shape[0], 1))
#         # E = ErrSOE_Relocate(init, *additional)
#         # grad = GradSOE_Relocate(init, *additional)
#
#         x = minimize(ErrSOE_Relocate, Init, method='SLSQP', args=additional, jac=GradSOE_Relocate,
#                      bounds=bnds, options={'disp': True, 'maxiter': 50})
#         x = np.reshape(x.x, (C.shape[0], dim))
#     elif D == l and flagMove == 0:
#         x = minimize(ErrSOE, Init, method='BFGS', args=Matrix, jac=GradSOE,
#                      options={'gtol': eps, 'disp': True, 'maxiter': T})
#         x = np.reshape(x.x, (l, dim))
#     elif D == 3 and flagMove == 0:
#         x = minimize(ErrSOE_triplet, Init, method='BFGS', args=Matrix, jac=GradSOE_triplet,
#                      options={'gtol': eps, 'disp': True, 'maxiter': T})
#         x = np.reshape(x.x, (l, dim))
#     else:
#         print('Wrong matrix')
#         return 0
#     return x
#
#
# def PreForRelocationOE(Param, anchor0, anchorC, label):
#     Del = 0.01
#     c = int(Param.shape[0] / 2)
#     [n, p] = anchor0.shape
#     x = np.zeros((n, p))
#     delx = np.zeros((n, p))
#     theta = Param[0: c]
#     scal = Param[c: Param.shape[0]]
#     diffLabel = np.unique(label)
#     for i in range(diffLabel.shape[0]):
#         templ = np.squeeze(label == diffLabel[i], axis=1)
#         delx[templ, :] = anchor0[templ, :] - np.mean(anchor0[templ, :], axis=0)
#         Theta = Rtheta(theta[i])
#         Scal = Sscal(scal[i])
#         x[templ, :] = (Theta @ Scal @ delx[templ, :].transpose()).transpose() + anchorC[i, :]
#     disgraph = squareform(pdist(x, 'euclidean'))
#     return n, x, delx, disgraph, theta, scal, diffLabel, Del
#
#
# def Rtheta(theta):
#     k = np.array([[np.cos(theta), - np.sin(theta)], [np.sin(theta), np.cos(theta)]])
#     if len(k.shape) > 2:
#         k = np.squeeze(k, axis=2)
#     return k
#
#
# def gradRtheta(theta):
#     k = np.array([[- np.sin(theta), -np.cos(theta)], [np.cos(theta), - np.sin(theta)]])
#     if len(k.shape) > 2:
#         k = np.squeeze(k, axis=2)
#     return k
#
#
# def Sscal(scal):
#     return np.array([[scal, 0], [0, scal]], dtype=float)
#
#
# def ErrSOE_Relocate(Param, *args):
#     A_order, anchor0, anchorC, labels = args[0], args[1], args[2], args[3]
#     n, x, delx, disgraph, theta, scal, diffLabel, Del = PreForRelocationOE(Param, anchor0, anchorC, labels)
#     E = ErrSOE_Relocate_loop(n, Del, A_order, disgraph, label)
#     return E
#
#
# @jit(nopython=True)
# def ErrSOE_Relocate_loop(n, Del, A_order, disgraph, labels):
#     E = 0
#     for i in range(0, n):
#         for j in range(1, n - 1):
#             for k in range(j + 1, n):
#                 if labels[A_order[i, 0]] == labels[A_order[i, j]]:
#                     if labels[A_order[i, 0]] == labels[A_order[i, k]]:
#                         temp = disgraph[A_order[i, 0], A_order[i, j]] + Del - disgraph[A_order[i, 0], A_order[i, k]]
#                         if temp > 0:
#                             E = E + temp * temp
#     return E
#
#
# def GradSOE_Relocate(Param, *args):
#     A_order, anchor0, anchorC, labels = args[0], args[1], args[2], args[3]
#     n, x, delx, disgraph, theta, scal, diffLabel, Del = PreForRelocationOE(Param, anchor0, anchorC, labels)
#     gradX = GradSOE_Relocate_loop(delx, n, Del, A_order, disgraph, theta, scal, anchorC, diffLabel, labels)
#     gradX0 = np.squeeze(np.reshape(gradX, (Param.shape[0], 1)))
#     return gradX0
#
#
# def RS(theta, scal):
#     if len(Rtheta(theta).shape) > 2:
#         R = np.squeeze(Rtheta(theta), axis=2)
#     else:
#         R = Rtheta(theta)
#     return R @ Sscal(scal)
#
#
# def gradRS(theta, scal):
#     if len(gradRtheta(theta).shape) > 2:
#         R = np.squeeze(gradRtheta(theta), axis=2)
#     else:
#         R = gradRtheta(theta)
#     return R @ Sscal(scal)
#
#
# def GradSOE_Relocate_loop(delx, n, Del, A_order, disgraph, theta, scal, C, diffLabel, labels):
#     gradT = np.zeros((theta.shape[0], 2))
#     for i in range(0, n):
#         for j in range(1, n - 1):
#             for k in range(j + 1, n):
#                 if labels[A_order[i, 0]] == labels[A_order[i, j]] and labels[A_order[i, 0]] == labels[A_order[i, k]]:
#                     if disgraph[A_order[i, 0], A_order[i, j]] + Del - disgraph[A_order[i, 0], A_order[i, k]] > 0:
#                         temp = 1e-5
#                         if disgraph[A_order[i, 0], A_order[i, j]] < temp:
#                             d_ij = temp
#                         else:
#                             d_ij = disgraph[A_order[i, 0], A_order[i, j]]
#                         if disgraph[A_order[i, 0], A_order[i, k]] < temp:
#                             d_ik = temp
#                         else:
#                             d_ik = disgraph[A_order[i, 0], A_order[i, k]]
#
#                         if len((diffLabel == label[A_order[i, 0]]).shape) > 1:
#                             li = np.squeeze(diffLabel == label[A_order[i, 0]], axis=1)
#                             lj = np.squeeze(diffLabel == label[A_order[i, j]], axis=1)
#                             lk = np.squeeze(diffLabel == label[A_order[i, k]], axis=1)
#                         else:
#                             li = diffLabel == label[A_order[i, 0]]
#                             lj = diffLabel == label[A_order[i, j]]
#                             lk = diffLabel == label[A_order[i, k]]
#
#                         if len(theta[li]) > 1:
#                             theta_li = np.squeeze(theta[li], axis=1)
#                             theta_lj = np.squeeze(theta[lj], axis=1)
#                             theta_lk = np.squeeze(theta[lk], axis=1)
#                             scal_li = np.squeeze(scal[li], axis=1)
#                             scal_lj = np.squeeze(scal[lj], axis=1)
#                             scal_lk = np.squeeze(scal[lk], axis=1)
#                         else:
#                             theta_li = theta[li]
#                             theta_lj = theta[lj]
#                             theta_lk = theta[lk]
#                             scal_li = scal[li]
#                             scal_lj = scal[lj]
#                             scal_lk = scal[lk]
#
#                         x_i = (RS(theta_li, scal_li) @ delx[A_order[i, 0], :].transpose()).transpose() + C[li, :]
#                         x_j = (RS(theta_lj, scal_lj) @ delx[A_order[i, j], :].transpose()).transpose() + C[lj, :]
#                         x_k = (RS(theta_lk, scal_lk) @ delx[A_order[i, k], :].transpose()).transpose() + C[lk, :]
#
#                         gradXi = 2 * (disgraph[A_order[i, 0], A_order[i, j]] - disgraph[
#                             A_order[i, 0], A_order[i, k]] + Del) * ((x_i - x_j) / d_ij - (x_i - x_k) / d_ik)
#                         gradXj = - 2 * (disgraph[A_order[i, 0], A_order[i, j]] - disgraph[
#                             A_order[i, 0], A_order[i, k]] + Del) * ((x_i - x_j) / d_ij)
#                         gradXk = 2 * (disgraph[A_order[i, 0], A_order[i, j]] - disgraph[
#                             A_order[i, 0], A_order[i, k]] + Del) * ((x_i - x_k) / d_ik)
#
#                         gradT[li, 0] = gradT[li, 0] + gradXi @ gradRS(theta_li, scal_li) @ delx[A_order[i, 0],
#                                                                                            :].transpose()
#                         gradT[lj, 0] = gradT[lj, 0] + gradXj @ gradRS(theta_li, scal_lj) @ delx[A_order[i, j],
#                                                                                            :].transpose()
#                         gradT[lk, 0] = gradT[lk, 0] + gradXk @ gradRS(theta_lk, scal_lk) @ delx[A_order[i, k],
#                                                                                            :].transpose()
#
#                         gradT[li, 1] = gradT[li, 1] + gradXi @ Rtheta(theta_li) @ delx[A_order[i, 0],
#                                                                                   :].transpose()
#                         gradT[lj, 1] = gradT[lj, 1] + gradXj @ Rtheta(theta_lj) @ delx[A_order[i, j],
#                                                                                   :].transpose()
#                         gradT[lk, 1] = gradT[lk, 1] + gradXk @ Rtheta(theta_lk) @ delx[A_order[i, k],
#                                                                                   :].transpose()
#     return gradT
#
#
# def disForOE(x):
#     n = int(x.shape[0] / 2)
#     x0 = np.reshape(x, (n, 2))
#     Del = 0.01
#     disgraph = squareform(pdist(x0, 'euclidean'))
#     return n, x0, Del, disgraph
#
#
# def ErrSOE(x, A_order):
#     n, x0, Del, disgraph = disForOE(x)
#     E = ErrSOE_loop(n, Del, A_order, disgraph)
#     return E
#
#
# @jit(nopython=True)
# def ErrSOE_loop(n, Del, A_order, disgraph):
#     E = 0
#     for i in range(0, n):
#         for j in range(1, n - 1):
#             for k in range(j + 1, n):
#                 temp = disgraph[A_order[i, 0], A_order[i, j]] + Del - disgraph[A_order[i, 0], A_order[i, k]]
#                 if temp > 0:
#                     E = E + temp * temp
#     return E
#
#
# def GradSOE(x, A_order):
#     n, x0, Del, disgraph = disForOE(x)
#     gradX = GradSOE_loop(x0, n, Del, A_order, disgraph)
#     gradX0 = np.squeeze(np.reshape(gradX, (x.shape[0], 1)))
#     return gradX0
#
#
# @jit(nopython=True)
# def GradSOE_loop(x0, n, Del, A_order, disgraph):
#     gradX = np.zeros((n, 2))
#     for i in range(0, n):
#         for j in range(1, n - 1):
#             for k in range(j + 1, n):
#                 if disgraph[A_order[i, 0], A_order[i, j]] + Del - disgraph[A_order[i, 0], A_order[i, k]] > 0:
#                     temp = 1e-5
#                     if disgraph[A_order[i, 0], A_order[i, j]] < temp:
#                         d_ij = temp
#                     else:
#                         d_ij = disgraph[A_order[i, 0], A_order[i, j]]
#                     if disgraph[A_order[i, 0], A_order[i, k]] < temp:
#                         d_ik = temp
#                     else:
#                         d_ik = disgraph[A_order[i, 0], A_order[i, k]]
#                     x_i = x0[A_order[i, 0], :]
#                     x_j = x0[A_order[i, j], :]
#                     x_k = x0[A_order[i, k], :]
#                     gradX[A_order[i, 0], :] = gradX[A_order[i, 0], :] + 2 * (
#                             disgraph[A_order[i, 0], A_order[i, j]] -
#                             disgraph[A_order[i, 0], A_order[i, k]] + Del) * ((x_i - x_j) / d_ij - (x_i - x_k) / d_ik)
#                     gradX[A_order[i, j], :] = gradX[A_order[i, j], :] - 2 * (
#                             disgraph[A_order[i, 0], A_order[i, j]] -
#                             disgraph[A_order[i, 0], A_order[i, k]] + Del) * ((x_i - x_j) / d_ij)
#                     gradX[A_order[i, k], :] = gradX[A_order[i, k], :] + 2 * (
#                             disgraph[A_order[i, 0], A_order[i, j]] -
#                             disgraph[A_order[i, 0], A_order[i, k]] + Del) * ((x_i - x_k) / d_ik)
#     return gradX
#
#
# def ErrSOE_triplet(x, A_order):
#     n, x0, Del, disgraph = disForOE(x)
#     E = ErrSOE_triplet_loop(n, Del, A_order, disgraph)
#     return E
#
#
# @jit(nopython=True)
# def ErrSOE_triplet_loop(n, Del, A_order, disgraph):
#     E = 0
#     for i in range(0, n):
#         temp_order = A_order[i, :]
#         temp = disgraph[temp_order[i, 0], temp_order[i, 1]] + Del - disgraph[temp_order[i, 0], temp_order[i, 2]]
#         if temp > 0:
#             E = E + temp * temp
#     return E
#
#
# def GradSOE_triplet(x, A_order):
#     n, x0, Del, disgraph = disForOE(x)
#     gradX = GradSOE_triplet_loop(x0, n, Del, A_order, disgraph)
#     gradX0 = np.squeeze(np.reshape(gradX, (x.shape[0], 1)))
#     return gradX0
#
#
# @jit(nopython=True)
# def GradSOE_triplet_loop(x0, n, Del, A_order, disgraph):
#     gradX = np.zeros((n, 2))
#     for i in range(0, n):
#         temp_order = A_order[i, :]
#         if disgraph[temp_order[i, 0], temp_order[i, 1]] + Del - disgraph[temp_order[i, 0], temp_order[i, 2]] > 0:
#             temp = 1e-5
#             if disgraph[temp_order[i, 0], temp_order[i, 1]] < temp:
#                 d_ij = temp
#             else:
#                 d_ij = disgraph[temp_order[i, 0], temp_order[i, 1]]
#             if disgraph[temp_order[i, 0], temp_order[i, 2]] < temp:
#                 d_ik = temp
#             else:
#                 d_ik = disgraph[temp_order[i, 0], temp_order[i, 2]]
#             x_i = x0[temp_order[i, 0], :]
#             x_j = x0[temp_order[i, 1], :]
#             x_k = x0[temp_order[i, 2], :]
#             gradX[temp_order[i, 0], :] = gradX[temp_order[i, 0], :] + 2 * (
#                     disgraph[temp_order[i, 0], temp_order[i, 1]] -
#                     disgraph[temp_order[i, 0], temp_order[i, 2]] + Del) * ((x_i - x_j) / d_ij - (x_i - x_k) / d_ik)
#             gradX[temp_order[i, 1], :] = gradX[temp_order[i, 1], :] - 2 * (
#                     disgraph[temp_order[i, 0], temp_order[i, 1]] -
#                     disgraph[temp_order[i, 0], temp_order[i, 2]] + Del) * ((x_i - x_j) / d_ij)
#             gradX[temp_order[i, 2], :] = gradX[temp_order[i, 2], :] + 2 * (
#                     disgraph[temp_order[i, 0], temp_order[i, 1]] -
#                     disgraph[temp_order[i, 0], temp_order[i, 2]] + Del) * ((x_i - x_k) / d_ik)
#     return gradX
#
#
# def Ad_cohort_order_chg(A_order, anchorlabel, linkage_order, k, param):
#     lk = k.shape[0]
#     l = A_order.shape[0]
#     cohort_chg = int(np.ceil(param * lk))
#     A_order_ad = np.zeros((l, l))
#     for i in range(l):
#         certain_label = anchorlabel[i]
#         label_order = anchorlabel[A_order[i, :]]
#         count = 0
#         temp_Ai = A_order[i, :]
#         temp_labelorder = label_order
#         for j in range(cohort_chg):
#             temp_label = k[linkage_order[k == certain_label, j]]
#             i_same_location = np.where(label_order == temp_label)[0]
#             temp_same_location = np.where(temp_labelorder == temp_label)[0]
#             l_i_same_location = i_same_location.shape[0]
#             A_order_ad[i, count: count + l_i_same_location] = A_order[i, i_same_location]
#             temp_Ai = np.delete(temp_Ai, temp_same_location)
#             temp_labelorder = np.delete(temp_labelorder, temp_same_location)
#             count = count + l_i_same_location
#         A_order_ad[i, count: l] = temp_Ai
#
#     return A_order_ad

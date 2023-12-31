# pylint: disable-all

import numpy as np
from scipy.io import loadmat, savemat
from .localanchorembedding import AnchorGraph
from scipy.spatial.distance import pdist, cdist, squareform
from scipy.optimize import minimize
from sklearn import preprocessing
from numba import jit
from .FunctionFile import CohortDistance, Ad_cohort_order_chg, AdjacencyMatrix, funInit, postProcessing
from .SOEmbedding import SOE, disForOE, Rtheta, Sscal
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.sparse import csr_matrix, isspmatrix_csr
from sklearn.neighbors import kneighbors_graph


def AnchorPointGeneration(Data, DataLabel, sparsity=0.1, t=3, metric='euclidean', cn=10):
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
    if num_point == 1:
      Anchortemp = Data[np.squeeze(DataLabel == diffLabel[i]), :]
      if len(Anchortemp.shape) < 2:
        Anchortemp = Anchortemp.reshape([1, Anchortemp.shape[0]])
      AnchorLabeltemp = np.array([diffLabel[i]]).reshape((1, 1))
      AnchorPoint = np.concatenate((AnchorPoint, Anchortemp), axis=0)
      AnchorLabel = np.concatenate((AnchorLabel, AnchorLabeltemp), axis=0)
      Zset[str(i)] = np.array([1])
    else:
      numOfAnchor_temp = np.floor(num_point * sparsity)
      if numOfAnchor_temp == 0:
        numOfAnchor_temp = 1
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
  print('finish generation')
  Z = np.zeros([l, len(AnchorLabel)])
  for i in range(num_label):
    if len(DataLabel.shape) > 1:
      if DataLabel.shape[1] == l:
        DataLabel = DataLabel.transpose()
      DataLabel = np.squeeze(DataLabel)
    if len(AnchorLabel.shape) > 1:
      if AnchorLabel.shape[1] == l:
        AnchorLabel = AnchorLabel.transpose()
      AnchorLabel = np.squeeze(AnchorLabel)
    datalocation = np.argwhere(DataLabel == diffLabel[i])
    anchorlocation = np.argwhere(AnchorLabel == diffLabel[i])
    Z[np.ix_(np.squeeze(datalocation, axis=1), np.squeeze(
      anchorlocation, axis=1))] = Zset[str(i)]
  print('finish Z')
  return AnchorPoint, AnchorLabel, Z


def AnchorEmbedding(
        Anchor,
        anchorlabel,
        flagMove=0,
        lamb=0.0,
        dim=2,
        init=0,
        flagDistanceMatrix=0,
        T=200,
        metric="euclidean",
        cohortmetric="average",
        scale=1,
        cinit=0):
  l = Anchor.shape[0]
  if isinstance(init, int):
    # np.random.seed(0)
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

  anchor0 = SOE(A_order.astype(int), anchorlabel,
                Init=init, T=T, scale=scale, dim=dim)
  # plt.scatter(anchor0[:, 0], anchor0[:, 1], c=anchorlabel)
  # plt.show()
  scaler = preprocessing.MinMaxScaler()
  scaler.fit(anchor0)
  anchor0 = scaler.transform(anchor0)

  if flagMove != 0:
    d_cohort = CohortDistance(Anchor, anchorlabel)
    C_order = np.argsort(d_cohort, axis=-1).astype(int)
    C = SOE(C_order.astype(int), k, dim=dim, Init=cinit)
    plt.scatter(C[:, 0], C[:, 1], c=k)
    plt.show()
    scaler.fit(C)
    # C = C / (np.max(np.max(C)) / np.max(np.max(anchor0)))
    C = scaler.transform(C) * 2
    Param = SOE(A_order, anchorlabel, C=C,
                anchor=anchor0, flagMove=1, dim=dim, T=20)
    anchor = np.zeros((l, dim))
    aDelta = np.zeros((l, dim))
    for i in range(k.shape[0]):
      tempi = np.squeeze(anchorlabel == k[i])
      aDelta[tempi, :] = anchor0[tempi, :] - np.mean(anchor0[tempi, :], axis=0)
      Theta = Rtheta(Param[i, 0], dim=dim, C=C[i, :])
      Scal = Sscal(Param[i, 1], dim=dim)
      # anchor[tempi, :] = (Theta @ Scal @ aDelta[tempi, :].transpose()).transpose() + C[i, :]
      anchor[tempi, :] = (Theta.dot(Scal).dot(
          aDelta[tempi, :].transpose())).transpose() + C[i, :]
  else:
    anchor = anchor0
    C = 0
  return anchor, anchor0, C


def ErrLOE(x, *args):
  A_order, dim = args[0], args[1]
  n, x0, Del, disgraph = disForOE(x, dim)
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


def GradLOE(x, *args):
  A_order, dim = args[0], args[1]
  n, x0, Del, disgraph = disForOE(x, dim)
  tempj = np.argwhere(A_order > 0)
  lj = tempj.shape[0]
  templ = np.argwhere(A_order == 0)
  ll = templ.shape[0]
  gradX = GradLOE_loop(x0, n, Del, dim, tempj, lj, templ, ll, disgraph)
  gradX0 = np.squeeze(np.reshape(gradX, (x.shape[0], 1)))
  return gradX0


@jit(nopython=True)
def GradLOE_loop(x0, n, Del, dim, tempj, lj, templ, ll, disgraph):
  gradX = np.zeros((n, dim))
  for i in range(0, lj):
    for j in range(0, ll):
      if tempj[i, 0] == templ[j, 0] and tempj[i, 0] != tempj[i, 1]:
        if templ[j, 0] != templ[j, 1]:
          if disgraph[tempj[i, 0], tempj[i, 1]] + Del - disgraph[templ[j, 0], templ[j, 1]] > 0:
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


def reformX(x, dim):
  n = int(x.shape[0] / dim)
  x0 = np.reshape(x, (n, dim))
  return x0


def ErrTSNE(x, *args):
  A_order, dim = args[0], args[1]
  x0 = reformX(x, dim)
  if isspmatrix_csr(A_order):
    A_order = A_order.toarray()
  E = TSNEcost(x0, A_order)
  return E


def GradTSNE(x, *args):
  A_order, dim = args[0], args[1]
  if isspmatrix_csr(A_order):
    A_order = A_order.toarray()
  x0 = reformX(x, dim)
  grad = TSNEgrad(x0, A_order)
  gradX0 = np.squeeze(np.reshape(grad, (x.shape[0], 1)))
  return gradX0


def TSNEcost(x, Ad):
  n = Ad.shape[0]
  P = Ad / Ad.sum()
  d2 = squareform(pdist(x, 'euclidean'))
  d2 = d2 * d2
  Q = 1 / (1 + d2)
  Q[range(n), range(n)] = 0
  Q_n = Q / sum(Q)
  Q_n = np.maximum(Q_n, 1e-12)
  y = -P * np.log(Q_n)
  y[range(n), range(n)] = 0
  o = sum(sum(y))
  return o


def TSNEgrad(x, Ad):
  n = Ad.shape[0]
  P = Ad / Ad.sum()
  d2 = squareform(pdist(x, 'euclidean'))
  d2 = d2 * d2
  Q = 1 / (1 + d2)
  Q[range(n), range(n)] = 0
  Q_n = Q / sum(Q)
  Q_n = np.maximum(Q_n, 1e-12)
  L = (P - Q_n) * Q
  gd = 4 * (np.diag(np.sum(L, axis=0)) - L).dot(x)
  return gd


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
        T=80,
        neighbor=10):
  [l, D] = Data.shape
  if isinstance(init, int):
    # np.random.seed(0)
    init = np.random.random_sample((l * dim, 1))
  else:
    if len(init.shape) > 1:
      init = np.reshape(init, (l * dim, 1))
  LAEstart = Z.dot(anchor)
  additional = (W, dim)
  initstart = np.reshape(LAEstart, (l * dim, 1))
  if dim == 2:
    bnds1 = [(LAEstart[i, 0] - eps, LAEstart[i, 0] + eps) for i in range(0, l)]
    bnds2 = [(LAEstart[i, 1] - eps, LAEstart[i, 1] + eps) for i in range(0, l)]
    bnds = []
    for i in range(0, l):
      bnds.append(bnds1[i])
      bnds.append(bnds2[i])
  elif dim == 3:
    bnds1 = [(LAEstart[i, 0] - eps, LAEstart[i, 0] + eps) for i in range(0, l)]
    bnds2 = [(LAEstart[i, 1] - eps, LAEstart[i, 1] + eps) for i in range(0, l)]
    bnds3 = [(LAEstart[i, 2] - eps, LAEstart[i, 2] + eps) for i in range(0, l)]
    bnds = []
    for i in range(0, l):
      bnds.append(bnds1[i])
      bnds.append(bnds2[i])
      bnds.append(bnds3[i])
  else:
    print('error')
    return
  if optType == 'constrained':
    x = minimize(ErrLOE, x0=init, method='SLSQP', args=additional, jac=GradLOE,
                 bounds=bnds, options={'disp': True, 'maxiter': T})
    x = np.reshape(x.x, (l, dim))

  elif optType == 'fast':
    W0 = kneighbors_graph(Data, neighbor, mode='distance', include_self=False)
    additional = (W0, dim)
    x = minimize(ErrTSNE, x0=initstart, method='L-BFGS-B', args=additional, jac=GradTSNE,
                 bounds=bnds, options={'disp': True, 'maxiter': T})
    x = np.reshape(x.x, (l, dim))
  else:
    x = 0
    print('error')
  return x


def draw_vector(v0, v1, ax=None):
  ax = ax or plt.gca()
  arrowprops = dict(arrowstyle='->',
                    linewidth=2,
                    shrinkA=0, shrinkB=0)
  ax.annotate('', v1, v0, arrowprops=arrowprops)


if __name__ == '__main__':
  fullData = loadmat('mnist_256_100sample.mat')
  # fullData = loadmat('../Data/cylinder_top.mat')
  scaler = preprocessing.MinMaxScaler()
  # x = csr_matrix(fullData.get('newsdata')).toarray()
  scaler.fit(np.array(fullData.get('g')))
  g = scaler.transform(np.array(fullData.get('g')))
  label = np.array(fullData.get('label')).transpose()
  label.astype(int)
  # np.random.seed(0)

  [AnchorPoint, AnchorLabel, Z] = AnchorPointGeneration(g, label, sparsity=0.1)
  initdata, initanchor, initc = funInit(label, AnchorLabel, dim=2)
  anchorpoint, anchor0, C = AnchorEmbedding(
      AnchorPoint, AnchorLabel, init=initanchor, flagMove=1, lamb=0.8, dim=2, cinit=initc, T=30)
  scaler.fit(anchorpoint)
  anchorpoint = scaler.transform(anchorpoint)

  # plt.scatter(anchorpoint[:, 0], anchorpoint[:, 1], c=AnchorLabel, cmap='rainbow')
  # plt.show()

  # fig = plt.figure()
  # ax = fig.add_subplot(projection='3d')
  # ax.scatter(anchorpoint[:, 0], anchorpoint[:, 1], anchorpoint[:, 2], c=AnchorLabel)
  # plt.show()

  W = kneighbors_graph(g, 10, mode='connectivity', include_self=False)

  for i in range(5):
    result = ANGEL_embedding(g, anchorpoint, Z, W, dim=2, T=1,
                             eps=0.1, init=initdata, optType='fast', neighbor=10)
    initdata = result
    plt.scatter(result[:, 0], result[:, 1], c=label, cmap='rainbow')
    plt.show()
  result = postProcessing(result, dim=2)

  # fig = plt.figure()
  # ax = fig.add_subplot(projection='3d')
  # ax.scatter(result[:, 0], result[:, 1], result[:, 2], c=label, cmap='rainbow')
  # plt.show()
  plt.scatter(result[:, 0], result[:, 1], c=label, cmap='rainbow')
  plt.show()

  # plt.scatter(result[:, 0], result[:, 1])
  # for length, vector in zip(pca.explained_variance_, pca.components_):
  #     v = vector * 3 * np.sqrt(length)
  #     draw_vector(pca.mean_, pca.mean_ + v)
  # plt.axis('equal')
  # plt.show()
  # result = pca.transform(result)

  plot_neighbor(g, result, label, k=10, part=0.5, choice='link')
  p, pl, pg, ps = Prev(g, result, label)
  print(p)
  print(pl)
  print(ps)

  print('finish')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

  # Generate Cellbt
  # fullData = loadmat('cellBT.mat')
  # scaler = preprocessing.MinMaxScaler()
  # # x = csr_matrix(fullData.get('newsdata')).toarray()
  # scaler.fit(np.array(fullData.get('g')))
  # g = scaler.transform(np.array(fullData.get('g')))
  # label = np.squeeze(np.array(fullData.get('label'))).transpose()
  # a = np.array([3, 4, 21, 20, 14, 1])
  # gtemp = np.zeros((55306, 38))
  # labeltemp = np.zeros((55306, 1))
  # temp = 0
  # for i in range(len(a)):
  #     t = np.squeeze(np.argwhere(label == a[i]))
  #     gtemp[temp: temp + len(t), :] = g[t, :]
  #     labeltemp[temp: temp + len(t), 0] = label[t]
  #     temp = temp + len(t)
  # g = np.array(gtemp)
  # label = np.array(labeltemp)
  # rnds = random.sample(range(0, 55306), 500)
  # g = g[rnds, :]
  # label = label[rnds]


# Read bicycle
  # g = []
  # with open('bicycle.pts') as file:
  #     for line in file:
  #         line = line.strip('\n')
  #         all_data = line.split()
  #         for ii in range(len(all_data)):
  #             all_data[ii] = float(all_data[ii])
  #         g.append(all_data)
  # g = np.asarray(g)
  #
  # label = []
  # with open('bicycle.seg') as file:
  #     for line in file:
  #         line = line.strip('\n')
  #         all_data = line.split()
  #         for ii in range(len(all_data)):
  #             all_data[ii] = float(all_data[ii])
  #         label.append(all_data)
  # label = np.asarray(label)
  #
  # rnds = random.sample(range(0, 2346), 500)
  # g = g[rnds, :]
  # label = label[rnds]
  #
  # fig = plt.figure()
  # ax = fig.add_subplot(projection='3d')
  # ax.scatter(g[:, 0], g[:, 1], g[:, 2], c=label)
  # plt.show()
  #
  # scaler = preprocessing.MinMaxScaler()
  # scaler.fit(g)
  # g = scaler.transform(g)


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

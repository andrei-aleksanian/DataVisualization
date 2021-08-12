# pylint: disable-all

import numpy as np
from scipy.io import loadmat
from scipy.spatial.distance import pdist, cdist, squareform
from scipy.optimize import minimize
# from sklearn.neighbors import NearestNeighbors
from sklearn import preprocessing
from sklearn.cluster import KMeans

# from FunctionFile import CohortDistance
from .SOEmbedding import SOE
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import directed_hausdorff
from pymanopt.manifolds import FixedRankEmbedded
from pymanopt import Problem
# from pymanopt.solvers import SteepestDescent
from pymanopt.solvers import ConjugateGradient
import matplotlib.pyplot as plt
from sklearn.manifold import MDS


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
    tempi = np.squeeze(np.argwhere(np.squeeze(
        DataLabel, axis=1) == u_Label[i]), axis=1)
    for j in range(l_label):
      if i == j:
        dCluster[i, j] = 0
      else:
        tempj = np.squeeze(np.argwhere(np.squeeze(
            DataLabel, axis=1) == u_Label[j]), axis=1)
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


def PrototypeEmbedding(Dc, DataLabel, Embedding='SOE'):
  linkage_order = np.argsort(Dc, axis=-1)
  if Embedding == 'SOE':
    V = SOE(linkage_order.astype(int), DataLabel)
  elif Embedding == 'MDS':
    embedding = MDS(n_components=2, dissimilarity='precomputed')
    V = embedding.fit_transform(Dc)
  return V


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


def ReScale(Data, NumMin, NumMax):
  X_std = (Data - Data.min()) / (Data.max() - Data.min())
  X_scaled = X_std * (NumMax - NumMin) + NumMin
  return X_scaled


def CohortConfidence(Data, DataCohort, lamb):
  [l, D] = Data.shape
  diffLabel = np.unique(DataCohort)
  num_label = len(diffLabel)
  W = np.zeros([l, num_label])
  Y = np.zeros([l, num_label])
  for i in range(num_label):
    tempData = Data[np.squeeze(DataCohort == diffLabel[i]), :]
    Y[np.squeeze(DataCohort == diffLabel[i]), i] = 1
    tempc = np.sum(tempData, axis=0) / tempData.shape[0]
    for j in range(num_label):
      tData = Data[np.squeeze(DataCohort == diffLabel[j]), :]
      tempw = cdist(np.expand_dims(
          tempc, axis=1).transpose(), tData, 'euclidean')
      mu = np.mean(tempw)
      sigma = np.cov(tempw)
      p = np.exp(-(tempw - mu) * (tempw - mu) / sigma)
      W[np.squeeze(DataCohort == diffLabel[j]), i] = p
  if lamb != 0:
    Rtemp = ReScale(W * Y, 1 - lamb, 1) * Y
    Rtemp2 = ReScale(W * (1 - Y), 0, lamb) * (1 - Y)
    R = Rtemp + Rtemp2
  else:
    R = Y * W
  # R = R / sum(sum(R))
  return R


def analyticalCOVA(R, Ad, V, alpha):
  Dr = np.diag(np.sum(R, axis=1))
  L3 = np.diag(np.sum(Ad, axis=0)) - Ad
  x = np.linalg.pinv(alpha * Dr + (1 - alpha) * L3) @ R @ V
  o1 = OjLocalDist(x, R, V)
  o3 = OjGlobalDist(x, Ad)
  o = alpha * o1 + (1 - alpha) * o3
  return o, x


def OjLocalDist(x, R, V, opttype='GD_Euclidean'):
  Dr = np.diag(np.sum(R, axis=1))
  Dc = np.diag(np.sum(R, axis=0))
  if opttype == 'GD_Riemannian':
    x = x[0] @ np.diag(x[1]) @ x[2]
  o = np.trace(x.transpose() @ Dr @ x) + np.trace(V.transpose()
                                                  @ Dc @ V) - 2 * np.trace(x.transpose() @ R @ V)
  return o


def OjGlobalDist(x, Ad, opttype='GD_Euclidean'):
  L3 = np.diag(np.sum(Ad, axis=0)) - Ad
  if opttype == 'GD_Riemannian':
    x = x[0] @ np.diag(x[1]) @ x[2]
  o = np.trace(x.transpose() @ L3 @ x)
  return o


def OjLocalSE(x, R, V, opttype='GD_Euclidean'):
  if opttype == 'GD_Riemannian':
    x = x[0] @ np.diag(x[1]) @ x[2]
  D = cdist(x, V, metric='euclidean')
  D = D * D
  T = 1 / (1 + D)
  if abs(sum(sum(R)) - 1) < 1e-10:
    T1 = T / sum(sum(T))
  elif abs(np.mean(np.sum(R, axis=0)) - 1) < 1e-10:
    T1 = T @ np.diag(1 / np.sum(T, axis=0))
  else:
    T1 = T @ np.diag(1 / np.sum(T, axis=0)) @ np.diag(np.sum(R, axis=0))
  y = -R * np.log(T1)
  o = sum(sum(y))
  return o


def OjGlobalSE(x, Ad, opttype='GD_Euclidean'):
  if opttype == 'GD_Riemannian':
    x = x[0] @ np.diag(x[1]) @ x[2]
  n = Ad.shape[0]
  P = Ad / sum(sum(Ad))
  d2 = squareform(pdist(x, 'euclidean'))
  d2 = d2 * d2
  Q = 1 / (1 + d2)
  Q[range(n), range(n)] = 0
  Q_n = Q / sum(Q)
  y = -P * np.log(Q_n)
  y[range(n), range(n)] = 0
  o = sum(sum(y))
  return o


def GradLocalDist(x, R, V, opttype='GD_Euclidean'):
  Dr = np.diag(np.sum(R, axis=1))
  if opttype == 'GD_Euclidean':
    gd = 2 * Dr @ x - 2 * R @ V
    return gd
  elif opttype == 'GD_Riemannian':
    x0 = x[0] @ np.diag(x[1]) @ x[2]
    S = np.diag(x[1])
    gdu = (2 * Dr @ x0 - 2 * R @ V) @ (S @ x[2]).T
    gds = np.diag(x[0].T @ (2 * Dr @ x0 - 2 * R @ V) @ x[2].T)
    gvt = (x[0] @ S).T @ (2 * Dr @ x0 - 2 * R @ V)
    return gdu, gds, gvt


def GradLocalSE(x, R, V, opttype='GD_Euclidean'):
  D = cdist(x, V, metric='euclidean')
  D = D * D
  T = 1 / (1 + D)
  if abs(sum(sum(R)) - 1) < 1e-10:
    T1 = T / sum(sum(T))
  elif abs(np.mean(np.sum(R, axis=0)) - 1) < 1e-10:
    T1 = T @ np.diag(1 / np.sum(T, axis=0))
  else:
    T1 = T @ np.diag(1 / np.sum(T, axis=0)) @ np.diag(np.sum(R, axis=0))
  L = 2 * (R - T1) * T
  gd = np.diag(np.sum(L, axis=1)) @ x - L @ V
  return gd


def GradGlobalDist(x, Ad, opttype='GD_Euclidean'):
  L3 = np.diag(np.sum(Ad, axis=0)) - Ad
  if opttype == 'GD_Euclidean':
    gd = 2 * L3 @ x
    return gd
  elif opttype == 'GD_Riemannian':
    x0 = x[0] @ np.diag(x[1]) @ x[2]
    S = np.diag(x[1])
    gdu = (2 * L3 @ x0) @ (S @ x[2]).T
    gds = np.diag(x[0].T @ (2 * L3 @ x0) @ x[2].T)
    gvt = (x[0] @ S).T @ (2 * L3 @ x0)
    return gdu, gds, gvt


def GradGlobalSE(x, Ad, opttype='GD_Euclidean'):
  n = Ad.shape[0]
  P = Ad / sum(sum(Ad))
  d2 = squareform(pdist(x, 'euclidean'))
  d2 = d2 * d2
  Q = 1 / (1 + d2)
  Q[range(n), range(n)] = 0
  Q_n = Q / sum(Q)
  L = (P - Q_n) * Q
  gd = 4 * (np.diag(np.sum(L, axis=0)) - L) @ x
  return gd


def reformX(x):
  n = int(x.shape[0] / 2)
  x0 = np.reshape(x, (n, 2))
  return x0


def cost1(x, R, Ad, V, alpha, COVAtype='cova1', opttype='GD_Euclidean'):
  if opttype == 'GD_Euclidean':
    x = reformX(x)
  if COVAtype == 'cova1':
    o1 = OjLocalDist(x, R, V, opttype)
    o3 = OjGlobalDist(x, Ad, opttype)
  elif COVAtype == 'cova2':
    o1 = OjLocalSE(x, R, V, opttype)
    o3 = OjGlobalSE(x, Ad)
  elif COVAtype == 'cova3':
    o1 = OjLocalDist(x, R, V, opttype)
    o3 = OjGlobalSE(x, Ad, opttype)
  elif COVAtype == 'cova4':
    o1 = OjLocalSE(x, R, V, opttype)
    o3 = OjGlobalDist(x, Ad, opttype)
  else:
    print('error')
    return 0
  o = alpha * o1 + (1 - alpha) * o3
  return o


def grad1(x, R, Ad, V, alpha, COVAtype='cova1', opttype='GD_Euclidean'):
  l = len(x)
  if opttype == 'GD_Euclidean':
    x = reformX(x)
  if COVAtype == 'cova1':
    g1 = GradLocalDist(x, R, V, opttype)
    g3 = GradGlobalDist(x, Ad, opttype)
  elif COVAtype == 'cova2':
    g1 = GradLocalSE(x, R, V, opttype)
    g3 = GradGlobalSE(x, Ad, opttype)
  elif COVAtype == 'cova3':
    g1 = GradLocalDist(x, R, V, opttype)
    g3 = GradGlobalSE(x, Ad, opttype)
  elif COVAtype == 'cova4':
    g1 = GradLocalSE(x, R, V, opttype)
    g3 = GradGlobalDist(x, Ad, opttype)
  else:
    print('error')
    return 0
  if opttype == 'GD_Euclidean':
    gd = alpha * g1 + (1 - alpha) * g3
    gd = np.squeeze(np.reshape(gd, (l, 1)))
  elif opttype == 'GD_Riemannian':
    g1 = list(g1)
    g3 = list(g3)
    g1[0] = alpha * g1[0] + (1 - alpha) * g3[0]
    g1[1] = alpha * g1[1] + (1 - alpha) * g3[1]
    g1[2] = alpha * g1[2] + (1 - alpha) * g3[2]
    gd = tuple(g1)
  else:
    print('error')
    return 0
  return gd


def COVAembedding(
        Data,
        R,
        Ad,
        V,
        Init=0,
        dim=2,
        alpha=0.5,
        COVAType='cova1',
        opttype='GD_Euclidean'):
  if COVAType == 'AnalyticalCOVA1':
    o, x = analyticalCOVA(R, Ad, V, alpha)
  else:
    if opttype == 'AnalyticalCOVA1':
      o, x = analyticalCOVA(R, Ad, V, alpha)
    elif opttype == 'GD_Euclidean':
      l = Data.shape[0]
      if Init == 0:
        Init = np.random.random_sample((l, dim))
      additional = (R, Ad, V, alpha, COVAType, opttype)
      x = minimize(cost1, Init, method='BFGS', args=additional, jac=grad1,
                   options={'disp': True, 'maxiter': 50})
      x = np.reshape(x.x, (l, dim))
    elif opttype == 'GD_Riemannian':
      l = Data.shape[0]
      manifold = FixedRankEmbedded(l, dim, dim)
      cost, egrad = CreateCostGrad(R, Ad, V, alpha, COVAType, opttype)
      prob = Problem(manifold, cost=cost, egrad=egrad)
      solver = ConjugateGradient()
      x0 = solver.solve(prob)
      x = x0[0] @ np.diag(x0[1]) @ x0[2]
    else:
      print('error')
      return 0
  return x


def CreateCostGrad(R, Ad, V, alpha, COVAType, opttype='GD_Riemannian'):
  def cost(x):
    return cost1(x, R, Ad, V, alpha, COVAType, opttype)

  def egrad(x):
    return grad1(x, R, Ad, V, alpha, COVAType, opttype)

  return cost, egrad


def cova():
  fullData = loadmat('./app/visualization/Data/OneFlower.mat')
  # scaler = preprocessing.MinMaxScaler()
  # x = csr_matrix(fullData.get('newsdata')).toarray()
  # scaler.fit(np.array(fullData.get('g')))
  # g = scaler.transform(np.array(fullData.get('g')))
  # label = np.array(fullData.get('label'))

  # My code for sampling
  SAMPLE_SIZE = 200
  g = np.array(fullData.get('g'))[:SAMPLE_SIZE, :]
  label = np.array(fullData.get('label'))[:SAMPLE_SIZE, :]
  # My code finished

  Dc = CohortDistance(g, label)
  V = PrototypeEmbedding(Dc, label, Embedding='MDS')
  # plt.scatter(V[:, 0], V[:, 1])
  # plt.show()

  Ad = AdjacencyMatrix(g, 10)
  temp_order = np.squeeze(np.argsort(label, axis=0))
  W1 = Ad[temp_order, :]
  W2 = W1[:, temp_order]

  Relation = CohortConfidence(g, label, 0)
  R_show = Relation[temp_order, :]

  # Cost, Result = analyticalCOVA(Relation, Ad, V, 0.9)
  result = COVAembedding(g, Relation, Ad, V, Init=0, dim=2,
                         alpha=0.1, COVAType='cova1', opttype='GD_Riemannian')

  return result, label


"""
Relation: 395 | range: 0to1 float  DISPLAY
alpha: 399 | range 0to1 float DISPLAY
Ad: 390 | range > 1 int DISPLAY
Embedding 386 | 3-4 choices
COVAType 400 | 5 choices
opttype 400 | 3 choices
sparcityOfAnchorPoints: 0 to 0.5 float
metric: a choice of metric from scipy.spatial.distance
cohortmetric: average, single, complete, Hausdoff, central
"""

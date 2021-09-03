# pylint: disable-all

import numpy as np
from scipy.io import loadmat
from scipy.spatial.distance import pdist, cdist, squareform
from scipy.optimize import minimize
# from sklearn.neighbors import NearestNeighbors
from sklearn import preprocessing

# from FunctionFile import AdjacencyMatrix
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import directed_hausdorff
from pymanopt.manifolds import FixedRankEmbedded
from pymanopt import Problem
# from pymanopt.solvers import SteepestDescent
from pymanopt.solvers import ConjugateGradient
import matplotlib.pyplot as plt
from sklearn.manifold import MDS
from .SOEmbedding import SOE
from .ANGEL import AnchorPointGeneration, AnchorEmbedding
from sklearn.cluster import KMeans
# import imagesc
from .evaluation import plot_neighbor


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
          dCluster[i, j] = directed_hausdorff(tempCluster_i, tempCluster_j)[0]
          dCluster[j, i] = dCluster[i, j]
        else:
          print('Wrong Information')
          break
  return dCluster


def PrototypeEmbedding(Dc, DataLabel, dim=2, Embedding='SOE'):
  linkage_order = np.argsort(Dc, axis=-1)
  if Embedding == 'SOE':
    V = SOE(linkage_order.astype(int), DataLabel, dim=dim)
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
      simgraph[i, dis_ascend[1: k + 1]] = abs(dis_sort[dis_ascend[1: k + 1]])
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


def OjGlobalDist(x, R, V, opttype='GD_Euclidean'):
  Dr = np.diag(np.sum(R, axis=1))
  Dc = np.diag(np.sum(R, axis=0))
  if opttype == 'GD_Riemannian':
    x = x[0] @ np.diag(x[1]) @ x[2]
  o = np.trace(x.transpose() @ Dr @ x) + np.trace(V.transpose()
                                                  @ Dc @ V) - 2 * np.trace(x.transpose() @ R @ V)
  return o


def OjLocalDist(x, Ad, opttype='GD_Euclidean'):
  L3 = np.diag(np.sum(Ad, axis=0)) - Ad
  if opttype == 'GD_Riemannian':
    x = x[0] @ np.diag(x[1]) @ x[2]
  o = np.trace(x.transpose() @ L3 @ x)
  return o


def OjGlobalSE(x, R, V, opttype='GD_Euclidean'):
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


def OjLocalSE(x, Ad, opttype='GD_Euclidean'):
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


def GradGlobalDist(x, R, V, opttype='GD_Euclidean'):
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


def GradGlobalSE(x, R, V, opttype='GD_Euclidean'):
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


def GradLocalDist(x, Ad, opttype='GD_Euclidean'):
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


def GradLocalSE(x, Ad, opttype='GD_Euclidean'):
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


def reformX(x, dim):
  n = int(x.shape[0] / dim)
  x0 = np.reshape(x, (n, dim))
  return x0


def cost1(x, R, Ad, V, alpha, dim, COVAtype='cova1', opttype='GD_Euclidean'):
  # alpha = 1 - alpha
  if opttype == 'GD_Euclidean':
    x = reformX(x, dim)
  if COVAtype == 'cova1':
    o1 = OjGlobalDist(x, R, V, opttype)
    o3 = OjLocalDist(x, Ad, opttype)
  elif COVAtype == 'cova2':
    o1 = OjGlobalSE(x, R, V, opttype)
    o3 = OjLocalSE(x, Ad)
  elif COVAtype == 'cova3':
    o1 = OjGlobalDist(x, R, V, opttype)
    o3 = OjLocalSE(x, Ad, opttype)
  elif COVAtype == 'cova4':
    o1 = OjGlobalSE(x, R, V, opttype)
    o3 = OjLocalDist(x, Ad, opttype)
  else:
    print('error')
    return 0
  o = alpha * o1 + (1 - alpha) * o3
  return o


def grad1(x, R, Ad, V, alpha, dim, COVAtype='cova1', opttype='GD_Euclidean'):
  # alpha = 1 - alpha
  l = len(x)
  if opttype == 'GD_Euclidean':
    x = reformX(x, dim)
  if COVAtype == 'cova1':
    g1 = GradGlobalDist(x, R, V, opttype)
    g3 = GradLocalDist(x, Ad, opttype)
  elif COVAtype == 'cova2':
    g1 = GradGlobalSE(x, R, V, opttype)
    g3 = GradLocalSE(x, Ad, opttype)
  elif COVAtype == 'cova3':
    g1 = GradGlobalDist(x, R, V, opttype)
    g3 = GradLocalSE(x, Ad, opttype)
  elif COVAtype == 'cova4':
    g1 = GradGlobalSE(x, R, V, opttype)
    g3 = GradLocalDist(x, Ad, opttype)
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
        T=5,
        COVAType='cova1',
        opttype='GD_Euclidean'):
  if COVAType == 'AnalyticalCOVA1':
    o, x = analyticalCOVA(R, Ad, V, alpha)
  else:
    if opttype == 'AnalyticalCOVA1':
      o, x = analyticalCOVA(R, Ad, V, alpha)
    elif opttype == 'GD_Euclidean':
      l = Data.shape[0]
      if isinstance(Init, int):
        Init = np.random.random_sample((l, dim))
      elif not isinstance(Init, int) and not isinstance(Init, np.ndarray):
        print('init error')
        return 0
      additional = (R, Ad, V, alpha, dim, COVAType, opttype)
      x = minimize(cost1, Init, method='BFGS', args=additional, jac=grad1,
                   options={'disp': True, 'maxiter': T})
      x = np.reshape(x.x, (l, dim))
    elif opttype == 'GD_Riemannian':
      l = Data.shape[0]
      manifold = FixedRankEmbedded(l, dim, dim)
      cost, egrad = CreateCostGrad(R, Ad, V, alpha, dim, COVAType, opttype)
      prob = Problem(manifold, cost=cost, egrad=egrad)
      solver = ConjugateGradient()
      x0 = solver.solve(prob)
      x = x0[0] @ np.diag(x0[1]) @ x0[2]
    else:
      print('error')
      return 0
  return x


def CreateCostGrad(R, Ad, V, alpha, dim, COVAType, opttype='GD_Riemannian'):
  def cost(x):
    return cost1(x, R, Ad, V, alpha, dim, COVAType, opttype)

  def egrad(x):
    return grad1(x, R, Ad, V, alpha, dim, COVAType, opttype)

  return cost, egrad


def SeparateCohort(data, label, sparsity=0.1):
  [l, D] = data.shape
  diffLabel = np.unique(label)
  num_label = len(diffLabel)
  prototype = np.empty([0, D])
  protolabel = np.empty([0, 1])
  clabel = np.zeros([l, 1])
  count = 0
  for i in range(num_label):
    num_point = len(np.where(label == diffLabel[i])[0])
    numOfAnchor_temp = np.floor(num_point * sparsity)
    if numOfAnchor_temp == 0:
      numOfAnchor_temp = 1
    while numOfAnchor_temp <= 3:
      numOfAnchor_temp = numOfAnchor_temp * 2
    numOfAnchor_temp = int(numOfAnchor_temp)
    gtemp = data[np.squeeze(label == diffLabel[i]), :]
    temp_Index = KMeans(n_clusters=numOfAnchor_temp, n_init=5).fit(gtemp)
    Anchortemp = temp_Index.cluster_centers_
    AnchorLabeltemp = diffLabel[i] * np.ones([numOfAnchor_temp, 1])
    prototype = np.concatenate((prototype, Anchortemp), axis=0)
    protolabel = np.concatenate((protolabel, AnchorLabeltemp), axis=0)
    clabel[np.squeeze(label == diffLabel[i]), 0] = temp_Index.labels_ + count
    count = count + numOfAnchor_temp

  return prototype, protolabel, clabel


def ProtoGeneration(data, label, dim=2, C=1, metric='euclidean', Embedding='SOE'):
  if C == 0:
    if len(label.shape) > 1:
      if label.shape[1] > 1:
        label = label.transpose()
    Dc = CohortDistance(data, label)
    V = PrototypeEmbedding(Dc, label, dim, Embedding)
    clabel = label
  elif C == 1:
    prototypes, protolabel, clabel = SeparateCohort(data, label, sparsity=0.1)
    A = squareform(pdist(prototypes, metric))
    A_order = np.argsort(A, axis=1).astype(int)
    V = SOE(A_order.astype(int), protolabel, dim=dim)
    scaler.fit(V)
    V = scaler.transform(V)
  else:
    print('Error')
    return 0
  return V, clabel


if __name__ == '__main__':
  fullData = loadmat('bicycle_sampe.mat')

  # fullData = loadmat('../Data/cylinder_top.mat')
  # x = csr_matrix(fullData.get('newsdata')).toarray()

  scaler = preprocessing.MinMaxScaler()
  scaler.fit(np.array(fullData.get('result')))
  g = scaler.transform(np.array(fullData.get('result')))
  label = np.array(fullData.get('label')).transpose()
  # fig = plt.figure()
  # ax = fig.add_subplot(projection='3d')
  # ax.scatter(g[:, 0], g[:, 1], g[:, 2], c=label)
  # plt.show()

  # prototypes, protolabel, clabel = SeparateCohort(g, label, sparsity=0.1)
  # A = squareform(pdist(prototypes, 'euclidean'))
  # A_order = np.argsort(A, axis=1).astype(int)
  # V = SOE(A_order.astype(int), protolabel, dim=3)
  # scaler.fit(V)
  # V = scaler.transform(V)
  # # Dc = CohortDistance(g, r_label)
  # V = PrototypeEmbedding(A_order, protolabel, dim=3, Embedding='SOE')

  # fig = plt.figure()
  # ax = fig.add_subplot(projection='3d')
  # ax.scatter(V[:, 1], V[:, 2], V[:, 0], c=protolabel)
  # plt.show()
  V, clabel = ProtoGeneration(
      g, label, dim=2, C=1, metric='euclidean', Embedding='SOE')
  Ad = AdjacencyMatrix(g, 10)
  # temp_order = np.squeeze(np.argsort(label, axis=0))
  # W_show = Ad[temp_order, :]
  # W_show = W_show[:, temp_order]
  # imagesc.plot(W_show, extent=[0, 1000, 0, 1000])

  # temp_order = np.squeeze(np.argsort(label, axis=0))

  Relation = CohortConfidence(g, clabel, 0)
  # R_show = Relation[temp_order,:]
  # imagesc.plot(R_show, extent=[0, 1000, 0, 1000])

  # Cost, Result = analyticalCOVA(Relation, Ad, V, 0.9)
  # init = 0
  # for i in range(50):
  #     Result = COVAembedding(g, Relation, Ad, V, Init=init, dim=3, alpha=0.5, T=1, COVAType='cova1', opttype='GD_Riemannian')
  # # x = Result
  # # plt.scatter(x[:, 0], x[:, 1])
  # # plt.show()
  #     fig = plt.figure()
  #     ax = fig.add_subplot(projection='3d')
  #     ax.scatter(Result[:, 0], Result[:, 1], Result[:, 2], c=label)
  #     plt.show()
  #     init = Result

  # init1 = Result
  Result = COVAembedding(g, Relation, Ad, V, Init=0, dim=2, alpha=0.4, T=100, COVAType='cova1',
                         opttype='GD_Euclidean')
  # fig = plt.figure()
  # ax = fig.add_subplot(projection='3d')
  # ax.scatter(Result[:, 0], Result[:, 1], Result[:, 2], c=label)
  # plt.show()

  # fig = plt.figure()
  # ax = fig.add_subplot(projection='2d')
  # plt.scatter(Result[:, 0], Result[:, 1], c=label)
  # plt.show()

  plot_neighbor(g, Result, label, k=10, part=0.6, choice='link')

  print(Ad)

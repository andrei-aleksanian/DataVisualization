# pylint: disable-all

import numpy as np
from sklearn.metrics import pairwise_distances


def AnchorGraph(Data, Anchor, t=3, cn=10, metric='euclidean'):
  """

  :param Data: input data matrix, D times n with D: dimension, n: number of samples
  :param Anchor: input anchor matrix, D times m with m: num of anchors
  :param t: number of closest anchors, default = 3
  :param cn: number of iterations for LAE, usually set to 5-20, default = 10
  :param metric: metric used to calculate distance
  :return: Z: n times m output anchor-to-data regression weight matrix
  """

  m = Anchor.shape[0]
  n = Data.shape[0]
  Z = np.zeros([n, m])
  val = np.zeros([n, t])
  pos = np.zeros([n, t])
  Dis = pairwise_distances(Data, Anchor, metric)
  for i in range(t):
    # val[:, i] = Dis.min(axis=1)
    pos[:, i] = Dis.argmin(axis=1)
    temppos = np.expand_dims(np.argmin(Dis, axis=1), axis=1)
    np.put_along_axis(Dis, temppos.astype(int), 1e60, axis=1)
  for i in range(n):
    x = np.expand_dims(Data[i, :], axis=0).transpose()
    U = Anchor[pos[i, :].astype(int), :].transpose()
    tempv = LAE(x, U, cn)
    # val[i, :] = np.squeeze(tempv, axis=1)
    Z[i, pos[i, :].astype(int)] = np.squeeze(tempv, axis=1)

  return Z


def LAE(Data, Anchor, cn):
  """
  main function of the LAE method
  :param Data: input data vector, D times 1 with D: dimensionality
  :param Anchor: input anchor vector, D times t with D: dimensionality, t: nearest anchor points
  :param cn: the number of iterations, 5-20
  :return: z: the s-dimensional coefficient vector
  """
  s = Anchor.shape[1]
  z0 = np.ones([s, 1]) / s
  z1 = z0.copy()
  delta = np.zeros([1, cn + 2])
  delta[:, 0] = 0
  delta[:, 1] = 1
  beta = np.zeros([1, cn + 1])
  beta[:, 0] = 1
  for t in range(cn):
    alpha = (delta[:, t] - 1) / delta[:, t + 1]
    v = z1 + alpha * (z1 - z0)

    dif = Data - np.dot(Anchor, v)
    gv = np.dot(dif.transpose(), dif) / 2
    gv = np.squeeze(gv, axis=0)
    dgv = np.dot(np.dot(Anchor.transpose(), Anchor), v) - \
        np.dot(Anchor.transpose(), Data)
    for j in range(100):
      b = pow(2, j) * beta[:, t]
      z = SimplexPr(v - dgv / b)
      dif = Data - np.dot(Anchor, z)
      gz = np.dot(dif.transpose(), dif) / 2
      gz = np.squeeze(gz, axis=0)
      dif = z - v
      gvz = gv + np.dot(dgv.transpose(), dif) + \
          np.dot(np.dot(b, dif.transpose()), dif) / 2
      if gz <= gvz:
        beta[:, t + 1] = b
        z0 = z1
        z1 = z
        break
    if beta[:, t + 1] == 0:
      beta[:, t + 1] = b
      z0 = z1
      z1 = z
    delta[:, t + 2] = (1 + np.sqrt(1 + 4 * pow(delta[:, t + 1], 2))) / 2

    if np.sum(np.absolute(z1 - z0)) <= 1e-4:
      break

    z = z1
  return z


def SimplexPr(X):
  """
  :param X: input data matrix, D times N with D: dimensionality, N:sample
  :return: S: the projected matrix of X onto C-dimensional simplex
  """
  [C, N] = X.shape
  T2 = np.argsort(X, axis=0)[:: -1]
  T1 = X[T2, :]
  T1 = np.squeeze(T1, axis=1)
  S = X.copy()

  for i in range(N):
    kk = 0
    t = T1[:, i]
    for j in range(C):
      tep = t[j] - (np.sum(t[0: j + 1]) - 1) / (j + 1)
      if tep <= 0:
        kk = j
        break

    if kk == 0:
      kk = C
    theta = (np.sum(t[0: kk]) - 1) / kk
    S[:, i] = np.maximum(X[:, i] - theta, 0)
  return S

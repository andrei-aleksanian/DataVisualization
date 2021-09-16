# pylint: disable-all

import numpy as np
from scipy.io import loadmat
from scipy.spatial.distance import pdist, squareform
from sklearn import preprocessing
from .FunctionFile import k_nearest_neighbor_disturb, k_nearest_neighbor, CohortDistance
from scipy import stats
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
import matplotlib as mplt
# import plotly as ply


def neighbor_prev_disturb(high_d, low_d, label, k, metric='euclidean', part=0.5):
  """
  Anchor point generation based on K-means method.
  Relationship matrix Z is obtained by LAE approach using t-nearest anchor points.

  :param high_d: input data matrix in the high-dimensional space
  :param low_d: input embedded data matrix in the low-dimensional space
  :param label: data label
  :param k: the neighbourhood size
  :param metric: default is 'euclidean'
  :param part: find data points with part% of wrongly preserved neighbors
  :return:
      prev_score: local preservation score
      neighbor_low: neighborhood of each data point in the low-dimensional space
      neighbor_high: neighborhood of each data point in the high-dimensional space
      prev_keep_high: successfully preserved neighbors index
      prev_wrong_in_high: index of neighbors find in the high-dimensional data but not in the low-d data
      prev_wrong_in_low: index of neighbors find in the low-dimensional data but not in the high-d data
      prev_partsave: Index of points who have bad neighbor preservation performance
  """
  if len(label.shape) > 1:
    label = np.squeeze(label)
  num = np.unique(label)
  n = len(num)
  l = high_d.shape[0]
  dis_high = np.zeros([l, l])
  dis_low = np.zeros([l, l])
  neighbor_high = np.zeros([l, l])
  neighbor_low = np.zeros([l, l])
  for i in range(n):
    temp_index = np.squeeze(np.argwhere(label == num[i]))
    temp_high_data = high_d[temp_index, :]
    temp_high = squareform(pdist(temp_high_data, metric=metric))
    temp_low_data = low_d[temp_index, :]
    temp_low = squareform(pdist(temp_low_data, metric=metric))
    temp_nei_high = k_nearest_neighbor(temp_high, k=k, weight=0, direction=1)
    temp_nei_low = k_nearest_neighbor_disturb(
        temp_low, k=k, weight=0, direction=1)
    dis_high[np.ix_(temp_index, temp_index)] = temp_high
    dis_low[np.ix_(temp_index, temp_index)] = temp_low
    neighbor_high[np.ix_(temp_index, temp_index)] = temp_nei_high
    neighbor_low[np.ix_(temp_index, temp_index)] = temp_nei_low
  total_samenei = 0
  prev_keep_high = np.zeros([l, k])
  prev_wrong_in_high = []
  prev_wrong_in_low = []
  prev_partsave = []
  for i in range(l):
    same_neigh = 0
    neih = neighbor_high[i, :]
    neil = neighbor_low[i, :]
    whereneighh = np.squeeze(np.where(neih == 1))
    whereneighl = np.squeeze(np.where(neil == 1))
    if k == 1:
      if whereneighh == whereneighl:
        same_neigh = same_neigh + 1
        prev_keep_high[i] = whereneighh
      else:
        prev_wrong_in_high.append(whereneighh)
        prev_wrong_in_low.append(whereneighl)
    else:
      if whereneighh.shape[0] < k:
        templh = whereneighh.shape[0]
        prev_keep_high[i, templh:] = 1e1000
      whereneighh_num = len(whereneighh)
      whereneighl_num = len(whereneighl)
      temp_marklow = np.zeros([whereneighl_num])
      for j in range(whereneighh_num):
        for a in range(whereneighl_num):
          if whereneighh[j] == whereneighl[a]:
            same_neigh = same_neigh + 1
            prev_keep_high[i, j] = whereneighh[j]
            temp_marklow[a] = whereneighl[a]
      temp_nomarkhigh = whereneighh[np.squeeze(
          np.argwhere(prev_keep_high[i, :] == 0))]
      temp_nomarklow = whereneighl[np.squeeze(np.argwhere(temp_marklow == 0))]
      prev_wrong_in_high.append(temp_nomarkhigh)
      prev_wrong_in_low.append(temp_nomarklow)
    if same_neigh < part * k:
      prev_partsave.append(i)
    total_samenei = total_samenei + same_neigh
  prev_score = total_samenei / (l * k)
  return prev_score, neighbor_low, neighbor_high, prev_keep_high, prev_wrong_in_high, prev_wrong_in_low, prev_partsave


def P_local(high_d, low_d, label, k, metric='euclidean'):
  if k < 10:
    k = 20
  save_prev = np.zeros([k, 1])
  sum_score = 0
  count = 0
  for i in range(k):
    if i == 0:
      continue
    else:
      count = count + 1
      prev_score = neighbor_prev_disturb(
          high_d, low_d, label, i, metric=metric)[0]
      sum_score = sum_score + prev_score
      save_prev[i] = prev_score
  prev_score = sum_score / count
  return prev_score, save_prev


def P_global(high_d, low_d, label, CohortMetric):
  k = np.unique(label)
  num_k = len(k)
  d_cohort1 = CohortDistance(
      high_d, label, linkC=CohortMetric, metricC='euclidean')
  d_cohort2 = CohortDistance(
      low_d, label, linkC=CohortMetric, metricC='euclidean')
  A1_o = np.argsort(d_cohort1, axis=1)
  A2_o = np.argsort(d_cohort2, axis=1)
  prev_score = stats.spearmanr(A1_o, A2_o, axis=None).correlation
  return prev_score


def Prev(high_d, low_d, label, specific='all', metric='euclidean', CohortMetric='average'):
  if specific == 'all':
    k = np.unique(label)
    num_label = len(k)
    smallest_label = float("inf")
    for i in range(num_label):
      temp = np.squeeze(np.argwhere(label == k[i])).shape[0]
      if temp < smallest_label:
        smallest_label = temp
    neigh = int(np.floor(0.5 * smallest_label))
    P_l = P_local(high_d, low_d, label, neigh, metric=metric)[0]

    P_g = P_global(high_d, low_d, label, CohortMetric)

    knn = KNeighborsClassifier(n_neighbors=1, weights='distance')
    cv_scores = cross_val_score(knn, low_d, np.ravel(label), cv=5)
    P_s = np.mean(cv_scores)

    P = (P_l + P_g + P_s) / 3
    return P, P_l, P_g, P_s
  elif specific == 'local':
    k = np.unique(label)
    num_label = len(k)
    smallest_label = float("inf")
    for i in range(num_label):
      temp = np.squeeze(np.argwhere(label == k[i])).shape[0]
      if temp < smallest_label:
        smallest_label = temp
    neigh = int(np.floor(0.5 * smallest_label))
    P_l = P_local(high_d, low_d, label, neigh, metric=metric)[0]
    return P_l
  elif specific == 'global':
    P_g = P_global(high_d, low_d, label, CohortMetric)
    return P_g
  elif specific == 'separability':
    knn = KNeighborsClassifier(n_neighbors=1, weights='distance')
    cv_scores = cross_val_score(knn, low_d, np.ravel(label), cv=5)
    P_s = np.mean(cv_scores)
    return P_s
  else:
    print('Error')
    return 0


def plot_neighbor(high_d, low_d, label, k=10, part=0.5, choice='link'):
  l = high_d.shape[0]
  dim = low_d.shape[1]
  Result_nei = neighbor_prev_disturb(
      high_d, low_d, label, k=k, metric='euclidean', part=part)
  neigh_low = Result_nei[1]
  neigh_high = Result_nei[2]
  prev_keep_high = Result_nei[3]
  prev_wrong_in_high = Result_nei[4]
  prev_wrong_in_low = Result_nei[5]
  prev_partsave = Result_nei[6]
  if part > 0:
    colorall = np.ones([l])
    temp_save = np.asarray(prev_partsave)
    # colorall[temp_save] = 2
    colorlabel = ['gray']
    if choice == 'link':
      if dim == 2:
        plt.scatter(low_d[:, 0], low_d[:, 1], c=colorall,
                    cmap=mplt.colors.ListedColormap(colorlabel))
      elif dim == 3:
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.scatter(low_d[:, 0], low_d[:, 1], low_d[:, 2],
                   c=colorall, cmap=mplt.colors.ListedColormap(colorlabel))
      else:
        print('error')
        return 0
      for i in range(len(prev_partsave)):
        templist = prev_wrong_in_low[prev_partsave[i]]
        temppoint = low_d[templist, :]
        colorall[templist] = 3
        for j in range(len(templist)):
          tempp = low_d[prev_partsave[i], :]
          tempj = temppoint[j, :]
          tempset = np.array([tempp, tempj])
          if dim == 2:
            plt.plot(tempset[:, 0], tempset[:, 1], 'r')
          elif dim == 3:
            plt.plot(tempset[:, 0], tempset[:, 1], tempset[:, 2], 'r')
          else:
            print('error')
            return 0
    elif choice == 'size':
      sizeall = np.ones([l]) * 10
      sizeall[temp_save] = 100
      if dim == 2:
        plt.scatter(low_d[:, 0], low_d[:, 1], s=sizeall,
                    c=colorall, cmap=mplt.colors.ListedColormap(colorlabel))
      elif dim == 3:
        plt.scatter(low_d[:, 0], low_d[:, 1], low_d[:, 2], s=sizeall,
                    c=colorall, cmap=mplt.colors.ListedColormap(colorlabel))
      else:
        print('error')
        return 0
  plt.show()
  return 0


if __name__ == '__main__':
  fullData = loadmat('../Data/cylinder_top.mat')
  scaler = preprocessing.MinMaxScaler()
  # x = csr_matrix(fullData.get('newsdata')).toarray()
  scaler.fit(np.array(fullData.get('x')))
  g = scaler.transform(np.array(fullData.get('x')))
  label = np.array(fullData.get('label')).transpose()
  Adis = squareform(pdist(g, metric='euclidean'))

  # fullresult = loadmat('../Result/flower/OneFlower_AnchorLOE_constrained_eps2.mat')
  fullresult = loadmat('angel_neigh300.mat')
  x = np.array(fullresult.get('result'))

  # a = Prev(g, x, label, specific='local')

  plot_neighbor(g, x, label, k=10, part=0.6, choice='link')

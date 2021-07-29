import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.optimize import minimize

from numba import jit


def SOE(Matrix, DataLabel, C=0, anchor=0, dim=2, Init=0, metric='euclidean', flagMove=0, T=500, eps=1e-6, scale=1):
    [l, D] = Matrix.shape
    if Init == 0:
        Init = np.random.random_sample((l, dim))
    if flagMove == 1:
        # l1 = -0.5 * np.pi * np.ones((C.shape[0], 1))
        # u1 = 0.5 * np.pi * np.ones((C.shape[0], 1))
        # l2 = np.zeros((C.shape[0], 1))
        # u2 = scale * np.ones((C.shape[0], 1))
        # b1 = np.concatenate((l1, l2), axis=0)
        # b2 = np.concatenate((u1, u2), axis=0)
        Init = np.random.random_sample((C.shape[0], dim))

        bnds1 = [(-0.5 * np.pi, 0.5 * np.pi) for i in range(0, C.shape[0])]
        bnds2 = [(0, scale) for i in range(0, C.shape[0])]
        bnds = bnds1 + bnds2

        additional = (Matrix, anchor, C, DataLabel)
        # init = np.reshape(Init, (2*C.shape[0], 1))
        # E = ErrSOE_Relocate(init, *additional)
        # grad = GradSOE_Relocate(init, *additional)

        x = minimize(ErrSOE_Relocate, Init, method='SLSQP', args=additional, jac=GradSOE_Relocate,
                     bounds=bnds, options={'disp': True, 'maxiter': 50})
        x = np.reshape(x.x, (C.shape[0], dim))
    elif D == l and flagMove == 0:
        x = minimize(ErrSOE, Init, method='BFGS', args=Matrix, jac=GradSOE,
                     options={'gtol': eps, 'disp': True, 'maxiter': T})
        x = np.reshape(x.x, (l, dim))
    elif D == 3 and flagMove == 0:
        x = minimize(ErrSOE_triplet, Init, method='BFGS', args=Matrix, jac=GradSOE_triplet,
                     options={'gtol': eps, 'disp': True, 'maxiter': T})
        x = np.reshape(x.x, (l, dim))
    else:
        print('Wrong matrix')
        return 0
    return x


def PreForRelocationOE(Param, anchor0, anchorC, label):
    Del = 0.01
    c = int(Param.shape[0] / 2)
    [n, p] = anchor0.shape
    x = np.zeros((n, p))
    delx = np.zeros((n, p))
    theta = Param[0: c]
    scal = Param[c: Param.shape[0]]
    diffLabel = np.unique(label)
    for i in range(diffLabel.shape[0]):
        templ = np.squeeze(label == diffLabel[i], axis=1)
        delx[templ, :] = anchor0[templ, :] - np.mean(anchor0[templ, :], axis=0)
        Theta = Rtheta(theta[i])
        Scal = Sscal(scal[i])
        x[templ, :] = (Theta @ Scal @ delx[templ, :].transpose()).transpose() + anchorC[i, :]
    disgraph = squareform(pdist(x, 'euclidean'))
    return n, x, delx, disgraph, theta, scal, diffLabel, Del


def Rtheta(theta):
    k = np.array([[np.cos(theta), - np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    if len(k.shape) > 2:
        k = np.squeeze(k, axis=2)
    return k


def gradRtheta(theta):
    k = np.array([[- np.sin(theta), -np.cos(theta)], [np.cos(theta), - np.sin(theta)]])
    if len(k.shape) > 2:
        k = np.squeeze(k, axis=2)
    return k


def Sscal(scal):
    return np.array([[scal, 0], [0, scal]], dtype=float)


def ErrSOE_Relocate(Param, *args):
    A_order, anchor0, anchorC, labels = args[0], args[1], args[2], args[3]
    n, x, delx, disgraph, theta, scal, diffLabel, Del = PreForRelocationOE(Param, anchor0, anchorC, labels)
    E = ErrSOE_Relocate_loop(n, Del, A_order, disgraph, labels)
    return E


@jit(nopython=True)
def ErrSOE_Relocate_loop(n, Del, A_order, disgraph, labels):
    E = 0
    for i in range(0, n):
        for j in range(1, n - 1):
            for k in range(j + 1, n):
                if labels[A_order[i, 0]] == labels[A_order[i, j]]:
                    if labels[A_order[i, 0]] == labels[A_order[i, k]]:
                        temp = disgraph[A_order[i, 0], A_order[i, j]] + Del - disgraph[A_order[i, 0], A_order[i, k]]
                        if temp > 0:
                            E = E + temp * temp
    return E


def GradSOE_Relocate(Param, *args):
    A_order, anchor0, anchorC, labels = args[0], args[1], args[2], args[3]
    n, x, delx, disgraph, theta, scal, diffLabel, Del = PreForRelocationOE(Param, anchor0, anchorC, labels)
    gradX = GradSOE_Relocate_loop(delx, n, Del, A_order, disgraph, theta, scal, anchorC, diffLabel, labels)
    gradX0 = np.squeeze(np.reshape(gradX, (Param.shape[0], 1)))
    return gradX0


def RS(theta, scal):
    if len(Rtheta(theta).shape) > 2:
        R = np.squeeze(Rtheta(theta), axis=2)
    else:
        R = Rtheta(theta)
    return R @ Sscal(scal)


def gradRS(theta, scal):
    if len(gradRtheta(theta).shape) > 2:
        R = np.squeeze(gradRtheta(theta), axis=2)
    else:
        R = gradRtheta(theta)
    return R @ Sscal(scal)


def GradSOE_Relocate_loop(delx, n, Del, A_order, disgraph, theta, scal, C, diffLabel, labels):
    gradT = np.zeros((theta.shape[0], 2))
    for i in range(0, n):
        for j in range(1, n - 1):
            for k in range(j + 1, n):
                if labels[A_order[i, 0]] == labels[A_order[i, j]] and labels[A_order[i, 0]] == labels[A_order[i, k]]:
                    if disgraph[A_order[i, 0], A_order[i, j]] + Del - disgraph[A_order[i, 0], A_order[i, k]] > 0:
                        temp = 1e-5
                        if disgraph[A_order[i, 0], A_order[i, j]] < temp:
                            d_ij = temp
                        else:
                            d_ij = disgraph[A_order[i, 0], A_order[i, j]]
                        if disgraph[A_order[i, 0], A_order[i, k]] < temp:
                            d_ik = temp
                        else:
                            d_ik = disgraph[A_order[i, 0], A_order[i, k]]

                        if len((diffLabel == labels[A_order[i, 0]]).shape) > 1:
                            li = np.squeeze(diffLabel == labels[A_order[i, 0]], axis=1)
                            lj = np.squeeze(diffLabel == labels[A_order[i, j]], axis=1)
                            lk = np.squeeze(diffLabel == labels[A_order[i, k]], axis=1)
                        else:
                            li = diffLabel == labels[A_order[i, 0]]
                            lj = diffLabel == labels[A_order[i, j]]
                            lk = diffLabel == labels[A_order[i, k]]

                        if len(theta[li]) > 1:
                            theta_li = np.squeeze(theta[li], axis=1)
                            theta_lj = np.squeeze(theta[lj], axis=1)
                            theta_lk = np.squeeze(theta[lk], axis=1)
                            scal_li = np.squeeze(scal[li], axis=1)
                            scal_lj = np.squeeze(scal[lj], axis=1)
                            scal_lk = np.squeeze(scal[lk], axis=1)
                        else:
                            theta_li = theta[li]
                            theta_lj = theta[lj]
                            theta_lk = theta[lk]
                            scal_li = scal[li]
                            scal_lj = scal[lj]
                            scal_lk = scal[lk]

                        x_i = (RS(theta_li, scal_li) @ delx[A_order[i, 0], :].transpose()).transpose() + C[li, :]
                        x_j = (RS(theta_lj, scal_lj) @ delx[A_order[i, j], :].transpose()).transpose() + C[lj, :]
                        x_k = (RS(theta_lk, scal_lk) @ delx[A_order[i, k], :].transpose()).transpose() + C[lk, :]

                        gradXi = 2 * (disgraph[A_order[i, 0], A_order[i, j]] - disgraph[
                            A_order[i, 0], A_order[i, k]] + Del) * ((x_i - x_j) / d_ij - (x_i - x_k) / d_ik)
                        gradXj = - 2 * (disgraph[A_order[i, 0], A_order[i, j]] - disgraph[
                            A_order[i, 0], A_order[i, k]] + Del) * ((x_i - x_j) / d_ij)
                        gradXk = 2 * (disgraph[A_order[i, 0], A_order[i, j]] - disgraph[
                            A_order[i, 0], A_order[i, k]] + Del) * ((x_i - x_k) / d_ik)

                        gradT[li, 0] = gradT[li, 0] + gradXi @ gradRS(theta_li, scal_li) @ delx[A_order[i, 0],
                                                                                           :].transpose()
                        gradT[lj, 0] = gradT[lj, 0] + gradXj @ gradRS(theta_li, scal_lj) @ delx[A_order[i, j],
                                                                                           :].transpose()
                        gradT[lk, 0] = gradT[lk, 0] + gradXk @ gradRS(theta_lk, scal_lk) @ delx[A_order[i, k],
                                                                                           :].transpose()

                        gradT[li, 1] = gradT[li, 1] + gradXi @ Rtheta(theta_li) @ delx[A_order[i, 0],
                                                                                  :].transpose()
                        gradT[lj, 1] = gradT[lj, 1] + gradXj @ Rtheta(theta_lj) @ delx[A_order[i, j],
                                                                                  :].transpose()
                        gradT[lk, 1] = gradT[lk, 1] + gradXk @ Rtheta(theta_lk) @ delx[A_order[i, k],
                                                                                  :].transpose()
    return gradT


def disForOE(x):
    n = int(x.shape[0] / 2)
    x0 = np.reshape(x, (n, 2))
    Del = 0.01
    disgraph = squareform(pdist(x0, 'euclidean'))
    return n, x0, Del, disgraph


def ErrSOE(x, A_order):
    n, x0, Del, disgraph = disForOE(x)
    E = ErrSOE_loop(n, Del, A_order, disgraph)
    return E


@jit(nopython=True)
def ErrSOE_loop(n, Del, A_order, disgraph):
    E = 0
    for i in range(0, n):
        for j in range(1, n - 1):
            for k in range(j + 1, n):
                temp = disgraph[A_order[i, 0], A_order[i, j]] + Del - disgraph[A_order[i, 0], A_order[i, k]]
                if temp > 0:
                    E = E + temp * temp
    return E


def GradSOE(x, A_order):
    n, x0, Del, disgraph = disForOE(x)
    gradX = GradSOE_loop(x0, n, Del, A_order, disgraph)
    gradX0 = np.squeeze(np.reshape(gradX, (x.shape[0], 1)))
    return gradX0


@jit(nopython=True)
def GradSOE_loop(x0, n, Del, A_order, disgraph):
    gradX = np.zeros((n, 2))
    for i in range(0, n):
        for j in range(1, n - 1):
            for k in range(j + 1, n):
                if disgraph[A_order[i, 0], A_order[i, j]] + Del - disgraph[A_order[i, 0], A_order[i, k]] > 0:
                    temp = 1e-5
                    if disgraph[A_order[i, 0], A_order[i, j]] < temp:
                        d_ij = temp
                    else:
                        d_ij = disgraph[A_order[i, 0], A_order[i, j]]
                    if disgraph[A_order[i, 0], A_order[i, k]] < temp:
                        d_ik = temp
                    else:
                        d_ik = disgraph[A_order[i, 0], A_order[i, k]]
                    x_i = x0[A_order[i, 0], :]
                    x_j = x0[A_order[i, j], :]
                    x_k = x0[A_order[i, k], :]
                    gradX[A_order[i, 0], :] = gradX[A_order[i, 0], :] + 2 * (
                            disgraph[A_order[i, 0], A_order[i, j]] -
                            disgraph[A_order[i, 0], A_order[i, k]] + Del) * ((x_i - x_j) / d_ij - (x_i - x_k) / d_ik)
                    gradX[A_order[i, j], :] = gradX[A_order[i, j], :] - 2 * (
                            disgraph[A_order[i, 0], A_order[i, j]] -
                            disgraph[A_order[i, 0], A_order[i, k]] + Del) * ((x_i - x_j) / d_ij)
                    gradX[A_order[i, k], :] = gradX[A_order[i, k], :] + 2 * (
                            disgraph[A_order[i, 0], A_order[i, j]] -
                            disgraph[A_order[i, 0], A_order[i, k]] + Del) * ((x_i - x_k) / d_ik)
    return gradX


def ErrSOE_triplet(x, A_order):
    n, x0, Del, disgraph = disForOE(x)
    E = ErrSOE_triplet_loop(n, Del, A_order, disgraph)
    return E


@jit(nopython=True)
def ErrSOE_triplet_loop(n, Del, A_order, disgraph):
    E = 0
    for i in range(0, n):
        temp_order = A_order[i, :]
        temp = disgraph[temp_order[i, 0], temp_order[i, 1]] + Del - disgraph[temp_order[i, 0], temp_order[i, 2]]
        if temp > 0:
            E = E + temp * temp
    return E


def GradSOE_triplet(x, A_order):
    n, x0, Del, disgraph = disForOE(x)
    gradX = GradSOE_triplet_loop(x0, n, Del, A_order, disgraph)
    gradX0 = np.squeeze(np.reshape(gradX, (x.shape[0], 1)))
    return gradX0


@jit(nopython=True)
def GradSOE_triplet_loop(x0, n, Del, A_order, disgraph):
    gradX = np.zeros((n, 2))
    for i in range(0, n):
        temp_order = A_order[i, :]
        if disgraph[temp_order[i, 0], temp_order[i, 1]] + Del - disgraph[temp_order[i, 0], temp_order[i, 2]] > 0:
            temp = 1e-5
            if disgraph[temp_order[i, 0], temp_order[i, 1]] < temp:
                d_ij = temp
            else:
                d_ij = disgraph[temp_order[i, 0], temp_order[i, 1]]
            if disgraph[temp_order[i, 0], temp_order[i, 2]] < temp:
                d_ik = temp
            else:
                d_ik = disgraph[temp_order[i, 0], temp_order[i, 2]]
            x_i = x0[temp_order[i, 0], :]
            x_j = x0[temp_order[i, 1], :]
            x_k = x0[temp_order[i, 2], :]
            gradX[temp_order[i, 0], :] = gradX[temp_order[i, 0], :] + 2 * (
                    disgraph[temp_order[i, 0], temp_order[i, 1]] -
                    disgraph[temp_order[i, 0], temp_order[i, 2]] + Del) * ((x_i - x_j) / d_ij - (x_i - x_k) / d_ik)
            gradX[temp_order[i, 1], :] = gradX[temp_order[i, 1], :] - 2 * (
                    disgraph[temp_order[i, 0], temp_order[i, 1]] -
                    disgraph[temp_order[i, 0], temp_order[i, 2]] + Del) * ((x_i - x_j) / d_ij)
            gradX[temp_order[i, 2], :] = gradX[temp_order[i, 2], :] + 2 * (
                    disgraph[temp_order[i, 0], temp_order[i, 1]] -
                    disgraph[temp_order[i, 0], temp_order[i, 2]] + Del) * ((x_i - x_k) / d_ik)
    return gradX



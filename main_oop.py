import numpy as np
from math import inf


def get_min_idx(list_):
    return np.argmin(list_)


def simplex_end_condition(target_param_):
    for z in target_param_:
        if z < 0:
            return False
    return True


def simplex_solve(c_, a_, b_):
    c = c_
    b = b_
    constrain_matrix = a_
    constrain_num = constrain_matrix.shape[0]

    A = np.append(constrain_matrix, np.eye(constrain_num), axis=1)
    A = np.append(A, b, axis=1)
    print(A)

    # ------------------------------------------------------------

    obj_coeffs = np.zeros(A.shape[1] - 1)
    obj_coeffs[:c.shape[0]] = c
    print("obj_coeffs:", obj_coeffs)

    basic_variables = np.array(range(c.shape[0], A.shape[1] - 1))
    print("basic_variables:", basic_variables)

    cB = np.array([obj_coeffs[i] for i in basic_variables]).reshape(1, -1)
    print("cB:", cB)
    obj_discs = obj_coeffs - np.dot(cB, A[:, :A.shape[1] - 1])
    print("obj_discs:", obj_discs)

    while True:
        print("#" * 100)
        if simplex_end_condition(obj_discs[0]):
            break

        enter_idx = get_min_idx(obj_discs[0][:obj_discs[0].shape[0] - 1])

        ans = np.zeros(A.shape[0])
        for i in range(0, A.shape[0]):
            if A[i][enter_idx] > 0:
                ans[i] = A[i][A.shape[1] - 1] / A[i][enter_idx]
            else:
                ans[i] = inf
        ans_min_idx = get_min_idx(ans)
        leave_idx = basic_variables[ans_min_idx]

        A[ans_min_idx] = A[ans_min_idx] / A[ans_min_idx][enter_idx]
        for i in range(0, A.shape[0]):
            if i == ans_min_idx:
                continue
            A[i] = A[i][:] - A[i][enter_idx] * A[ans_min_idx]
        print(A)

        basic_variables[ans_min_idx] = enter_idx
        print("basic_variables:", basic_variables)

        cB = np.array([obj_coeffs[y] for y in basic_variables]).reshape(1, -1)
        print("cB:", cB)

        obj_discs[0] = obj_discs[0] - np.dot(cB, A[:, :A.shape[1] - 1])
        print("obj_discs:", obj_discs[0])

        goal_value = cB @ A[:, A.shape[1] - 1]
        print("goal_value:", goal_value)


if __name__ == '__main__':
    # ------------------------------------------------------------

    c_in = np.array([-2, 4, -1, 1])
    a_in = np.array([[1, 2, 4, 1],
                     [-1, 1, 0, 0],
                     [1, 0, 0, 0],
                     [0, 0, 1, -5],
                     [0, 0, -1, 2]])
    b_in = np.array([[20], [3], [4], [5], [2]])
    simplex_solve(c_in, a_in, b_in)

    # ------------------------------------------------------------

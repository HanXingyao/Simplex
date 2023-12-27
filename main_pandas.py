import numpy as np
import pandas as pd
from math import inf


def simplex_end_condition(target_param_):
    for z in target_param_:
        if z > 0:
            return False
    return True


def simplex_solve(c_, a_, b_):
    c, b, a = c_, b_, a_
    constrain_num = a.shape[0]
    A = np.append(a, np.eye(constrain_num), axis=1)
    variable_num = A.shape[1]

    tableau = np.zeros((A.shape[0] + 2, A.shape[1] + 2))
    tableau[0, :c.shape[0]] = c
    tableau[1: -1, :-2] = A
    tableau[1: -1, -2] = b.reshape(-1)
    column_names = ["x" + str(i) for i in range(1, variable_num + 1)] + ["b", "ratios"]
    index_names = (["coeffs"]
                   + ["x" + str(i) for i in range(variable_num - a.shape[1], variable_num + 1)]
                   + ["discs"])
    tableau = pd.DataFrame(tableau, columns=column_names, index=index_names)
    tableau.loc["discs"] = tableau.loc["coeffs"]
    print(tableau)

    # ------------------------------------------------------------

    while True:
        print("#" * 100)
        # 选择入基变量
        enter_idx = np.argmax(tableau.loc["discs"].tolist()[: -2])
        enter_variable = tableau.columns.values.tolist()[enter_idx]

        # 计算各个约束的比值
        for i in range(1, tableau.shape[0] - 1):
            if tableau.iloc[i, enter_idx] > 0:
                tableau.iloc[i, variable_num + 1] = tableau.iloc[i, variable_num] / tableau.iloc[i, enter_idx]
            else:
                tableau.iloc[i, variable_num + 1] = inf
        print(tableau)

        # 选择离基变量
        ratio_min_idx = np.argmin(tableau.iloc[1: -1, variable_num + 1].tolist())
        ratio_min_idx += 1
        leave_variable = tableau.index.values.tolist()[ratio_min_idx]

        print(leave_variable, " --> ", enter_variable)

        # 更新单纯形表格
        new_index = {leave_variable: enter_variable}
        tableau = tableau.rename(index=new_index)
        tableau.iloc[ratio_min_idx, :-1] = tableau.iloc[ratio_min_idx, :-1] / tableau.iloc[ratio_min_idx, enter_idx]
        for i in range(1, tableau.shape[0]):
            if i == ratio_min_idx:
                continue
            tableau.iloc[i, :-1] = (tableau.iloc[i, :-1] -
                                    tableau.iloc[i, enter_idx] * tableau.iloc[ratio_min_idx, :-1])
        print(tableau)
        if simplex_end_condition(tableau.loc["discs"].tolist()[: -2]):
            break


if __name__ == '__main__':
    # ------------------------------------------------------------

    c_in = np.array([2, -4, 1, -1])
    a_in = np.array([[1, 2, 4, 1],
                     [-1, 1, 0, 0],
                     [1, 0, 0, 0],
                     [0, 0, 1, -5],
                     [0, 0, -1, 2]])
    b_in = np.array([[20], [3], [4], [5], [2]])
    simplex_solve(c_in, a_in, b_in)

    # ------------------------------------------------------------

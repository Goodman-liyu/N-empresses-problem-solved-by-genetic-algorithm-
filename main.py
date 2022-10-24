import numpy as np
import random
import sys

n = int(input("请输入皇后规模"))
m = int(input("请输入种群规模"))  # 种群规模越大越快
x = np.zeros((m, n), dtype=int)


# x为二维数组，x[m]代表了第m条数据的皇后排列信息，x[i][1]的值代表第i条数据的第一列皇后放在第x[i][1]行

def f_Cost(pm, pn, data):  # 评价函数，当当前皇后的位置与其他皇后冲突越多时，其cost值越大，当cost等于0时，直接输出，退出。list中存放cost的倒数
    list = []
    for i in range(pm):
        cost = 0
        for j in range(pn):
            for k in range(j + 1, pn):
                if (abs(j - k) == abs(data[i][j] - data[i][k])) or (data[i][j] == data[i][k]):
                    cost += 1
        if cost == 0:
            list.append(100)
            print(data[i])
            sys.exit()
        else:
            list.append(1 / cost)
    return list


def dealdata(p_list):  # 将每条数据的cost倒数值（存放在list中）计算其比例，并且计算累计百分比
    total_data = 0
    for count in p_list:
        total_data += count
    for i in range(len(p_list)):
        p_list[i] = p_list[i] / total_data
    for j in range(len(p_list) - 1, 0, -1):  # 注意倒叙的写法
        t = 0
        for i in range(j, -1, -1):
            t += p_list[i]
        p_list[j] = t
    return


def exchange(data, which1, which2, where):  # 交叉的具体实现，将选中的两条数据的两部分进行交换
    temp1 = data[which1][where:].copy()
    temp2 = data[which2][where:].copy()  # 深拷贝。。。巨坑，要是没有copy（）的话，修改data[witch1]的时候temp1就也跟着变，导致data[witch2]结果出错
    for i in range(len(temp1)):
        data[which1][where + i] = temp2[i]
    for j in range(len(temp2)):
        data[which2][where + j] = temp1[j]
    return


def change(pm, pn, data, costlist, a):  # 交叉操作 ，a是本身固定的交换概率
    for i in range(int(pm / 2)):
        index1 = 0
        index2 = 0
        afa = random.random() - 0.000000002  # 减去一个小数是因为，在实际计算累计百分比时，因为舍入的原因，会使最大累加百分比不是1（十分趋近1），所以在此选择减去一个小数
        while costlist[index1] < afa:
            index1 += 1
        afa = random.random() - 0.000000002
        while costlist[index2] < afa:
            index2 += 1
        A = random.random()
        if A < a: pass  # 只有当随机生成的交换因子A>=a时，才执行交换
        set = random.randint(0, pn) # 随机生成set，交换的其实位置
        exchange(data, index1, index2, set)


for i in range(m):  # 随机生成初始数据，注意同一组数据不能有重复的
    tabu_list = []
    for j in range(n):
        temp = random.randint(1, n)
        while temp in tabu_list:
            temp = random.randint(1, n)
        x[i][j] = temp
        tabu_list.append(temp)

while True:  # 当输入的皇后值本身有解，一定可以找到解
    cost_list = f_Cost(m, n, x)
    dealdata(cost_list)
    change(m, n, x, cost_list, 0.6)

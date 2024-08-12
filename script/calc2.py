def func(arg: str, arg2=2):
    """
    计算技能值
    :param arg: 技能值
    :param arg2: 后续几位
    :return: 新技能值，公差，最长小数位
    """

    ls = [float(i) for i in arg.split()]  # str转float
    diff = ls[1] - ls[0]  # 算公差
    for i in range(arg2):
        ls.append(ls[-1] + diff)  # 算后几位并加入列表

    # 算出小数位
    ls2 = []
    for i in ls:
        n = str(i).split('.')[1]
        if n == '0':
            ls2.append(0)  # 若为0则不算小数
        else:
            ls2.append(len(n))

    poi = max(ls2)  # 最长小数位
    ls3 = ' '.join([f'{i:.{poi}f}' for i in ls])  # list转成str

    return ls3, f'{diff:.{poi}f}', poi


if __name__ == '__main__':
    res = func("1.75 2.5 3.25 4", 2)
    print(res)

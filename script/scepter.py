def func(arg, arg2=0):
    """
    计算A杖值
    :param arg: 技能最大值
    :param arg2: 魔晶加成
    :return: A杖值，注释值
    """
    ls = [10 ** i for i in range(10)]
    # print(ls)

    for i in ls:
        if arg > i:
            continue
        return i - arg2, i


if __name__ == '__main__':
    scepter, note = func(1500, 400)
    print(f'scepter: {scepter}')
    print(f'note: {note}')

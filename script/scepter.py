def func(arg, arg2=0):
    """
    :param arg: 技能最大值
    :param arg2: 魔晶加成
    :return: A杖值，注释值
    """
    ls = [1, 10, 100, 1000, 10000]

    for i in ls:
        if arg > i:
            continue
        return i - arg2, i


if __name__ == '__main__':
    scepter, note = func(700, 400)
    print(f'scepter: {scepter}')
    print(f'note: {note}')

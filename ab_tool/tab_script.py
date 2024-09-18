def func1(tx: str) -> str:
    """退tab"""
    ls = tx.split('\t')
    if ls[0] == '':
        ls.pop(0)
    tx2 = '\t'.join(ls)
    return tx2


def func2(tx: str) -> str:
    """进tab"""
    ls = tx.split('\t')
    ls.insert(0, '')
    tx2 = '\t'.join(ls)
    return tx2


def tab_func(tx: str, x) -> str:
    """
    :param tx: 需要做tab处理的文本
    :param x: +是进一格tab，-是退一个tab
    :return: 处理完成的文本
    """
    ls = tx.split('\n')
    ls2 = []
    for i in ls:
        match x:
            case '-':
                i2 = func1(i)
            case '+':
                i2 = func2(i)
            case _:
                i2 = i
        ls2.append(i2)

    tx2 = '\n'.join(ls2)
    return tx2


if __name__ == '__main__':
    ex = '''\t\tab
\t\t{
\t\t\t"v"\t\t\t\t"1 2 3"
\t\t\t"sa"\t\t\t\t"+1"
\t\t\t"sp"\t\t\t\t"+2"
\t\t}
'''
    res1 = tab_func(ex, '-')
    res2 = tab_func(ex, '+')
    print(ex)
    print(res1)
    print(res2)

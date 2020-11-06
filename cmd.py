import os


def os_popen(stmt, *parm):
    re = os.popen(stmt).readlines()
    result = []
    for i in range(0, len(re) - 1):  # 由于原始结果需要转换编码，所以循环转为utf8编码并且去除\n换行
        res = re[i].strip('\n')
        result.append(res)
    if parm == ():
        return result  # 获取全部执行结果
    else:
        line = int(parm[0]) - 1
        return result[line]  # 获取执行结果的指定行


def kuandai():
    os_popen('rasdial kuandai /disconnect')
    flag = False
    while not flag:
        res = os_popen('rasdial kuandai 02209999150@liantong 123456')[3]
        print(res)
        if res == '已连接 kuandai。':
            flag = True


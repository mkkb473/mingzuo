from random import choices, random, seed
from time import time
import numpy as np
# 设定随机种子


# 是否为五星
star = [0, 5] 
# 抽中五星与否的概率
w = [0.994, 0.006]
# 歪五星概率
half = 0.5
# 大保底
dabaodi = 180

def run_experiment(sample_size, mingzuo):
    '''
    sample_size: 模拟实验的次数
    mingzuo:     命座

    '''
    seed(time())
    # 所有模拟样本中集满制定命座所需要的抽卡数集合
    result = []
    # 抽人物=命座+1
    same_draw = mingzuo + 1
    for i in range(sample_size):
        s = 0
        count = 0
        draws = 0
        must = False
        while s < same_draw:
            card = choices(star, w)
            count += 1
            draws += 1
            if (count % 90 == 0 and count > 0) or card[0] == 5:
                a = True if random() > half else False
                count = 0
                if a or must:
                    must = False
                    s += 1
                else:
                    must = True
        result.append(draws)
    return result

# 这里至少要保证实验次数是20的倍数
def show_sample_probability(result, mingzuo):
    same_draw = mingzuo + 1
    arr = np.array(result)
    # 排序以方便列出分段概率
    arr = np.sort(arr)
    part = []
    print('实验次数（0抽直至{}命）:'.format(mingzuo), len(result))
    print('命座数:', same_draw-1)
    for i in range(19):
        num_draws = arr[(i+1)*int(len(result) / 20)-1]
        part.append(num_draws)
        print("抽{}次的人至少占{}%".format(num_draws, (i+1)*5))
    return arr

def plot_image(sorted_result, mingzuo):
    same_draw = mingzuo + 1
    from matplotlib import pyplot as plt
    from matplotlib.ticker import PercentFormatter
    fig, ax = plt.subplots()
    ax.hist(sorted_result, bins = [n for n in range(0, same_draw * dabaodi, 10)])
    plt.gca().yaxis.set_major_formatter(PercentFormatter(len(result)))
    plt.xlabel('draw count')
    plt.ylabel('distribution')
    plt.show()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    sample_size = 10000
    mingzuo = 6
    parser.add_argument("--sample", help="实验次数", default=10000)
    parser.add_argument("--mingzuo", help="命座数, 0到6", default=6)
    args = parser.parse_args()
    if args.sample:
        sample_size = int(args.sample)
    if args.mingzuo:
        mingzuo = int(args.mingzuo)
    result = run_experiment(sample_size, mingzuo)
    sorted_result = show_sample_probability(result, mingzuo)
    plot_image(sorted_result, mingzuo)


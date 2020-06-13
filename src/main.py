import sys
from math import sqrt, floor, ceil
from pathlib import Path
from typing import List, Tuple

import numpy as np
import matplotlib.pyplot as plt
import scipy as scipy
from scipy.stats import kurtosis


def read_file(file_name) -> Tuple[int, List[float]]:
    lines = []
    len = 0
    with open(file_name) as file:
        for line in file:
            lines.append(float(line.strip()))
            len += 1
    return len, lines


def empiric_average(marks_sum, observations_num):
    return marks_sum / observations_num


def standard_deviation(empiric_avg, marks_list, observations_num) -> float:
    sd = 0.0
    for mark in marks_list:
        sd += pow(mark - empiric_avg, 2)
    return sqrt(sd / observations_num)


def moments(empiric_avg, marks_list, observations_num, sd, power) -> float:
    fourth_central_moment = 0.0
    for mark in marks_list:
        fourth_central_moment += pow(mark - empiric_avg, power)
    return (fourth_central_moment / observations_num) / pow(sd, power)


def percentile(marks_list, observations_num, percentile):
    tmp = ceil(observations_num * (percentile / 100))
    sorted_marks_list = sorted(marks_list)
    return sorted_marks_list[tmp]


def histogram(data):
    n, bins, patches = plt.hist(x=data, bins='auto', color='#0504aa', alpha=0.7, rwidth=0.85)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('My Very Own Histogram')
    plt.text(23, 45, r'$\mu=15, b=3$')
    max_freq = n.max()
    plt.ylim(ymax=np.ceil(max_freq / 10) * 10 if max_freq % 10 else max_freq + 10)
    plt.show()


def main() -> None:
    # file_name = Path(input('filename >'))
    #
    # if not file_name.exists() or not file_name.is_file():
    #     print(file_name + 'does not exists or is not a file.')
    #

    file_name = '../notesproba.txt'
    observations_num, marks_list = read_file(file_name)

    marks_sum = sum(marks_list)

    # La moyenne empirique d'un échantillon est la somme de ses éléments divisée par leur nombre.
    # Si l'échantillon est noté (x1,x2,x3,....xn), sa moyenne empirique est :
    # x barre = (x1+x2+x3+....xn) / n
    emp_avg = empiric_average(marks_sum, observations_num)

    sd = standard_deviation(emp_avg, marks_list, observations_num)

    first_quartile = percentile(marks_list, observations_num, 25)
    third_quartile = percentile(marks_list, observations_num, 75)

    # Le kurosis est le moment centré d’ordre 4 normalisé par l'écart-type élevé à la puissance 4.
    kurtosis = moments(emp_avg, marks_list, observations_num, sd, 4)
    # Le skewness est le moment centré d’ordre 3 normalisé par l'écart-type élevé au cube.
    skewness = moments(emp_avg, marks_list, observations_num, sd, 3)


if __name__ == "__main__":
    main()

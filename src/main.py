import os
from math import sqrt, ceil
from pathlib import Path
from typing import List, Tuple, Dict

import numpy as np
import matplotlib.pyplot as plt


def read_file(file_name) -> List[float]:
    lines = []
    with open(file_name) as file:
        for line in file:
            lines.append(float(line.strip()))
    return lines


def empiric_average(marks, observations_num) -> float:
    return sum(marks) / observations_num


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


def percentile(marks_list, observations_num, percentile) -> float:
    tmp = ceil(observations_num * (percentile / 100))
    sorted_marks_list = sorted(marks_list)
    return sorted_marks_list[tmp]


def histogram(data, title):
    n, bins, patches = plt.hist(x=data, bins='auto', color='#0504aa', alpha=0.7, rwidth=0.85)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title(title)
    max_freq = n.max()
    plt.ylim(ymax=np.ceil(max_freq / 10) * 10 if max_freq % 10 else max_freq + 10)
    plt.show()


def standard_derivation_estimation(ea1, len1, marks_list1) -> float:
    sd = 0.0
    for mark in marks_list1:
        sd += pow(mark - ea1, 2)
    return sqrt(sd / (len1 - 1))


def av_trust_interval(alpha, standard_dev, empiric_average, len) -> Tuple[float, float]:
    quantile = 1 - (alpha / 2)
    inf = standard_dev - sqrt(pow(empiric_average, 2) / len) * quantile
    sup = standard_dev + sqrt(pow(empiric_average, 2) / len) * quantile
    return inf, sup


def test_hypothesis_membership(standard_dev, len, u0, ea, alpha) -> bool:
    # loi de student a n-1 degré de liberté
    test_statistic = sqrt(len) * ((ea - u0) / standard_dev)
    quantile2 = 1 - alpha
    if test_statistic > quantile2:
        return False
    else:
        return True


def descriptive_statistics():
    os.system('clear')
    print('***** Statistiques descriptives *****')

    lists = open_files()

    if len(lists) == 0:
        menu()

    for dict in lists:
        key = list(dict.keys())[0]
        values = list(dict.values())[0]

        print("\n***** File " + key + " *****\n")

        observations_num = len(values)

        # La moyenne empirique d'un échantillon est la somme de ses éléments divisée par leur nombre.
        # Si l'échantillon est noté (x1,x2,x3,....xn), sa moyenne empirique est :
        # x barre = (x1+x2+x3+....xn) / n
        emp_avg = empiric_average(values, observations_num)

        sd = standard_deviation(emp_avg, values, observations_num)
        first_quartile = percentile(values, observations_num, 25)
        third_quartile = percentile(values, observations_num, 75)

        # Le kurosis est le moment centré d’ordre 4 normalisé par l'écart-type élevé à la puissance 4.
        kurtosis = moments(emp_avg, values, observations_num, sd, 4)

        # Le skewness est le moment centré d’ordre 3 normalisé par l'écart-type élevé au cube.
        skewness = moments(emp_avg, values, observations_num, sd, 3)

        print('Moyenne empirique : ' + str(emp_avg))
        print('Ecart-type : ' + str(sd))
        print('Premier quartile : ' + str(first_quartile))
        print('Troisième quartile : ' + str(third_quartile))
        print('Kurtosis : ' + str(kurtosis))
        print('Skewness : ' + str(skewness))

        histogram(values, key + 'Histogram')

    print('\nq - Quitter')

    command = ''
    while command != 'q':
        command = input()

    menu()


def inferential_statistics() -> None:
    os.system('clear')
    print('***** Statistiques inférentielles *****')

    marks_list1 = open_files()
    len1 = len(marks_list1)
    marks_list2 = open_files()
    len2 = len(marks_list2)

    trust_level1 = 0.95
    trust_level2 = 0.75
    alpha1 = 0.05 - trust_level1
    alpha2 = 1 - trust_level2

    # Une estimation de l'espérance sans biais et converge vers la moyenne empirique
    # d'après la loi forte des grands nombres pour un échantillon assez grand.
    ea1 = empiric_average(marks_list1, len1)
    ea2 = empiric_average(marks_list2, len2)

    # Une estimation de sigma, lorsque la moyenne est inconnue, est la racine de la variance empirique corrigée.
    sd1 = standard_deviation(ea1, marks_list1, len1)
    sd2 = standard_deviation(ea2, marks_list2, len2)

    standard_derivation_estimation(ea1, len1, marks_list1)
    standard_derivation_estimation(ea2, len2, marks_list2)

    avti1 = av_trust_interval(alpha1, sd1, ea1, len1)
    avti2 = av_trust_interval(alpha2, sd2, ea2, len2)

    test1 = test_hypothesis_membership(sd1, len1, 3, ea1, alpha1)

    a = 2


def open_files() -> List[Dict[str, List[float]]]:
    res = []
    valid_file = False

    while not valid_file:
        files = input('filename > ')

        for filename in files.split():
            tmp = Path(filename)
            if tmp.exists() and tmp.is_file():
                res.append({filename: read_file(filename)})
            else:
                print(str(filename) + ' does not exists or is not a file.\n', end='')

        valid_file = True

    return res


def menu() -> None:
    os.system('clear')
    print('***** Menu *****')
    print('1 - Statistiques descriptives')
    print('2 - Statistiques inférentielles')
    print('q - Quitter')

    valid_command = False
    choice = -1

    while not valid_command:
        choice = input()
        if choice not in ['1', '2', 'q']:
            print("Commande non reconnue.")
        else:
            valid_command = True

    if choice == '1':
        descriptive_statistics()

    elif choice == '2':
        inferential_statistics()

    else:
        exit(0)


def main() -> None:
    menu()


if __name__ == "__main__":
    main()

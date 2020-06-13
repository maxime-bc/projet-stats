from math import sqrt, ceil
from pathlib import Path
from typing import List, Tuple

import numpy as np
import matplotlib.pyplot as plt


def read_file(file_name) -> List[float]:
    lines = []
    with open(file_name) as file:
        for line in file:
            lines.append(float(line.strip()))
    return lines


def empiric_average(marks, observations_num):
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


def descriptive_statistics(file_name):
    marks_list = read_file(file_name)
    observations_num = len(marks_list)

    # La moyenne empirique d'un échantillon est la somme de ses éléments divisée par leur nombre.
    # Si l'échantillon est noté (x1,x2,x3,....xn), sa moyenne empirique est :
    # x barre = (x1+x2+x3+....xn) / n
    emp_avg = empiric_average(marks_list, observations_num)

    sd = standard_deviation(emp_avg, marks_list, observations_num)
    first_quartile = percentile(marks_list, observations_num, 25)
    third_quartile = percentile(marks_list, observations_num, 75)

    # Le kurosis est le moment centré d’ordre 4 normalisé par l'écart-type élevé à la puissance 4.
    kurtosis = moments(emp_avg, marks_list, observations_num, sd, 4)

    # Le skewness est le moment centré d’ordre 3 normalisé par l'écart-type élevé au cube.
    skewness = moments(emp_avg, marks_list, observations_num, sd, 3)


def standard_derivation_estimation(ea1, len1, marks_list1):
    sd = 0.0
    for mark in marks_list1:
        sd += pow(mark - ea1, 2)
    return sqrt(sd / (len1 - 1))


def av_trust_interval(alpha,standard_dev,empiric_average,len):
    quantile=1-(alpha/2)
    inf=standard_dev-sqrt(pow(empiric_average,2)/len)*quantile
    sup=standard_dev+sqrt(pow(empiric_average,2)/len)*quantile

    return (inf,sup)

def test_hypothesis_membership(standard_dev,len,u0,ea,alpha):
    #loi de student a n-1 degré de liberté
    test_statistique=sqrt(len)*((ea-u0)/standard_dev)
    quantile=1-alpha/2
    if test_statistique<quantile or test_statistique>quantile
        return True
    else:
        return False


    
        

def inferential_statistics(file_name1, file_name2):
    marks_list1 = read_file(file_name1)
    len1 = len(marks_list1)
    marks_list2 = read_file(file_name2)
    len2 = len(marks_list2)

    trust_level1 = 0.95
    trust_level2 = 0.75
    alpha1 = 1 - trust_level1
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



def open_file() -> List[float]:

    valid_file = False

    while not valid_file:
        file_name = Path(input('filename > '))
        if file_name.exists() and file_name.is_file():
            return read_file(file_name)
        else:
            print(str(file_name) + ' does not exists or is not a file.\n', end='')


def menu() -> None:

    print('Menu')
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
        print('Statistiques descriptives')
        # descriptive_statistics()

    elif choice == '2':
        print('Statistiques inférentielles')
        # inferential_statistics()
    else:
        exit(0)


def main() -> None:
    menu()

    file_name = '../notesproba.txt'
    file_name2 = '../notestat.txt'
    # descriptive_statistics(file_name)
    inferential_statistics(file_name, file_name2)


if __name__ == "__main__":
    main()

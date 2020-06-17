import os
from math import sqrt, ceil
from pathlib import Path
from typing import List, Tuple

import scipy
from scipy import stats

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t

''' Lecture de fichiers '''


def read_file(filename: str) -> List[float]:
    lines: List[float] = []
    with open(filename) as file:
        for line in file:
            lines.append(float(line.strip()))
    return lines


def open_file(message: str) -> Tuple[str, List[float]]:
    while True:
        file: Path = Path(input(message))
        if file.exists() and file.is_file():
            return str(file), read_file(str(file))
        else:
            print(str(file) + ' does not exists or is not a file.\n', end='')


''' Partie statistiques descriptives '''


def empiric_average(values: List[float], length: int) -> float:
    return sum(values) / length


def standard_deviation(values: List[float], length: int) -> float:
    sd: float = 0.0
    empiric_avg: float = empiric_average(values, length)
    for mark in values:
        sd += pow(mark - empiric_avg, 2)
    return sqrt(sd / length)


def moments(values: List[float], length: int, power: int) -> float:
    fourth_central_moment: float = 0.0
    empiric_avg: float = empiric_average(values, length)
    std_dev: float = standard_deviation(values, length)

    for mark in values:
        fourth_central_moment += pow(mark - empiric_avg, power)
    return (fourth_central_moment / length) / pow(std_dev, power)


def percentile(values: List[float], length: int, percentage: float) -> float:
    sorted_marks_list: List[float] = sorted(values)
    return sorted_marks_list[ceil(length * (percentage / 100))]


def histogram(values: List[float], title: str) -> None:
    n, bins, patches = plt.hist(x=values, bins='auto', color='#0504aa', alpha=0.7, rwidth=0.85)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title(title)
    max_freq = n.max()
    plt.ylim(ymax=np.ceil(max_freq / 10) * 10 if max_freq % 10 else max_freq + 10)
    plt.show()


''' Partie statistiques inférentielles '''


def standard_derivation_estimation(ea: float, len: int, marks_list: List[float]) -> float:
    sd: float = 0.0
    for mark in marks_list:
        sd += pow(mark - ea, 2)
    return sqrt(sd / (len - 1))


def av_trust_interval(alpha: float, standard_dev: float, empiric_average: float, len: int) -> Tuple[float, float]:
    quantile: float = 1 - (alpha / 2)
    inf: float = standard_dev - sqrt(pow(empiric_average, 2) / len) * quantile
    sup: float = standard_dev + sqrt(pow(empiric_average, 2) / len) * quantile
    return inf, sup


def test_hypothesis_membership(standard_dev_estimation: float, len: int, ea: float, alpha: float) -> bool:
    u0: float = 10.5
    test_statistic: float = sqrt(len) * ((ea - u0) / standard_dev_estimation)
    # loi de student à n-1 degré de liberté
    quantile2: float = t.ppf(1 - alpha, df=len - 1)
    if test_statistic > quantile2:
        return False
    else:
        return True


def khi_square(alpha, values1, values2):
    # Le test statistique va tendre vers une loi de chi-deux à length - 1 degré de liberté.
    statistic_test = 0
    length = len(values1)
    for i in range(length):
        statistic_test += pow(values1[i] - values2[i], 2) / (length * values2[i])

    if statistic_test < scipy.stats.chi2.ppf(1 - alpha, length - 1):
        return False
    else:
        return True


def descriptive_statistics():
    def _desc_stats(filename, values):
        print("\n***** File " + filename + " *****\n")
        length = len(values)
        # La moyenne empirique d'un échantillon est la somme de ses éléments divisée par leur nombre.
        # Si l'échantillon est noté (x1,x2,x3,....xn), sa moyenne empirique est :
        # x barre = (x1+x2+x3+....xn) / n
        emp_avg = empiric_average(values, length)
        sd = standard_deviation(values, length)
        first_quartile = percentile(values, length, 25)
        third_quartile = percentile(values, length, 75)
        # Le kurosis est le moment centré d’ordre 4 normalisé par l'écart-type élevé à la puissance 4.
        kurtosis = moments(values, length, 4)
        # Le skewness est le moment centré d’ordre 3 normalisé par l'écart-type élevé au cube.
        skewness = moments(values, length, 3)
        print('Moyenne empirique : ' + str(emp_avg))
        print('Ecart-type : ' + str(sd))
        print('Premier quartile : ' + str(first_quartile))
        print('Troisième quartile : ' + str(third_quartile))
        print('Kurtosis : ' + str(kurtosis))
        print('Skewness : ' + str(skewness))
        histogram(values, filename + ' Histogram')

    os.system('clear')
    print('***** Statistiques descriptives *****')
    print('Les fichiers doivent contenir des valeurs numériques en colonne représentant '
          'les valeurs prises par une variable aléatoire.')
    filename1, values1 = open_file('Fichier contenant les notes en statistiques > ')
    filename2, values2 = open_file('Fichier contenant les notes en probabilité > ')

    _desc_stats(filename1, values1)
    _desc_stats(filename2, values2)

    print('\nq - Quitter')

    command = ''
    while command != 'q':
        command = input()

    menu()


def inferential_statistics() -> None:
    def _inf_stats(filename: str, values: List[float], trust_level: float):
        print("\n***** File " + filename + " *****\n")

        length = len(values)
        alpha_int = 1 - trust_level
        # Une estimation de l'espérance sans biais et converge vers la moyenne empirique
        # d'après la loi forte des grands nombres pour un échantillon assez grand.
        ea = empiric_average(values, length)
        # Une estimation de sigma, lorsque la moyenne est inconnue, est la racine de la variance empirique corrigée.
        sde = standard_derivation_estimation(ea, length, values)
        avti = av_trust_interval(alpha_int, sde, ea, length)
        thm = test_hypothesis_membership(sde, length, ea, alpha_int)

        print('Estimation de l\'espérance : ' + str(ea))
        print('Estimation de l\'écart-type : ' + str(sde))
        print('Intervale de confiance moyen : ' + str(avti))
        if thm:
            print('Hypothèse d\'appartenance acceptée. ')
        else:
            print('Hypothèse d\'appartenance rejetée. ')

    os.system('clear')
    print('***** Statistiques inférentielles *****')
    print('Les fichiers doivent contenir des valeurs numériques en colonne représentant '
          'les valeurs prises par une variable aléatoire.')

    filename1, values1 = open_file('Fichier contenant les notes en statistiques > ')
    trust_level1 = ask_between_0_and_1('Niveau de confiance de l\'intervale de confiance')
    filename2, values2 = open_file('Fichier contenant les notes en probabilité > ')
    trust_level2 = ask_between_0_and_1('Niveau de confiance de l\'intervale de confiance')

    _inf_stats(filename1, values1, trust_level1)
    _inf_stats(filename2, values2, trust_level2)

    print("\nTest du khi deux : ")
    alpha = ask_between_0_and_1("alpha")

    if khi_square(alpha, values1, values2):
        print('D\'après le test du khi-deux, l\'hypothèse de comparaison de ' + filename1
              + ' et ' + filename2 + ' est acceptée.\n')
    else:
        print('D\'après le test du khi-deux, l\'hypothèse de comparaison de ' + filename1
              + ' et ' + filename2 + ' est rejetée.\n')

    print('q - Quitter')

    command = ''
    while command != 'q':
        command = input()

    menu()


def ask_between_0_and_1(var_name: str) -> float:
    while True:
        try:
            var = float(input(var_name + ' > '))

            if 0.0 < var < 1.0:
                return var
            else:
                print('0 < ' + var_name + ' < 1')
                continue

        except ValueError:
            continue


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

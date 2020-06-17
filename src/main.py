import os
from math import sqrt, ceil
from pathlib import Path
from typing import List, Tuple

import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.stats import t

""" Fonctions utilitaires """


def ask_between_0_and_1(var_name: str) -> float:
    """
    Cette fonction demande à l'utilisateur de choisir un nombre décimal compris entre 0 et 1.
    :param var_name: message à afficher à l'utilisateur avant de lui demander d'entrer le nombre.
    :return: le nombre décimal compris entre 0 et 1 choisi par l'utilisateur.
    """
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


def histogram(values: List[float], title: str) -> None:
    """
    Affiche un histograme rempli avec les valeurs passées en argument.
    :param values: valeurs avec lesquelles l'histograme sera construit.
    :param title: titre de l'histograme.
    """
    n, bins, patches = plt.hist(x=values, bins='auto', color='#0504aa', alpha=0.7, rwidth=0.85)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title(title)
    max_freq = n.max()
    plt.ylim(ymax=np.ceil(max_freq / 10) * 10 if max_freq % 10 else max_freq + 10)
    plt.show()


""" Lecture de fichiers """


def read_file(filename: str) -> List[float]:
    """
    Cette fonction lit un fichier contenant des valeurs numériques stockées en colonne
    et les retournes sont forme de liste.
    :param filename: le nom du fichier à ouvrir.
    :return: les valeurs stockées dans le fichier sous forme de liste.
    """
    lines: List[float] = []
    with open(filename) as file:
        for line in file:
            lines.append(float(line.strip()))
    return lines


def open_file(message: str) -> Tuple[str, List[float]]:
    """
    Cette fonction ouvre un fichier puis lit son contenu et le retourne.
    :param message: message à afficher à l'utilisateur avant de lui demander d'entrer le nom du fichier à ouvrir.
    :return: les valeurs stockées dans le fichier sous forme de liste.
    """
    while True:
        file: Path = Path(input(message))
        if file.exists() and file.is_file():
            return str(file), read_file(str(file))
        else:
            print(str(file) + ' n\'existe pas ou n\'est pas un fichier.\n', end='')


""" Partie statistique descriptive """


class DescriptiveStatistics(object):
    """
    Cette classe contient toutes les données nécessaires à la partie sur la statistique descriptive du programme.
    """

    def __init__(self, values: List[float]):
        self._values = values
        self._length = len(values)
        # La moyenne empirique d'un échantillon est la somme de ses éléments divisée par leur nombre.
        # Si l'échantillon est noté (x1,x2,x3,....xn), sa moyenne empirique est :
        # x barre = (x1+x2+x3+....xn) / n
        self._emp_average = sum(self._values) / self._length
        self._std_deviation = self._get_standard_deviation()
        self._first_quartile = self._get_percentile(25)
        self._third_quartile = self._get_percentile(75)
        # Le kurtosis est le moment centré d’ordre 4 normalisé par l'écart-type élevé à la puissance 4.
        self._kurtosis = self._get_moment(4)
        # Le skewness est le moment centré d’ordre 3 normalisé par l'écart-type élevé au cube.
        self._skewness = self._get_moment(3)

    def _get_standard_deviation(self) -> float:
        """
        Calcule l'écart-type en fonction de l'échantillon d'observations.
        :return: l'écart-type.
        """
        std_dev: float = 0.0
        for value in self._values:
            std_dev += pow(value - self._emp_average, 2)
        return sqrt(std_dev / self._length)

    def _get_percentile(self, percentage: float) -> float:
        """
        Calcule le centile en fonction du pourcentage donné en argument.
        :param percentage: le pourcentage avec lequel on souhaite calculer le centile.
        :return: le centile.
        """
        sorted_marks_list: List[float] = sorted(self._values)
        return sorted_marks_list[ceil(self._length * (percentage / 100))]

    def _get_moment(self, power: int) -> float:
        """
        Calcule le moment en à l'ordre passé en argument.
        :param power: ordre pour lequel doit être calculé le moment.
        :return: le moment.
        """
        fourth_central_moment: float = 0.0

        for value in self._values:
            fourth_central_moment += pow(value - self._emp_average, power)
        return (fourth_central_moment / self._length) / pow(self._std_deviation, power)

    def get_values(self) -> List[float]:
        return self._values

    def get_length(self) -> int:
        return self._length

    def get_empiric_average(self) -> float:
        return self._emp_average

    def get_standard_deviation(self) -> float:
        return self._std_deviation

    def get_first_quartile(self) -> float:
        return self._first_quartile

    def get_third_quartile(self) -> float:
        return self._third_quartile

    def get_kurtosis(self) -> float:
        return self._kurtosis

    def get_skewness(self) -> float:
        return self._skewness


""" Partie statistique inférentielle """


class InferentialStatistics(object):
    """
    Cette classe contient toutes les données nécessaires à la partie sur la statistique inférentielle du programme.
    """

    def __init__(self, values: List[float]):
        self._values = values
        self._length = len(values)
        # Une estimation de l'espérance sans biais et converge vers la moyenne empirique
        # d'après la loi forte des grands nombres pour un échantillon assez grand.
        self._empiric_average = sum(self._values) / self._length
        # Une estimation de sigma, lorsque la moyenne est inconnue, est la racine de la variance empirique corrigée.
        self._standard_deviation_estimation = self._get_standard_deviation_estimation()

    def _get_standard_deviation_estimation(self) -> float:
        """
        Estime l'écart-type en fonction de l'échantillon d'observations.
        :return: l'estimation de l'écart-type.
        """
        std_dev_estimation: float = 0.0

        for value in self._values:
            std_dev_estimation += pow(value - self._empiric_average, 2)
        return sqrt(std_dev_estimation / (self._length - 1))

    def get_values(self) -> List[float]:
        return self._values

    def get_length(self) -> int:
        return self._length

    def get_empiric_average(self) -> float:
        return self._empiric_average

    def get_standard_deviation_estimation(self) -> float:
        return self._standard_deviation_estimation

    def get_average_trust_interval(self, alpha: float) -> Tuple[float, float]:
        """
        Calcule l'intervalle moyen de confiance en fonction de la valeur d'alpha passée en argument.
        :param alpha: niveau de confiance de l'intervalle.
        :return: l'intervalle moyen de confiance.
        """
        quantile: float = 1 - (alpha / 2)
        inf: float = self._standard_deviation_estimation - sqrt(pow(self._empiric_average, 2) / self._length) * quantile
        sup: float = self._standard_deviation_estimation + sqrt(pow(self._empiric_average, 2) / self._length) * quantile
        return inf, sup

    def test_hypothesis_membership(self, alpha: float) -> bool:
        """
        Vérifie l'hypothèse d'appartenance en fonction de la valeur d'alpha.
        :param alpha: niveau de confiance de l'hypothèse.
        :return: True si l'hypothèse d'appartenance est validée et False s'il elle est déclinée.
        """
        u0: float = 10.5
        test_statistic: float = sqrt(self._length) * (
                (self._empiric_average - u0) / self._standard_deviation_estimation)
        # Loi de Student à n-1 degré de liberté
        quantile: float = t.ppf(1 - alpha, df=self._length - 1)
        if test_statistic > quantile:
            return False
        else:
            return True


def chi_square(alpha: float, values1: List[float], values2: List[float]) -> bool:
    """
    Effecture le test d'indépendance du khi-deux avec les deux échantillons passés en argument.
    :param alpha: niveau de confiance du test du chi-deux.
    :param values1: échantillon 1.
    :param values2: échantillon 2.
    :return: True si le test d'indépendance a réussi et False s'il a échoué.
    """
    # Le test statistique va tendre vers une loi de chi-deux à length - 1 degré de liberté.
    assert len(values1) == len(values2)
    statistic_test: float = 0.0
    length = len(values1)
    for i in range(length):
        statistic_test += pow(values1[i] - values2[i], 2) / (length * values2[i])

    if statistic_test < scipy.stats.chi2.ppf(1 - alpha, length - 1):
        return False
    else:
        return True


""" Fonctions gérant l'affichage """


def descriptive_statistics() -> None:
    """
    Cette fonction s'occupe de l'affichage de la partie du programme sur la statistique descriptive.
    """

    def _desc_stats(filename, values) -> None:
        print("\n***** File " + filename + " *****\n")

        desc_stats = DescriptiveStatistics(values)
        print('Moyenne empirique : ' + str(desc_stats.get_empiric_average()))
        print('Ecart-type : ' + str(desc_stats.get_standard_deviation()))
        print('Premier quartile : ' + str(desc_stats.get_first_quartile()))
        print('Troisième quartile : ' + str(desc_stats.get_third_quartile()))
        print('Kurtosis : ' + str(desc_stats.get_kurtosis()))
        print('Skewness : ' + str(desc_stats.get_skewness()))
        histogram(values, filename + ' Histogram')

    os.system('clear')
    print('***** Statistique descriptive *****')
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
    """
    Cette fonction s'occupe de l'affichage de la partie du programme sur la statistique inférentielle.
    """

    def _inf_stats(filename: str, values: List[float]) -> None:
        print("\n***** File " + filename + " *****\n")

        trust_level = ask_between_0_and_1('Niveau de confiance de l\'intervalle de confiance')
        alpha_int = 1 - trust_level
        inf_stats = InferentialStatistics(values)
        print('Estimation de l\'espérance : ' + str(inf_stats.get_empiric_average()))
        print('Estimation de l\'écart-type : ' + str(inf_stats.get_standard_deviation_estimation()))
        print('Intervale de confiance moyen : ' + str(inf_stats.get_average_trust_interval(alpha_int)))
        if inf_stats.test_hypothesis_membership(alpha_int):
            print('Hypothèse d\'appartenance acceptée. ')
        else:
            print('Hypothèse d\'appartenance rejetée. ')

    os.system('clear')
    print('***** Statistique inférentielle *****')
    print('Les fichiers doivent contenir des valeurs numériques en colonne représentant '
          'les valeurs prises par une variable aléatoire.')

    filename1, values1 = open_file('Fichier contenant les notes en statistiques > ')
    _inf_stats(filename1, values1)
    filename2, values2 = open_file('Fichier contenant les notes en probabilité > ')
    _inf_stats(filename2, values2)

    print("\nTest du khi-deux : ")
    alpha = ask_between_0_and_1("alpha")

    if chi_square(alpha, values1, values2):
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


def menu() -> None:
    """
    Cette fonction gère le menu du programme.
    """
    os.system('clear')
    print('***** Menu *****')
    print('1 - Statistique descriptive')
    print('2 - Statistique inférentielle')
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
    """
    Fontion principale du programme.
    """
    menu()


if __name__ == "__main__":
    main()

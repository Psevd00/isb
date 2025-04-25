import math

# noinspection PyUnresolvedReferences
from scipy.special import erfc, gammaincc


def frequency_test(sequence):
    '''
    Частотный побитовый тест NIST
    :param sequence: Бинарная строка, состоящая из '0' и '1'
    :return: P-значение в диапазоне [0, 1].
    '''
    n = len(sequence)
    s = sum(1 if bit == '1' else -1 for bit in sequence)
    s_abs = abs(s) / math.sqrt(n)
    p_value = erfc(s_abs / math.sqrt(2))
    return p_value


def runs_test(sequence):
    '''
    Тест на одинаковые подряд идущие биты
    :param sequence: Бинарная строка, состоящая из '0' и '1'
    :return: P-значение в диапазоне [0, 1].
    '''
    n = len(sequence)
    ones = sequence.count('1')
    prop = ones / n
    if abs(prop - 0.5) >= 2 / math.sqrt(n):
        return 0.0

    runs = 0
    for i in range(n - 1):
        if sequence[i] != sequence[i + 1]:
            runs += 1

    numerator = abs(runs - 2 * n * prop * (1 - prop))
    denominator = 2 * math.sqrt(2 * n) * prop * (1 - prop)
    p_value = erfc(numerator / denominator)
    return p_value

def load_constants():
    '''
    Загружает константы и параметры из файла constants.txt.
    :return: Словарь
    '''
    constants = {}
    with open('constants.txt', 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=')
                constants[key.strip()] = value.strip()
    return constants


constants = load_constants()
PI_VALUES = list(map(float, constants['PI_VALUES'].split(',')))


def longest_run_test(sequence, block_size=8):
    '''
    Тест на самую длинную последовательность единиц в блоке
    :param sequence: Бинарная строка, состоящая из '0' и '1'
    :param block_size: Размер блока для анализа.
    :return: P-значение в диапазоне [0, 1].
    '''
    blocks = [sequence[i:i + block_size] for i in range(0, len(sequence), block_size)]
    v = [0, 0, 0, 0]

    for block in blocks:
        max_run = 0
        current_run = 0
        for bit in block:
            if bit == '1':
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0

        if max_run <= 1:
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        else:
            v[3] += 1

    chi2 = sum((v[i] - 16 * PI_VALUES[i]) ** 2 / (16 * PI_VALUES[i]) for i in range(4))
    p_value = gammaincc(1.5, chi2 / 2)
    return p_value

#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import random

def generate_matrix(rows, cols, min_val, max_val):
    """Генерирует матрицу случайных целых чисел."""
    return [[random.randint(min_val, max_val) for _ in range(cols)] for _ in range(rows)]


def main():
    while True:
        try:
            # Запрашиваем ввод количества строк и столбцов
            rows = int(input("Введите количество строк: "))
            cols = int(input("Введите количество столбцов: "))
            min_val = int(input("Введите минимальное значение: "))
            max_val = int(input("Введите максимальное значение: "))

            # Проверяем, чтобы количество строк и столбцов было положительным
            if rows <= 0 or cols <= 0:
                raise ValueError("Количество строк и столбцов должно быть положительным числом.")
            if min_val > max_val:
                raise ValueError("Минимальное значение не может быть больше максимального.")

            # Генерируем и выводим матрицу
            matrix = generate_matrix(rows, cols, min_val, max_val)
            print("Сгенерированная матрица:")
            for row in matrix:
                print(row)
            break  # Выход из цикла после успешного выполнения
        except ValueError as e:
            print(f"Ошибка ввода: {e}. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()
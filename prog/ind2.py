#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import argparse
import os.path
import pathlib
import logging

# Настройка логирования
logging.basicConfig(
    filename='trains.log',
    level=logging.DEBUG,
    format='%(asctime)s.%f - %(levelname)s - %(message)s',  # Добавлено миллисекундное время
    datefmt='%Y-%m-%d %H:%M:%S', encoding='utf-8'  # Формат даты и времени
)

def add_train(trains, nomer, punkt, time):
    """
    Запросить данные о поездах и добавить новый поезд, если номер уникален.
    """
    if any(train['nomer'] == nomer for train in trains):
        logging.error(f"Ошибка: Поезд с номером {nomer} уже существует.")
        print(f"Ошибка: Поезд с номером {nomer} уже существует.")
        return trains

    trains.append(
        {
            "nomer": nomer,
            "punkt": punkt,
            "time": time,
        }
    )
    logging.info(f"Добавлен поезд: {nomer}, пункт: {punkt}, время: {time}")
    return trains


def display_trains(punkts):
    """
    Отобразить список поездов.
    """
    if punkts:
        line = "+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4, "-" * 30, "-" * 20, "-" * 17)
        print(line)
        print(
            "| {:^4} | {:^30} | {:^20} | {:^17} |".format(
                "№", "Номер поезда", "Пункт назначения", "Время отправления"
            )
        )
        print(line)
        for idx, train in enumerate(punkts, 1):
            print(
                "| {:>4} | {:<30} | {:<20} | {:>17} |".format(
                    idx,
                    train.get("nomer", ""),
                    train.get("punkt", ""),
                    train.get("time", 0),
                )
            )
        print(line)
    else:
        print("Список поездов пуст.")


def select_trains(punkts, period):
    """
    Выбрать поезда с заданным временем.
    """
    result = []
    for van in punkts:
        if van.get("time", 0) >= period:
            result.append(van)
    return result


def save_trains(filename, punkts):
    """
    Сохранить все поезда в JSON файл.
    """
    try:
        with open(filename, "w", encoding="utf-8") as fout:
            json.dump(punkts, fout, ensure_ascii=False, indent=4)
        logging.info(f"Данные о поездах сохранены в файл: {filename}")
    except IOError as e:
        logging.error(f"Ошибка при сохранении данных в файл: {e}")
        print(f"Ошибка при сохранении данных в файл: {e}")


def load_trains(filename):
    """
    Загрузить поезда из файла JSON.
    """
    try:
        with open(filename, "r", encoding="utf-8") as fin:
            return json.load(fin)
    except FileNotFoundError:
        logging.warning(f"Файл не найден: {filename}")
        print(f"Файл не найден: {filename}")
        return []
    except json.JSONDecodeError:
        logging.error(f"Ошибка декодирования JSON в файле: {filename}")
        print(f"Ошибка декодирования JSON в файле: {filename}")
        return []
    except Exception as e:
        logging.error(f"Неизвестная ошибка при загрузке файла: {e}")
        print(f"Неизвестная ошибка при загрузке файла: {e}")
        return []


def main(command_line=None):
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument("filename", action="store", help="The data file name")
    parser = argparse.ArgumentParser("trains")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    subparsers = parser.add_subparsers(dest="command")
    
    add = subparsers.add_parser("add", parents=[file_parser], help="Add a new train`s punkt")
    add.add_argument("-t", "--train", action="store", required=True, help="The train's number")
    add.add_argument("-p", "--punkt", action="store", help="The train's punkt")
    add.add_argument("-tm", "--time", action="store", type=int, required=True, help="Departure time")
    
    _ = subparsers.add_parser("display", parents=[file_parser], help="Display all trains")
    
    select = subparsers.add_parser("select", parents=[file_parser], help="Select the trains")
    select.add_argument("-tm", "--time", action="store", type=int, required=True, help="The distation")
    
    args = parser.parse_args(command_line)
    
    is_dirty = False
    homedir = pathlib.Path.home()
    if os.path.exists(args.filename):
        trains = load_trains(args.filename)
    elif pathlib.Path(f"{homedir / args.filename}").exists():
        trains = load_trains(homedir / args.filename)
    else:
        trains = []
    
    if args.command == "add":
        trains = add_train(trains, args.train, args.punkt, args.time)
        is_dirty = True
        logging.info(f"Команда 'add' выполнена для поезда {args.train}.")
    
    if args.command == "display":
        display_trains(trains)
        logging.info("Команда 'display' выполнена.")
    
    if args.command == "select":
        selected = select_trains(trains, args.time)
        display_trains(selected)
        logging.info(f"Команда 'select' выполнена с параметром времени: {args.time}.")
    
    if is_dirty:
        save_trains(args.filename, trains)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.critical(f"Неизвестная ошибка в основном потоке: {e}")
        print(f"Неизвестная ошибка: {e}")
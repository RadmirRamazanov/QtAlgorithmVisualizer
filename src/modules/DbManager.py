"""
Модуль: Менеджер бд
Автор: Радмир Рамазанов
Описание: Модуль для управление бд к проекту "QtAlgorithmVisualizer"
"""
import sqlite3


class DatabaseManager:
    """
    Класс для управления бд алгоритмов
    Отвечает за подключение к бд, выполнению запросов
    """
    def __init__(self):
        self.con = sqlite3.connect("algo.sqlite")

    def get_algorithm_info(self, algorithm_name):
        return self.con.cursor().execute(
            """SELECT description, asymptotics, video FROM algorithms WHERE name = ?""",
            (algorithm_name,)
        ).fetchone()

    def get_category_info(self, algorithm_name):
        return self.con.cursor().execute(
            """SELECT name, description FROM categories WHERE name = ?""",
            (algorithm_name,)
        ).fetchone()

    def get_all_algorithms_for_txt(self):
        return self.con.cursor().execute(
            """SELECT name, description FROM algorithms"""
        ).fetchall()

    def get_all_algorithms_for_csv(self):
        return self.con.cursor().execute(
            """SELECT name, description, asymptotics FROM algorithms"""
        ).fetchall()

    def update_category(self, category_text, algorithm_name):
        self.con.cursor().execute(
            """UPDATE categories SET description = ? WHERE name = ?""",
            (category_text, algorithm_name)
        )
        self.con.commit()

    def update_algorithm(self, algorithm_text, algorithm_name):
        self.con.cursor().execute(
            """UPDATE algorithms SET description = ? WHERE name = ?""",
            (algorithm_text, algorithm_name)
        )
        self.con.commit()
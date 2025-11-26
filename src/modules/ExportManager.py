"""
Модуль: Менеджер экспорта данных
Автор: Радмир Рамазанов
Описание: Модуль для управление экспортом данных к проекту "QtAlgorithmVisualizer"
"""
import csv
from PyQt6.QtWidgets import QFileDialog, QMessageBox


class ExportManager:
    """
    Класс для экспорта данных из бд в txt/csv
    Отвечает за экспорт, форматирование в файлах
    """
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def export_to_txt(self, parent):
        result = self.db_manager.get_all_algorithms_for_txt()
        fname = QFileDialog.getOpenFileName(parent, 'Выбрать файл', '')[0]
        if fname:
            with open(fname, "w", encoding="utf-8") as f:
                for i in result:
                    f.writelines(i[0] + "\n" + i[1] + "\n")
            self.show_message(parent)

    def export_to_csv(self, parent):
        result = self.db_manager.get_all_algorithms_for_csv()
        fname = QFileDialog.getOpenFileName(parent, 'Выбрать файл', '')[0]
        if fname:
            with open(fname, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(["name", "code", "asymptotics"])
                for i in result:
                    writer.writerow(i)
            self.show_message(parent)

    def show_message(self, parent):
        messagebox = QMessageBox(parent)
        messagebox.setText("Успешно!")
        messagebox.exec()
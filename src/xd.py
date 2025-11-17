import sys
import sqlite3
import csv
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QMessageBox
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtMultimedia import QMediaPlayer


class QtAlgorithmsVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("design.ui", self)
        self.con = sqlite3.connect("algo.sqlite")
        self.tree_widget.itemClicked.connect(self.algorithm_info)
        self.export_txt_btn.clicked.connect(self.export_to_txt)
        self.export_csv_btn.clicked.connect(self.export_to_csv)
        self.update_btn.clicked.connect(self.update_info)
        self.counter = 0
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.setPixmap(
            QPixmap("dark-abstract-background-black-overlap-free.jpg").scaled(
            self.width(), self.height(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding))
        self.background_label.lower()
        self.background.clicked.connect(self.wallpaper)
        self.media_player = QMediaPlayer(self)
        self.video_widget = QVideoWidget(self)
        self.video_widget.setMinimumSize(500, 400)
        self.media_player.setVideoOutput(self.video_widget)
        self.verticalLayout_3.insertWidget(0, self.video_widget)
        self.textEdit.setParent(None)
        self.media_player.positionChanged.connect(self.update_video_progress)
        self.media_player.durationChanged.connect(self.update_video_duration)
        self.progress_slider.sliderMoved.connect(self.set_video_position)
        self.video_widget.setAspectRatioMode(Qt.AspectRatioMode.IgnoreAspectRatio)

    def update_info(self):
        if self.title_label.text() in ["Сортировки", "Алгоритмы поиска", "Теория чисел",
                                        "Динамическое программирование", "Графы"]:
            self.con.cursor().execute("""UPDATE categories
            SET description = ?
            WHERE name = ?""", (self.textEdit_2.toPlainText(), self.title_label.text()))
            self.con.commit()
            messagebox = QMessageBox(self)
            messagebox.setText("Успешно!")
            messagebox.exec()
            return
        self.con.cursor().execute("""UPDATE algorithms
        SET description = ?
        WHERE name = ?""", (self.textEdit_2.toPlainText(), self.title_label.text()))
        self.con.commit()
        messagebox = QMessageBox(self)
        messagebox.setText("Успешно!")
        messagebox.exec()

    def algorithm_info(self, item, col):
        algorithm_text = item.text(col)
        self.title_label.setText(algorithm_text)
        if algorithm_text in ["Сортировки", "Алгоритмы поиска", "Теория чисел",
                                  "Динамическое программирование", "Графы"]:
            result = self.con.cursor().execute(f"""SELECT name, description FROM categories
            WHERE name = ?""", (algorithm_text,)).fetchone()
            self.textEdit_2.setText(result[1])
            self.time.setText(f"Временная сложность: ")
            return
        result = self.con.cursor().execute(f"""SELECT description, asymptotics, video FROM algorithms
        WHERE name = ?""", (algorithm_text,)).fetchone()
        self.textEdit_2.setText(result[0])
        self.time.setText(f"Временная сложность: {result[1]}")
        self.media_player.setSource(QUrl.fromLocalFile(result[2]))
        self.media_player.play()

    def export_to_txt(self):
        result = self.con.cursor().execute(
            f"""SELECT name, description FROM algorithms""").fetchall()
        fname = QFileDialog.getOpenFileName(self, 'Выбрать файл', '')[0]
        with open(fname, "w", encoding="utf-8") as f:
            for i in result:
                f.writelines(i[0] + "\n" + i[1] + "\n")
        messagebox = QMessageBox(self)
        messagebox.setText("Успешно!")
        messagebox.exec()

    def export_to_csv(self):
        result = self.con.cursor().execute(
            f"""SELECT name, description, asymptotics FROM algorithms""").fetchall()
        fname = QFileDialog.getOpenFileName(self, 'Выбрать файл', '')[0]
        with open(fname, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["name", "code", "asymptotics"])
            for i in result:
                writer.writerow(i)
        messagebox = QMessageBox(self)
        messagebox.setText("Успешно!")
        messagebox.exec()

    def wallpaper(self):
        if self.counter % 2 == 0:
            self.background_label.setPixmap(QPixmap("dark_back1.jpg").scaled(
                self.width(), self.height(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding))
        else:
            self.background_label.setPixmap(
                QPixmap("dark-abstract-background-black-overlap-free.jpg").scaled(
                self.width(), self.height(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding))
        self.counter += 1

    def update_video_progress(self, position):
        if self.media_player.duration() > 0:
            progress = (position / self.media_player.duration()) * 100
            self.progress_slider.setValue(int(progress))
            current_sec = position // 1000
            total_sec = self.media_player.duration() // 1000
            self.time_label.setText(
                f"{current_sec // 60:02d}:{current_sec % 60:02d} / {total_sec // 60:02d}:{total_sec % 60:02d}")

    def update_video_duration(self):
        self.progress_slider.setRange(0, 100)

    def set_video_position(self, position):
        if self.media_player.duration() > 0:
            new_position = (position / 100) * self.media_player.duration()
            self.media_player.setPosition(int(new_position))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QtAlgorithmsVisualizer()
    ex.show()
    sys.exit(app.exec())

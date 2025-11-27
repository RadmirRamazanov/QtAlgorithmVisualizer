import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QMessageBox,
                             QTextEdit, QPushButton, QVBoxLayout, QFrame,
                             QHBoxLayout, QDialog)
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtMultimedia import QMediaPlayer
from modules.DbManager import DatabaseManager
from modules.ExportManager import ExportManager
from modules.design import Ui_MainWindow


class BackgroundManager:
    """
    Класс для управления фоном
    Отвечает за изображения фона
    """
    def __init__(self, parent):
        self.counter = 0
        self.background_label = QLabel(parent)
        self.background_label.setGeometry(0, 0, parent.width(), parent.height())
        self.background_label.lower()
        self.set_default_background(parent)

    def set_default_background(self, parent):
        self.background_label.setPixmap(
            QPixmap("content/pictures/dark-abstract-background-black-overlap-free.jpg").scaled(
                parent.width(), parent.height(),
                Qt.AspectRatioMode.IgnoreAspectRatio))

    def toggle_background(self, parent):
        if self.counter % 2 == 0:
            self.background_label.setPixmap(QPixmap("content/pictures/dark_back1.jpg").scaled(
                parent.width(), parent.height(),
                Qt.AspectRatioMode.IgnoreAspectRatio))
        else:
            self.background_label.setPixmap(
                QPixmap("content/pictures/dark-abstract-background-black-overlap-free.jpg").scaled(
                parent.width(), parent.height(),
                Qt.AspectRatioMode.IgnoreAspectRatio))
        self.counter += 1


class VideoManager:
    """
    Класс для управления видео алгоритмов
    Отвечает за виджет, воспроизведение видео
    """
    def __init__(self, parent):
        self.parent = parent
        self.media_player = QMediaPlayer(parent)
        self.video_widget = QVideoWidget(parent)
        self.video_widget.setMinimumSize(500, 400)
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.positionChanged.connect(self.update_video_progress)
        self.media_player.durationChanged.connect(self.update_video_duration)
        self.video_widget.setAspectRatioMode(Qt.AspectRatioMode.IgnoreAspectRatio)

    def setup_video(self, video):
        self.media_player.setSource(QUrl.fromLocalFile(video))
        self.media_player.play()

    def update_video_progress(self, position):
        if self.media_player.duration() > 0:
            progress = (position / self.media_player.duration()) * 100
            self.parent.progress_slider.setValue(int(progress))
            current_sec = position // 1000
            total_sec = self.media_player.duration() // 1000
            self.parent.time_label.setText(
                f"{current_sec // 60:02d}:{current_sec % 60:02d} / {total_sec // 60:02d}:{total_sec % 60:02d}")

    def update_video_duration(self):
        self.parent.progress_slider.setRange(0, 100)

    def set_video_position(self, position):
        if self.media_player.duration() > 0:
            new_position = (position / 100) * self.media_player.duration()
            self.media_player.setPosition(int(new_position))


class AboutDialog(QDialog):
    """
    Класс показа формы с информацией о программе
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setFixedSize(450, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: #ffffff;
                font-family: 'Segoe UI', Arial;
            }
            QLabel {
                color: #cccccc;
                font-size: 12px;
            }
            QLabel#titleLabel {
                color: #ffffff;
                font-size: 18px;
                font-weight: bold;
            }
            QLabel#versionLabel {
                color: #0078d7;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #404040;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:pressed {
                background-color: #606060;
            }
            QFrame#separator {
                background-color: #555555;
                max-height: 1px;
                min-height: 1px;
            }
            QTextEdit {
                background-color: #323232;
                color: #cccccc;
                border: 1px solid #555555;
                border-radius: 4px;
                font-size: 11px;
                padding: 10px;
            }
        """)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        title_label = QLabel("Визуализатор алгоритмов")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        version_label = QLabel("Версия 1.0.0")
        version_label.setObjectName("versionLabel")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(version_label)
        separator1 = QFrame()
        separator1.setObjectName("separator")
        separator1.setFrameShape(QFrame.Shape.HLine)
        main_layout.addWidget(separator1)
        description_text = QTextEdit()
        description_text.setReadOnly(True)
        description_text.setMaximumHeight(80)
        description_text.setPlainText(
            "Программа для интерактивной визуализации алгоритмов и структур данных. "
            "Позволяет изучать алгоритмы через наглядные анимации и примеры кода."
        )
        main_layout.addWidget(description_text)
        features_label = QLabel("Основные возможности:")
        features_label.setStyleSheet("font-weight: bold; color: #ffffff;")
        main_layout.addWidget(features_label)
        features_text = QTextEdit()
        features_text.setReadOnly(True)
        features_text.setMaximumHeight(120)
        features_text.setPlainText("""
1) Визуализация алгоритмов 
2) Примеры кода на Python
3) Подробные описания и сложность
4) Экспорт данных в TXT/CSV
5) Оффлайн-режим работы
        """.strip())
        main_layout.addWidget(features_text)
        separator2 = QFrame()
        separator2.setObjectName("separator")
        separator2.setFrameShape(QFrame.Shape.HLine)
        main_layout.addWidget(separator2)
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        developer_label = QLabel("Разработчик: Радмир Рамазанов")
        info_layout.addWidget(developer_label)
        course_label = QLabel("Курс: Яндекс Лицей 2")
        info_layout.addWidget(course_label)
        year_label = QLabel("Год: 2025")
        info_layout.addWidget(year_label)
        main_layout.addLayout(info_layout)
        tech_label = QLabel("Технологии: Python, PyQt6, SQLite")
        tech_label.setStyleSheet("font-style: italic; color: #888888;")
        tech_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(tech_label)
        main_layout.addStretch(1)
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.accept)
        close_button.setFixedWidth(120)
        button_layout.addWidget(close_button)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.accept()


class QtAlgorithmVisualizer(QMainWindow, Ui_MainWindow):
    """
    Главный класс
    ОТвечает за остальные классы и запуск интерфейса
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db_manager = DatabaseManager()
        self.export_manager = ExportManager(self.db_manager)
        self.video_player = VideoManager(self)
        self.background_manager = BackgroundManager(self)
        self.tree_widget.itemClicked.connect(self.algorithm_info)
        self.export_txt_btn.clicked.connect(self.export_to_txt)
        self.export_csv_btn.clicked.connect(self.export_to_csv)
        self.update_btn.clicked.connect(self.update_info)
        self.background.clicked.connect(self.wallpaper)
        self.pushButton.clicked.connect(self.show_about_dialog)
        self.progress_slider.sliderMoved.connect(self.video_player.set_video_position)
        self.verticalLayout_3.insertWidget(0, self.video_player.video_widget)
        self.textEdit.setParent(None)

    def algorithm_info(self, item, col):
        algorithm_name = item.text(col)
        self.title_label.setText(algorithm_name)
        if algorithm_name in ["Сортировки", "Алгоритмы поиска", "Теория чисел",
                                  "Динамическое программирование", "Графы"]:
            result = self.db_manager.get_category_info(algorithm_name)
            self.textEdit_2.setText(result[1])
            self.time.setText(f"Временная сложность: ")
            return
        result = self.db_manager.get_algorithm_info(algorithm_name)
        self.textEdit_2.setText(result[0])
        self.time.setText(f"Временная сложность: {result[1]}")
        print(result)
        self.video_player.setup_video(result[2])

    def update_info(self):
        if self.title_label.text() in ["Сортировки", "Алгоритмы поиска", "Теория чисел",
                                        "Динамическое программирование", "Графы"]:
            self.db_manager.update_category(self.textEdit_2.toPlainText(), self.title_label.text())
            self.show_message()
            return
        self.db_manager.update_algorithm(self.textEdit_2.toPlainText(), self.title_label.text())
        self.show_message()

    def export_to_txt(self):
        self.export_manager.export_to_txt(self)

    def export_to_csv(self):
        self.export_manager.export_to_csv(self)

    def wallpaper(self):
        self.background_manager.toggle_background(self)

    def show_message(self):
        messagebox = QMessageBox(self)
        messagebox.setText("Успешно!")
        messagebox.exec()

    def show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QtAlgorithmVisualizer()
    ex.show()
    sys.exit(app.exec())

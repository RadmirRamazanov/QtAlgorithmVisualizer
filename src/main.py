import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtMultimedia import QMediaPlayer
from DbManager import DatabaseManager
from ExportManager import ExportManager
from design import Ui_MainWindow


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
            QPixmap("dark-abstract-background-black-overlap-free.jpg").scaled(
                parent.width(), parent.height(),
                Qt.AspectRatioMode.IgnoreAspectRatio))

    def toggle_background(self, parent):
        if self.counter % 2 == 0:
            self.background_label.setPixmap(QPixmap("dark_back1.jpg").scaled(
                parent.width(), parent.height(),
                Qt.AspectRatioMode.IgnoreAspectRatio))
        else:
            self.background_label.setPixmap(
                QPixmap("dark-abstract-background-black-overlap-free.jpg").scaled(
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QtAlgorithmVisualizer()
    ex.show()
    sys.exit(app.exec())

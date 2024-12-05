import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QFileDialog, QWidget
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from ImageIterator import ImgIterator

class ImageViewer(QMainWindow):
    def __init__(self):
        """
        Вызывает конструктор родительского класса,
        создаёт окно приложения и его элементы
        а также три основных поля для функций класса:
        iterator, current_image_path и current_index
        """
        super().__init__()
        self.setWindowTitle("Lab5")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.image_place = QLabel("Здесь будет отображаться изображение")
        self.image_place.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_place)

        self.file_button = QPushButton("Выбрать файл аннотации")
        self.file_button.clicked.connect(self.select_annotation_file)
        self.layout.addWidget(self.file_button)

        self.prev_button = QPushButton("Предыдущее")
        self.prev_button.setEnabled(False)
        self.prev_button.clicked.connect(self.show_previous_image)
        self.layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Следующее")
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self.show_next_image)
        self.layout.addWidget(self.next_button)

        self.iterator = None
        self.current_image_paths = []
        self.current_index = -1

    def select_annotation_file(self):
        """
        Позволяет открыть в приложении аннотацию в формате CSV
        и просматривать изображения, пути к которым лежат
        в этой аннотации
        :return:
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл аннотации", "", "CSV Files (*.csv)")
        if file_path:
            self.iterator = ImgIterator(file_path)
            self.current_image_paths = list(self.iterator)
            if not self.current_image_paths:
                self.image_place.setText("Файл аннотации пуст или не содержит данных.")
            else:
                self.current_index = 0
                self.show_image()
                self.prev_button.setEnabled(False)
                self.next_button.setEnabled(len(self.current_image_paths) > 1)

    def show_image(self) -> None:
        """
        Показывает текущее изображение
        с индексом current_index в элементе image_place
        :return:
        """
        if 0 <= self.current_index < len(self.current_image_paths):
            image_path = self.current_image_paths[self.current_index].split("   ")[0]
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                self.image_place.setText(f"Не удалось загрузить изображение: {image_path}")
            else:
                self.image_place.setPixmap(pixmap.scaled(self.image_place.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.image_place.setText("Изображение отсутствует")

    def show_next_image(self) -> None:
        """
        если не выходит за пределы current_image_paths
        увеличивает значение current_index на 1 и снова
        вызывает функцию show_image
        :return:
        """
        if self.current_index < len(self.current_image_paths) - 1:
            self.current_index += 1
            self.show_image()
            self.prev_button.setEnabled(True)
            if self.current_index == len(self.current_image_paths) - 1:
                self.next_button.setEnabled(False)

    def show_previous_image(self) -> None:
        """
        если не выходит за пределы current_image_paths
        уменьшает значение current_index на 1 и снова
        вызывает функцию show_image
        :return:
        """
        if self.current_index > 0:
            self.current_index -= 1
            self.show_image()
            self.next_button.setEnabled(True)
            if self.current_index == 0:
                self.prev_button.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())


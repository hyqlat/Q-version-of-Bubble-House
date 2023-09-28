from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt

class MyWindos(QMainWindow):
    def __init__(self, player_list, map_class, opt):
        super().__init__()

        #保存元素，后续操作用
        self.player_list = player_list
        self.gmap_class = map_class

        self.array = map_class.gmap
        self.opt = opt

        self.rowelem_size = self.opt.win_height // map_class.gmap.shape[0]
        self.colelem_size = self.opt.win_width // map_class.gmap.shape[1]

        #初始化图形
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('AT')
        self.setGeometry(100, 100, self.opt.win_height, self.opt.win_width)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.image_label = QLabel()
        layout.addWidget(self.image_label)

        # 绘制图形
        self.drawShapes()

    def drawShapes(self):
        pixmap = QPixmap(self.opt.win_height, self.opt.win_width)
        pixmap.fill(Qt.white)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        for y in range(len(self.array)):
            for x in range(len(self.array[y])):
                if self.array[y][x] == 0:
                    painter.setBrush(QColor(255, 0, 0))
                    painter.drawEllipse(x * self.rowelem_size, y * self.colelem_size, self.rowelem_size, self.colelem_size)
                elif self.array[y][x] == 1:
                    painter.setBrush(QColor(0, 0, 255))  
                    painter.drawRect(x * self.rowelem_size, y * self.colelem_size, self.rowelem_size, self.colelem_size)

        painter.end()

        self.image_label.setPixmap(pixmap)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.player_list[0].move(self.gmap_class.gmap, 'left')
            print("左箭头被按下")
        elif event.key() == Qt.Key_Right:
            self.player_list[0].move(self.gmap_class.gmap, 'right')
            print("右箭头被按下")
        elif event.key() == Qt.Key_Up:
            self.player_list[0].move(self.gmap_class.gmap, 'up')
            print("上箭头被按下")
        elif event.key() == Qt.Key_Down:
            self.player_list[0].move(self.gmap_class.gmap, 'down')
            print("下箭头被按下")


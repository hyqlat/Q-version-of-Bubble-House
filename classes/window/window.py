from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt
import numpy as np
import copy

import threading
import time

COLOR_LIST = {
    'border': QColor(255,0,0),
    'path': QColor(0,0,255),
    'setboom': QColor(128,128,12),
    'player0': QColor(0,255,0),
    'player1': QColor(128,255,0),
    'booming': QColor(128,128,128)
}

##临界区锁
lock_changecolor = threading.Lock()


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

        self.pixmap = QPixmap(self.opt.win_height, self.opt.win_width)
        # layout.addWidget(QWidget(self))

        self.image_label = QLabel()
        layout.addWidget(self.image_label)

        # 绘制图形
        self.drawShapes()

        self.setFocusPolicy(Qt.StrongFocus)

    def drawShapes(self):
        
        self.pixmap.fill(Qt.white)

        painter = QPainter(self.pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        for x in range(self.opt.col_num):
            for y in range(self.opt.row_num):
                if self.array[y][x] == 0:
                    painter.setBrush(COLOR_LIST['border'])
                    painter.drawEllipse(x * self.colelem_size, y * self.rowelem_size, self.colelem_size, self.rowelem_size)
                elif self.array[y][x] == 1:
                    painter.setBrush(COLOR_LIST['path'])  
                    painter.drawRect(x * self.colelem_size, y * self.rowelem_size, self.colelem_size, self.rowelem_size)
        
        #设置初始p位置
        painter.setBrush(COLOR_LIST['player{}'.format(0)])  
        painter.drawRect(self.player_list[0].position[1] * self.colelem_size, self.player_list[0].position[0] * self.rowelem_size, self.colelem_size, self.rowelem_size)


        painter.end()

        self.image_label.setPixmap(self.pixmap)


    def kb_move_player(self, pid, cmd):
        ori_posi = self.player_list[pid].move(self.gmap_class.gmap, cmd)
        if ori_posi is not None:
            self.change_posicolor(ori_posi, COLOR_LIST['path'])#改旧位置颜色
            self.change_posicolor(self.player_list[0].position, COLOR_LIST['player{}'.format(pid)])#改新位置颜色


    def kb_useweapon(self, pid, weap, posi, dire, exp_dist):
        # weap, posi, dire, exp_dist = self.player_list[pid].weapon, self.player_list[pid].position, self.player_list[pid].direction, self.player_list[pid].expand_dist
        if weap == 'boom':
            self.weap_boom(posi, pid, exp_dist) 
        else:
            pass
    
    def booming_color(self, posi, expand_dist, color):
        rec_boom_posi = [[posi[0], posi[1]]]#
        offset = np.array([-1,0,0], dtype=np.int32)
        for j in range(expand_dist):
            coor1 = posi + (j+1) * offset
            if (coor1[0] > 0) and (self.gmap_class.gmap[coor1[0], coor1[1]] == 1):
                self.change_posicolor(coor1, color)
                rec_boom_posi.append([coor1[0], coor1[1]])

        offset = np.array([1,0,0], dtype=np.int32)
        for j in range(expand_dist):
            coor1 = posi + (j+1) * offset
            if (coor1[0] < (self.gmap_class.gmap.shape[0]-1)) and (self.gmap_class.gmap[coor1[0], coor1[1]] == 1):
                self.change_posicolor(coor1, color)
                rec_boom_posi.append([coor1[0], coor1[1]])

        offset = np.array([0,-1,0], dtype=np.int32)
        for j in range(expand_dist):
            coor1 = posi + (j+1) * offset
            if (coor1[1] > 0) and (self.gmap_class.gmap[coor1[0], coor1[1]] == 1):
                self.change_posicolor(coor1, color)
                rec_boom_posi.append([coor1[0], coor1[1]])

        offset = np.array([0,1,0], dtype=np.int32)
        for j in range(expand_dist):
            coor1 = posi + (j+1) * offset
            if (coor1[1] < (self.gmap_class.gmap.shape[1]-1)) and (self.gmap_class.gmap[coor1[0], coor1[1]] == 1):
                self.change_posicolor(coor1, color)
                rec_boom_posi.append([coor1[0], coor1[1]])

        return rec_boom_posi


    def weap_boom(self, posi, pid, expand_dist):
        self.change_posicolor(posi, COLOR_LIST['setboom'])#中心点放置炸弹
        time.sleep(1)
        rec_boom_posi = self.booming_color(posi, expand_dist, COLOR_LIST['booming'])#爆
        # print('boom!!!!', posi)
        time.sleep(0.5)

        
        for posi_recover in rec_boom_posi:#不能删玩家在的颜色啊，线程通信 TODO:必须原子操作
            ##临界区
            self.change_posicolor(posi_recover, COLOR_LIST['path'])
            ##

        # self.booming_color(posi, expand_dist, COLOR_LIST['path'])#恢复原来路径
        # time.sleep(1)
        # self.change_posicolor(posi, COLOR_LIST['player{}'.format(pid)])
        


    def keyPressEvent(self, event):
        
        if (event.key() == Qt.Key_Left) or (event.key() == Qt.Key_Right) or (event.key() == Qt.Key_Up) or (event.key() == Qt.Key_Down):
            if event.key() == Qt.Key_Left:
                cmd = 'left'
                # self.kb_move_player(0, cmd)
                
            elif event.key() == Qt.Key_Right:
                cmd = 'right'
                # self.kb_move_player(0, cmd)
            elif event.key() == Qt.Key_Up:
                cmd = 'up'            
                # self.kb_move_player(0, cmd)
            elif event.key() == Qt.Key_Down:
                cmd = 'down'
                # self.kb_move_player(0, cmd)

            t1 = threading.Thread(target=self.kb_move_player, kwargs={'pid':0, 'cmd':cmd})
            t1.start()
            t1.join()

            # self.kb_move_player(pid=0, cmd=cmd)


        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            weap, posi, dire, exp_dist = self.player_list[0].weapon, self.player_list[0].position, self.player_list[0].direction, self.player_list[0].expand_dist#得在线程开始前捕获这些值，否则会被修改
            t2 = threading.Thread(target=self.kb_useweapon, kwargs={'pid':0, 'weap':copy.deepcopy(weap), 'posi':copy.deepcopy(posi), 'dire':copy.deepcopy(dire), 'exp_dist':copy.deepcopy(exp_dist)})#注意要用深拷贝
            t2.start()
            # t2.join()

            # self.kb_useweapon(pid=0)
            
        
        
        
            
            

    def change_posicolor(self, posi, color):
        '''
        posi:[x y]
        '''
        painter = QPainter(self.pixmap)
        painter.setRenderHint(QPainter.Antialiasing)        
        painter.setBrush(color)
        #print('ss', posi)
        painter.drawRect(posi[1] * self.colelem_size, posi[0] * self.rowelem_size, self.colelem_size, self.rowelem_size)
        painter.end()
        self.image_label.setPixmap(self.pixmap)

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

from classes.map.map import Map
from classes.player.player import Player
from utils.opt import Options

from classes.window.window import MyWindos

def make_player_list():
    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    

    opt = Options().parse()
    p1 = Player()
    gmap_class = Map(opt)
    
    p1.print_state()

    player_list = [p1]

    wd_control = MyWindos(
        player_list=player_list, 
        map_class=gmap_class,
        opt=opt
    )

    wd_control.show()

    sys.exit(app.exec_())

    
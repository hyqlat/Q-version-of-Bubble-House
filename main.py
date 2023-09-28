from classes.map.map import Map
from classes.player.player import Player
from utils.opt import Options


if __name__ == '__main__':
    opt = Options().parse()
    p1 = Player()
    gmap = Map(opt)
    
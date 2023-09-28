from classes.map.map import Map
from classes.player.player import Player
from utils.opt import Options


if __name__ == '__main__':
    opt = Options().parse()
    p1 = Player()
    gmap = Map(opt)
    p1.print_state()

    while(True):
        try:
            u_input = input('输入操作')
            print('操作是', u_input)
        except ValueError:
            print('无效输入')

        if u_input == 'quit':
            break
        p1.move(gmap, u_input)
        p1.print_state()

        

    
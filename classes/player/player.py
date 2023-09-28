import numpy as np

class Player:
    def __init__(self) -> None:
        '''
        自身属性
        1.坐标
        2.hp
        3.weapon
        4.direction
        '''
        self.position = np.array([1,1,0], dtype=np.int32)#x y z    z之后可能有用
        self.hp = 0
        self.weapon = None
        self.direction = 0 #0:上；  1：右；  2：下； 3：左

        
        pass

    def print_state(self,):
        print('------------------------')
        print('|当前位置：{}|'.format(self.position))
        print('|当前方向：{}|'.format(self.direction))
        print('------------------------')

    
    #move
    def move(self, map, cmd):
        if cmd == 'up':
            if (self.position[0]-1 >= 0) and (map[self.position[0]-1, self.position[1]] != 0):
                self.up()
        elif cmd == 'down':
            if (self.position[0]+1 < map.shape[0]) and (map[self.position[0]+1, self.position[1]] != 0):
                self.down()
        elif cmd == 'left':
            if (self.position[1]-1 >= 0) and (map[self.position[0], self.position[1]-1] != 0):
                self.left()
        elif cmd == 'right':
            if (self.position[1]+1 < map.shape[1]) and (map[self.position[0], self.position[1]+1] != 0):
                self.right()
        else:
            print("unkonwn cmd!")
        self.print_state()

    def up(self,):
        self.position[0] -= 1
        self.direction = 0
    
    def down(self,):
        self.position[0] += 1
        self.direction = 2
    
    def left(self,):
        self.position[1] -= 1
        self.direction = 3

    def right(self,):
        self.position[1] += 1
        self.direction = 1


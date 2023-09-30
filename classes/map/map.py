import numpy as np

'''
   -------> y  
   |
   |
x  v

'''


'''
0:地图禁区
1:普通道路
2:炸弹
3:booming


10:玩家1
11:玩家2
'''

class Map:
    def __init__(self, opt) -> None:
        '''
        构建图
        '''
        self.opt = opt
        self.make_map()#感觉之后还是得从文件读入map
        pass


    def make_map(self,):
        '''
        可走设1,不可走设0
        '''
        self.gmap = np.zeros((self.opt.row_num, self.opt.col_num), dtype=np.int32)

        #边界外设1
        self.gmap[1:self.opt.row_num-1,1:self.opt.col_num-1] = 1

        print(self.gmap)

    def make_mapfromfile(self):
        pass

    def set_posi_map(self, posi, obj):
        self.gmap[posi[0], posi[1]] = obj

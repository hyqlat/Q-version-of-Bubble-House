#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
from pprint import pprint
from utils import log
import sys


class Options:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.opt = None

    def _initial(self):
        # ===============================================================
        #                     General options
        # ===============================================================
        self.parser.add_argument('--cuda_idx', type=str, default='cuda:0', help='cuda idx')
        self.parser.add_argument('--map_dir', type=str,
                                 default='/media/mtz/076f660b-b7de-4646-833c-0b7466f35185/data_set/h3.6m/dataset/',
                                 help='path to dataset')
        self.parser.add_argument('--row_num', type=int, default=32, help='map row number')
        self.parser.add_argument('--col_num', type=int, default=32, help='map col number')


    def _print(self):
        print("\n==================Options=================")
        pprint(vars(self.opt), indent=4)
        print("==========================================\n")

    def parse(self):
        self._initial()
        self.opt = self.parser.parse_args()        
        self._print()
        # log.save_options(self.opt)
        return self.opt



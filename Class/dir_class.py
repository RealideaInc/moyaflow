import os
from .. import moyaflow as mf


class dir_class:

    def make_dir(self, PATH):
        if not os.path.exists(PATH):
            print('【 Notice 】Create an {} directory.'.format(PATH))
            os.makedirs(PATH)

    def make_tree_dir(self):
        self.make_dir(mf.BASE_OUTPUT_PATH + '/test/images')
        self.make_dir(mf.BASE_OUTPUT_PATH + '/test/labels')
        self.make_dir(mf.BASE_OUTPUT_PATH + '/train/images')
        self.make_dir(mf.BASE_OUTPUT_PATH + '/train/labels')
        self.make_dir(mf.BASE_OUTPUT_PATH + '/valid/images')
        self.make_dir(mf.BASE_OUTPUT_PATH + '/valid/labels')

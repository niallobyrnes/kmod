
#!/usr/bin/env python

import os
import unittest

from kmod import BaseModule
from load_yaml import LoadYaml




class testKMod(unittest.TestCase):

    def setUp(self):
        os.environ[LoadYaml.ROOT] = '../test_yaml'
        self.m = BaseModule()
        


    def test_call_argv(self):
    	argv = [1,2,3,4]
    	self.m = Kmod()
    	argv = []
    	self.m = Kmod()


if __name__ == '__main__':
    unittest.main()




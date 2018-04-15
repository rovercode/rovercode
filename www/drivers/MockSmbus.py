''' A mock smbus object for use when not on target hardware'''

from random import randint

class MockSmbus():

    def write_byte_data(self, *args, **kwargs):
        print "Writing byte data with args {} {}".format(str(args), str(kwargs))

    def read_i2c_block_data(self, addr, reg, how_many):
        return [randint(0, 255)] * how_many
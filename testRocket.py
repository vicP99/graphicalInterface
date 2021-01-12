from rocket_module import rocket
from rocket_module import read
from rocket_module  import notARocket
from GUI import Interface
import unittest
import numpy as np


class test_readRocket(unittest.TestCase):
    def test_result(self):
        result = read("Ariane 5").Height
        self.assertEqual(result,52.0) #see if we read the good value
    def test_badInput(self):
        self.assertRaises(notARocket,read,"ImNotARocket") #test to contole the netry

class test_output_trajectory(unittest.TestCase):

    def test_earth_is_not_gas(self): #test if the rocket does not go inside earth
        Dt=0.0001
        my_rocket=read("Falcon 9")
        X,Z,G,A,T,K=rocket.trajectory(my_rocket,np.pi/4,Dt)
        self.assertTrue(Z[-2]>0,"la fusée est dans la terre") #we test if the rocket is not in the earth 
        self.assertTrue(100-Z[-2]>0)#also test if the last position is near the ground (100m precision)


if __name__ == '__main__':
    unittest.main()

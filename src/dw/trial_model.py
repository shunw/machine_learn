import numpy as np
import functools

'''
test Markov Chain
'''

custom_next_P = np.array([[.8,.1, .1], [.5, .1, .4], [.5, .3, .2]])
ini_status = np.array([.2,.4, .4])
custom_next_4 = functools.reduce(np.dot, [custom_next_P, custom_next_P, custom_next_P, custom_next_P])
p4 = np.dot(ini_status, custom_next_4)
print (p4)
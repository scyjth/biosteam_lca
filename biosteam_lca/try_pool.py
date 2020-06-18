# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 22:01:24 2019

@author: cyshi
"""



from multiprocessing import Pool
from os import getpid, fork
#
#def double(i):
#    print("I'm process", getpid())
#    return i * 2
#
#if __name__ == '__main__':
#    with Pool() as pool:
#        result = pool.map(double, [1, 2, 3, 4, 5])
#        print(result)


print("I am parent process", getpid())
if fork():
    print("I am the parent process, with PID", getpid())
else:
    print("I am the child process, with PID", getpid())
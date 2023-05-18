#!/usr/bin/env python3
"""
The script that runs the module script.
"""

import module

__author__ = 'Mariah Holder'
__version__ = 'Spring 2022'
__pylint__ = 'v.2.12.2'

ALPHA = 0.1
GAMMA = 0.9
EPSILON = 0.1

def main():
    '''
	The entry method to the program.
	'''
    learning_episodes = input("Enter number of learning episodes:")
    q_learner = module.QLearner(ALPHA, GAMMA, EPSILON)
    q_learner.learn(learning_episodes)
	
if __name__ == '__main__':
    main()

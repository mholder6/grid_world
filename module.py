#!/usr/bin/env python3
"""
The module that defines functionality for creating
a Q-Table for a specified grid world.
"""

import numpy
import sys
import pprint

__author__ = 'Mariah Holder'
__version__ = 'Spring 2022'
__pylint__ = 'v.2.12.2'

GRID_WORLD = list(range(1,51))

class QLearner:

    def __init__(self, alpha, gamma, epsilon):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def learn(self, learning_episodes):
        q_values = q_table()
        path = []
        for episode in range(int(learning_episodes)):
            state = 31
            learning = True
            while learning:
                path.append(state)
                action = greedy_policy(q_values, state, self.epsilon)
                #print(action)
                next_state = calculate_next_state(state, action[1])
                #print(next_state)
                reward = get_state_reward(state)[0]
                learning = get_state_reward(state)[1]
                
                maximum_future_state_action = _best_action(q_values, next_state)
                
                difference_target = reward + self.gamma * q_values[maximum_future_state_action]
                difference_error = difference_target - q_values[(state, action[1])]
                q_values[(state, action[1])] += self.alpha * difference_error
                state = next_state
            print(_list_to_string(path))

def get_state_reward(state):
    """
    Returns a tuple of the reward of the specified state,
    and True if the State is not terminating, False otherwise
    """
    cliff_states = [24, 34, 44]
    red_states = [6, 7, 14, 25, 26, 28, 38, 42, 48]
    blue_state = 13
    winning_state = 10
    if state in cliff_states:
        return (-100, False)
    if state in red_states:
        return (-10, True)
    if state == blue_state:
        return (25, True)
    if state == winning_state:
        return (1500, False)
    return (0, True)

def calculate_next_state(state, action):
    if action == 'West':
        return state - 1
    if action == 'East':
        return state + 1
    if action == 'North':
        return state - 10
    return state + 10

def get_state_actions(state):
    """
    Returns a list with the specified state's possible next
    state action pairs, with a maximum of 4 pairs.
    """
    possible = list(tuple())
    if not (state - 1) % 10 == 0:
        possible.append((state, 'West'))
    if state > 10:
        possible.append((state, 'North'))
    if not state % 10 == 0:
        possible.append((state, 'East'))
    if state < 40:
        possible.append((state, 'South'))
    
    return possible

def greedy_policy(q_values, state, epsilon):
    if numpy.random.random() < epsilon:
        random_index = numpy.random.choice(len(get_state_actions(state)))
        return get_state_actions(state)[random_index]
    return _best_action(q_values, state)

def _best_action(q_values, state):
    best_action_value = -1000000
    best_state_action = (state, "")
    
    possible_best = get_state_actions(state)
    for state_action in possible_best:
        if q_values[state_action] >= best_action_value:
            best_action_value = q_values[state_action]
            best_state_action = state_action
            
    if best_action_value == 0:
        random_index = numpy.random.choice(len(possible_best))
        best_action_value = (state, possible_best[random_index])
    return (state, best_state_action[1])

def _determine_action(state, new_state):
    if new_state - state == 1:
        return 'West'
    if state - new_state == 1:
        return 'East'
    if new_state - state == 10:
        return 'South'
    return 'North'

def q_table():
    state = 1
    table = {}

    while state in GRID_WORLD:
        possible_actions = get_state_actions(state)
        for action in possible_actions:
            table[(action)] = 0.0
        state = state + 1 
    return table

def _list_to_string(int_list):
    string_list = []
    for integer in int_list:
        string_list.append(str(integer))
        
    return ','.join(string_list) + '.' + '\r\n'

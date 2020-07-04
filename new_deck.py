#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 20:13:25 2020

@author: chaffee
"""
import random
import numpy as np

card_back = 'card_pics/blue_back_3.jpg'
# suits with just the initials
suits = ['S', 'C', 'H', 'D']


# denominations
card_values = [str(s) for s in list(np.arange(2, 11))]
face_cards = ['J', 'Q', 'K', 'A']
card_values.extend(face_cards)


#deck = []
        
# now join them to make a deck of cards!
def make_deck(shuffle = True):
    deck = []
    '''deck should be an empty list'''
    for value in card_values:
        for suit in suits:
            deck.append(value + suit)
    if shuffle:
        random.shuffle(deck)
    return deck
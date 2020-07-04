#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 01:23:55 2020

@author: chaffee
"""

from card_to_path import get_img_path
import new_deck

hands = {}
card_back = new_deck.card_back
card_plc_holder_imgs = ['card_pics/card_place_holder_img.png',
                        'card_pics/card_place_holder_img2_sm2.png',
                        'card_pics/card_place_holder_img3.jpg',
                        'card_pics/card_place_holder_img4_test4.png']
cd_plc_holder_img = card_plc_holder_imgs[3]
stage = []

def new_game(players):
    global deck 
    # generate a new, shuffled deck    
    deck = new_deck.make_deck()
    
    # convert the raw strings in deck to image file paths
    for i in range(len(deck)):
        card = deck[i]
        deck[i] = get_img_path(card)
    players_current_hand = players.copy()
    hands.clear()
    stage.clear()
    for p in players_current_hand:
        hands[p] = [] 
    hands['comm'] = []

def deal(players):
    if len(stage) == 0:
        new_game(players)
        for key in players:
            for i in range(4):
                hands[key].append(deck.pop())
        # sending dict to html requires values be tuples, not lists...
        hands_tuple = hands.copy()
        for key in hands_tuple.keys():
            hands_tuple[key] = tuple(hands[key])
        stage.append('flop')
        return hands_tuple        
    elif stage[0] == 'flop':
        for card in range(3):
            hands['comm'].append(deck.pop())
        hands_tuple = hands.copy()
        for key in hands_tuple.keys():
            hands_tuple[key] = tuple(hands[key])
        stage.pop()
        stage.append('turn')
        return hands_tuple
    elif stage[0] == 'turn':
        hands['comm'].append(deck.pop())
        hands_tuple = hands.copy()
        for key in hands_tuple.keys():
            hands_tuple[key] = tuple(hands[key])
        stage.pop()
        stage.append('river')
        return hands_tuple
    else:
        hands['comm'].append(deck.pop())
        hands_tuple = hands.copy()
        for key in hands_tuple.keys():
            hands_tuple[key] = tuple(hands[key])
        stage.clear()
        return hands_tuple
        
def get_display(hands_tuple, whose_pg):
    display_hands = {}
    # convert fucking tuples back to fucking lists...
    hands_list = hands_tuple.copy()
    for key in hands_list.keys():
        hands_list[key] = list(hands_tuple[key])
    
    # convert card pics to card back pics if 
    # player is not 'whose_pg'
    for key in hands_list.keys():
        cards = hands_list[key]
        if key not in ['comm', whose_pg]:
            cards = [card_back] * 5
        display_hands[key] = cards
    num_comm_cards = len(hands_list['comm'])
    print(f'from omaha.get_display(), num_comm_cards = {num_comm_cards}')
    if num_comm_cards < 5:
        display_hands['comm'].extend([cd_plc_holder_img]*(5-num_comm_cards))
    # convert fucking lists back to fucking tuples...
    for key in display_hands.keys():
        display_hands[key] = tuple(display_hands[key])
    return display_hands

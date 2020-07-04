#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 14:10:22 2020

@author: chaffee
"""

from card_to_path import get_img_path
import new_deck

hands = {}
draw_card_idxs = {}
card_back = new_deck.card_back
card_plc_holder_imgs = ['card_pics/card_place_holder_img.png',
                        'card_pics/card_place_holder_img2_sm2.png',
                        'card_pics/card_place_holder_img3.jpg',
                        'card_pics/card_place_holder_img4_test4.png']
cd_plc_holder_img = card_plc_holder_imgs[3]
stage = []

def new_game(players, community_game = True):
    global deck 
    # generate a new, shuffled deck    
    deck = new_deck.make_deck()
    
    # convert the raw strings in deck to image file paths
    for i in range(len(deck)):
        card = deck[i]
        deck[i] = get_img_path(card)
    
    players_current_hand = players.copy()
    hands.clear()
    draw_card_idxs.clear()
    stage.clear()
    for p in players_current_hand:
        hands[p] = []
    hands['spit'] = []

def deal(players):
    stage_len = len(stage)
    if stage_len == 0:
        new_game(players)
        for key in players:
            if key != 'spit':
                for i in range(5):
                    hands[key].append(deck.pop())
        hands['spit'].append(deck.pop())                
        stage.append('draw')      
        # now have to turn the lists into tuples for sending to url
        hands_tuple = hands.copy()
        for key in hands_tuple.keys():
            hands_tuple[key] = tuple(hands[key])
        return hands_tuple
    else:
        print(f'from spit.deal(players), draw_card_idxs: {draw_card_idxs}')
        for key in players:
            if key in draw_card_idxs.keys():
                for i in range(5):
                    if draw_card_idxs[key][i] == 'discard':
                        hands[key][i] = deck.pop()        
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
    
    # convert card pics to card back pic if 
    # player is not 'whose_pg'
    for key in hands_list.keys():
        cards = hands_list[key]
        if key != whose_pg:
            if key != 'spit':
                cards = [card_back] * 5
            else:
                cards = [card_back]
        display_hands[key] = cards
    # convert fucking lists back to fucking tuples...
    for key in display_hands.keys():
        display_hands[key] = tuple(display_hands[key])
    return display_hands

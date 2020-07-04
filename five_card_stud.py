#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 03:36:23 2020

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

def new_game(players, community_game = False):
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

# very annoying: you can't pass lists of things to the url, you have
# to use tuples. But python tuples are immutable, so have to create
# a new one with every new card dealt.       

def deal(players):
    stage_len = len(stage)
    if stage_len == 0:
        new_game(players)
        print(f'from five_card_stud.deal(), players = {players}, hands = {hands}')
        for p in players:
            for i in range(2):
                hands[p].append(deck.pop())
        stage.append(2)      
        # now have to turn the lists into tuples for sending to url
        hands_tuple = hands.copy()
        for key in hands_tuple.keys():
            hands_tuple[key] = tuple(hands[key])
        return hands_tuple
    else:
        for p in players:
            hands[p].append(deck.pop())
        stage.append(stage[stage_len -1] + 1)
        hands_tuple = hands.copy()
        for key in hands_tuple.keys():
            hands_tuple[key] = tuple(hands[key])
        if stage[stage_len -1] == 4: # dealing again will start a new hand
            stage.clear()
        return hands_tuple
    
# we have players' hands, but we don't want to display all cards
# to all players (of course). So show card backs for hole cards
# as appropriate
def get_display(hands_tuple, whose_pg):
    display_hands = {}
    # convert fucking tuples back to fucking lists...
    hands_list = hands_tuple.copy()
    for key in hands_list.keys():
        hands_list[key] = list(hands_tuple[key])
    
    # convert 1st card pic to card back pic if 
    # player is not 'whose_pg'
    for key in hands_list.keys():
        cards = hands_list[key]
        num_cards = len(cards)
        if key != whose_pg:
            cards[0] = card_back
        if num_cards < 5: # add fancy card place holder graphics 
            cards.extend([cd_plc_holder_img]*(5-num_cards))
        display_hands[key] = cards
    
    # convert fucking lists back to fucking tuples...
    for key in display_hands.keys():
        display_hands[key] = tuple(display_hands[key])
    return display_hands

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 23:08:13 2020

@author: chaffee
"""

from card_to_path import get_img_path
import new_deck
"""
Note: we don\'t use a stage for Monty, because no matter where you
are in the game, dealing just means dealing another round of cards 
exactly the same way each time, or ending the game.

Normally in Monty you leave Monty\'s cards set after dealing the 
first round, but that doesn\'t matter--here we just deal Monty a new
hand along with everybody else. In order to not run out of cards, the
deal() function just calls new_game() every time.  

The complications in Monty (what to do when various numbers of people
stay in) are all handled by the players themselves in the game. There
is always either a choice to deal again or end, depending on who
stays in and what happens in the showdown. Dealing again is just the same 
as starting over, except for the money in the pot, but that too is handled 
by the players in the betting app.
"""


hands = {}
hold_dict = {}
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
        card = deck [i]
        deck[i] = get_img_path(card)
    
    players_current_hand = players.copy()
    hands.clear()
    stage.clear()
    for p in players_current_hand:
        hands[p] = []
        hold_dict[p] = ''
    hands['monty'] = []


def deal(players):
    new_game(players)
    for key in players:
        for i in range(3):
            hands[key].append(deck.pop())
            hands['monty'].append(deck.pop())        
        
        # now have to turn the lists into tuples for sending to url
    hands_tuple = hands.copy()
    for key in hands_tuple.keys():
        hands_tuple[key] = tuple(hands[key])
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
            cards = [card_back] * 3
        display_hands[key] = cards
        if whose_pg in list(hands_list.keys()) and hold_dict[whose_pg] == 'hold': # display the player's own hand
            display_hands[whose_pg] = hands_list[whose_pg]
    # convert fucking lists back to fucking tuples...
    for key in display_hands.keys():
        display_hands[key] = tuple(display_hands[key])
    return display_hands
    

    
    
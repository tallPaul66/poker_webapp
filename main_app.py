from flask import Flask, render_template, request, jsonify, redirect, url_for
import seven_card_stud
import draw
import omaha
import five_card_stud
import monty
import spit

# global variables
players_tonight = []
possible_players = ['player1', 'player2', 'player3', 'player4', 'player5', 'player6']
player_map = {}
# games that require choices on the player's part beyond folding or staying in
choice_games = ['draw', 'monty', 'spit']

# declaring these global variables here so they're available 
# in case someone clicks the New Game button before any hands 
# are dealt for the evening.
cards_player1_pg = {}
cards_player2_pg = {}
cards_player3_pg = {}
cards_player4_pg = {}
cards_player5_pg = {}
cards_player6_pg = {}

app = Flask(__name__)

# app.url_map.strict_slashes = False

@app.route('/', methods=['GET', 'POST'])
def home(): 
    # This method gets called any time someone clicks the submit
    # button on the home pg.    
    
    if request.method == 'POST':
        players_tonight.clear()
        # this is from the checkbox version of the configure page:
        #players_selected = request.form.getlist('players')        
        #players_tonight.extend(players_selected) 
        player_map['player1'] = request.form.get('player1') 
        player_map['player2'] = request.form.get('player2')
        player_map['player3'] = request.form.get('player3')
        player_map['player4'] = request.form.get('player4')
        player_map['player5'] = request.form.get('player5')
        player_map['player6'] = request.form.get('player6')
        for key in player_map.keys():
            if player_map[key] != '':
                players_tonight.append(key)

        print('Using the text box entries:')
        print(f'from home(): form submitted, players set for tonight: {players_tonight}')
        print(player_map)
        
        ''' we do the below regardless of who is playing tonight. That way, if someone
        is later removed from the night's lineup, when someone calls get_img()
        that someone's cards will be blank, no matter what is going on in the
        game or what stage things are at. I.e., this resets the now-missing
        player's cards to null, which would not have happened if you simply
        remove the player from the lineup (unless everyone clicks New Game).'''
        #FIXIT:
        # when starting a new session, clicking "UPDATE CARDS" doesn't do anything,
        # i.e., doesn't update to blank, showing cards still from previous session
        
        for p in possible_players:
            cards_player1_pg[p] = ()
            cards_player2_pg[p] = ()
            cards_player3_pg[p] = ()
            cards_player4_pg[p] = ()
            cards_player5_pg[p] = ()
            cards_player6_pg[p] = ()

    return render_template('home.html')

#~~~~~~~~~~~~~~ 7-card stud ~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/seven_card', methods = ['GET', 'POST'])
def seven_card_play():
    if request.method == 'POST':
        print('\nfrom seven_card_play(): request.form is',  {request.form})
        if request.form['btn'] ==  'D E A L': 
            deal_click()
        elif request.form['btn'] == 'FOLDY-DOLDY':
            fold_hand()
        elif request.form['btn'] == 'REVEAL':
            reveal_cards()
        elif request.form['btn'] == 'NEW GAME':
            start_new_game()
    elif request.method == 'GET':
        print('\nyou just triggered a GET request which was detected in seven_card_play()')      
    return render_template('seven_card.html', names = player_map)

@app.route('/link_to_seven_card')
def redirect_to_seven_card():
     http_ref = request.environ['HTTP_REFERER']
     requesting_player = http_ref[http_ref.find('player=')+7:]
     print(f'msg from redirect_to_seven_card(): requesting_player is {requesting_player}')
     # starts a new game if ANYONE clicks a link to another game at any time
     # so folks should only click game links when a current game has ended
     start_new_game()
     return redirect(url_for('seven_card_play', player=requesting_player))

#~~~~~~~~~~~~~~ draw poker ~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/draw', methods = ['GET', 'POST'])
def draw_play():
    if request.method == 'POST':
        print('\nfrom draw_play(): request.form is',  {request.form})
        if request.form['btn'] ==  'D E A L': 
            deal_click()
        elif request.form['btn'] == 'FOLDY-DOLDY':
            fold_hand()
        elif request.form['btn'] == 'REVEAL':
            reveal_cards()
        elif request.form['btn'] == 'Draw':
            draw_cards()  
        elif request.form['btn'] == 'NEW GAME':
            start_new_game() 
    elif request.method == 'GET':
        print('\nyou just triggered a GET request which was detected in draw_play()') 
    return render_template('draw.html', names = player_map)

@app.route('/link_to_draw')
def redirect_to_draw():
    http_ref = request.environ['HTTP_REFERER']
    requesting_player = http_ref[http_ref.find('player=')+7:]
    print(f'msg from link_to_draw(): requesting_player is {requesting_player}')
    # starts a new game if ANYONE clicks a link to another game at any time
    # so folks should only click game links when a current game has ended
    start_new_game()
    return redirect(url_for('draw_play', player=requesting_player))

# special function for the game of draw poker to register discards for each
# player
def draw_cards():
    print('\nfrom draw_cards() fn:')
    http_ref = request.environ['HTTP_REFERER']
    requesting_player = http_ref[http_ref.find('player=')+7:]
    print(f' request.environ["HTTP_REFERER] is: {http_ref}')
    print(f'requesting_player is: {requesting_player}')
    card_statuses = [request.form['card1'], request.form['card2'], request.form['card3'], 
                  request.form['card4'], request.form['card5']]
    print('here are the card stats:')
    for s in card_statuses:
        print(s)
    draw.draw_card_idxs[requesting_player] = card_statuses


#~~~~~~~~~~~~~~ Omaha ~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/omaha', methods = ['GET', 'POST'])
def omaha_play():
    if request.method == 'POST':
        print('\nfrom omaha_play(): request.form is',  {request.form})
        if request.form['btn'] ==  'D E A L': 
            deal_click()
        elif request.form['btn'] == 'FOLDY-DOLDY':
            fold_hand()
        elif request.form['btn'] == 'REVEAL':
            reveal_cards()
        elif request.form['btn'] == 'Draw':
            draw_cards()         
        elif request.form['btn'] == 'NEW GAME':
            start_new_game() 
    elif request.method == 'GET':
        print('\nyou just triggered a GET request which was detected in omaha_play()') 
    return render_template('omaha.html', names = player_map)

@app.route('/link_to_omaha')
def redirect_to_omaha():
    http_ref = request.environ['HTTP_REFERER']
    requesting_player = http_ref[http_ref.find('player=')+7:]
    print(f'msg from link_to_omaha(): requesting_player is {requesting_player}')
    # starts a new game if ANYONE clicks a link to another game at any time
    # so folks should only click game links when a current game has ended
    start_new_game()
    return redirect(url_for('omaha_play', player=requesting_player))

#~~~~~~~~~~~~~~ FIVE-CARD STUD ~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/five_card_stud', methods = ['GET', 'POST'])
def five_card_play():    
    if request.method == 'POST':
        if request.form['btn'] ==  'D E A L': 
            print(f'from five_card_play(), cards_player1_pg = {cards_player1_pg}')
            deal_click()
        elif request.form['btn'] == 'FOLDY-DOLDY':
            fold_hand()
        elif request.form['btn'] == 'REVEAL':
            reveal_cards()
        elif request.form['btn'] == 'NEW GAME':
            start_new_game()
    elif request.method == 'GET':
        print('\nyou just triggered a GET request which was detected in five_card_play()') 
    return render_template('five_card_stud.html', names = player_map)

@app.route('/link_to_five_card_stud')
def redirect_to_five_card_stud():
    http_ref = request.environ['HTTP_REFERER']
    requesting_player = http_ref[http_ref.find('player=')+7:]
    print(f'msg from link_to_five_card_stud(): requesting_player is {requesting_player}')
    # starts a new game if ANYONE clicks a link to another game at any time
    # so folks should only click game links when a current game has ended
    start_new_game()
    return redirect(url_for('five_card_play', player=requesting_player))

#~~~~~~~~~~~~~~~~~~~ MONTY ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/monty', methods = ['GET', 'POST'])
def monty_play():   
    global reveal_players_monty
    if request.method == 'POST':
        if request.form['btn'] ==  'D E A L':
            reveal_players_monty = 0
            deal_click()
        # Monty has no "fold" option
        #elif request.form['btn'] == 'FOLDY-DOLDY': 
            #fold_hand()
        elif request.form['btn'] == 'REVEAL':
            reveal_cards()
        elif request.form['btn'] == 'HOLD':
            monty_hold()
        elif request.form['btn'] == 'REVEAL MONTY':
            reveal_monty()
        elif request.form['btn'] == 'NEW GAME':
            start_new_game()
    elif request.method == 'GET':
        print('\nyou just triggered a GET request which was detected in five_card_play()') 
    return render_template('monty.html', names = player_map)

@app.route('/link_to_monty')
def redirect_to_monty():
    http_ref = request.environ['HTTP_REFERER']
    requesting_player = http_ref[http_ref.find('player=')+7:]
    print(f'msg from link_to_monty(): requesting_player is {requesting_player}')
    # starts a new game if ANYONE clicks a link to another game at any time
    # so folks should only click game links when a current game has ended
    start_new_game()
    return redirect(url_for('monty_play', player=requesting_player))

def monty_hold():
    print('\nfrom monty_hold() fn:')
    http_ref = request.environ['HTTP_REFERER']
    requesting_player = http_ref[http_ref.find('player=')+7:]
    print(f' request.environ["HTTP_REFERER] is: {http_ref}')
    print(f'requesting_player {requesting_player} wants to hold.')
    monty.hold_dict[requesting_player] = 'hold'  
  
def reveal_monty():
    print('\nfrom reveal_monty() fn:')
    cards_player1_pg['monty'] = hands['monty']
    cards_player2_pg['monty'] = hands['monty']
    cards_player3_pg['monty'] = hands['monty']
    cards_player4_pg['monty'] = hands['monty']
    cards_player5_pg['monty'] = hands['monty']
    cards_player6_pg['monty'] = hands['monty']

#~~~~~~~~~~~~~~ spit in the ocean ~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/spit', methods = ['GET', 'POST'])
def spit_play():
    if request.method == 'POST':
        print('\nfrom draw_play(): request.form is',  {request.form})
        if request.form['btn'] ==  'D E A L': 
            deal_click()
        elif request.form['btn'] == 'FOLDY-DOLDY':
            fold_hand()
        elif request.form['btn'] == 'REVEAL':
            reveal_cards()
        elif request.form['btn'] == 'REVEAL SPIT':
            reveal_spit()
        elif request.form['btn'] == 'Draw':
            draw_spit_cards()  
        elif request.form['btn'] == 'NEW GAME':
            start_new_game() 
    elif request.method == 'GET':
        print('\nyou just triggered a GET request which was detected in spit_play()') 
    return render_template('spit_in_the_ocean.html', names = player_map)

@app.route('/link_to_spit')
def redirect_to_spit():
    http_ref = request.environ['HTTP_REFERER']
    requesting_player = http_ref[http_ref.find('player=')+7:]
    print(f'msg from link_to_spit(): requesting_player is {requesting_player}')
    # starts a new game if ANYONE clicks a link to another game at any time
    # so folks should only click game links when a current game has ended
    start_new_game()
    return redirect(url_for('spit_play', player=requesting_player))

# special function for the games of draw poker spit-in-the-ocean to register 
# discards for each player
def draw_spit_cards():
    print('\nfrom draw_spit_cards() fn:')
    http_ref = request.environ['HTTP_REFERER']
    requesting_player = http_ref[http_ref.find('player=')+7:]
    print(f' request.environ["HTTP_REFERER] is: {http_ref}')
    print(f'requesting_player is: {requesting_player}')
    card_statuses = [request.form['card1'], request.form['card2'], request.form['card3'], 
                  request.form['card4'], request.form['card5']]
    print('here are the card stats:')
    for s in card_statuses:
        print(s)
    spit.draw_card_idxs[requesting_player] = card_statuses
    
def reveal_spit():
    print('\nfrom reveal_spit() fn:')
    cards_player1_pg['spit'] = hands['spit']
    cards_player2_pg['spit'] = hands['spit']
    cards_player3_pg['spit'] = hands['spit']
    cards_player4_pg['spit'] = hands['spit']
    cards_player5_pg['spit'] = hands['spit']
    cards_player6_pg['spit'] = hands['spit']
#~~~~~~~~~~~~~~ General Poker Functions ~~~~~~~~~~~~~~~~~~~~~~~~~
# Function for dealing the next round of cards in a game.
def deal_click():
    global hands
    global players_active    
    http_ref = request.environ['HTTP_REFERER']
    
    if 'five_card_stud' in http_ref:
        print(f'\n from deal_click(), game is 5-card stud, five_card_stud.stage = {five_card_stud.stage}')
        if len(five_card_stud.stage) == 0: # re-activate all tonight's players
            players_active = players_tonight.copy()
        hands = five_card_stud.deal(players_active)
        a_pg_tmp = five_card_stud.get_display(hands, 'player1')
        b_pg_tmp = five_card_stud.get_display(hands, 'player2')
        k_pg_tmp = five_card_stud.get_display(hands, 'player3')
        p_pg_tmp = five_card_stud.get_display(hands, 'player4')
        s_pg_tmp = five_card_stud.get_display(hands, 'player5')
        g_pg_tmp = five_card_stud.get_display(hands, 'player6')
    elif 'seven_card' in http_ref:
        print(f'\n from deal_click(), game is 7-card stud, seven_card_stud.stage = {seven_card_stud.stage}')
        if len(seven_card_stud.stage) == 0: # re-activate all tonight's players
            players_active = players_tonight.copy()
        hands = seven_card_stud.deal(players_active)
        a_pg_tmp = seven_card_stud.get_display(hands, 'player1')
        b_pg_tmp = seven_card_stud.get_display(hands, 'player2')
        k_pg_tmp = seven_card_stud.get_display(hands, 'player3')
        p_pg_tmp = seven_card_stud.get_display(hands, 'player4')
        s_pg_tmp = seven_card_stud.get_display(hands, 'player5')
        g_pg_tmp = seven_card_stud.get_display(hands, 'player6')
    elif 'draw' in http_ref:
        print(f'\n from deal_click(), game is draw poker, draw.stage = {draw.stage}')
        if len(draw.stage) == 0: # re-activate all tonight's players
            players_active = players_tonight.copy()
        hands = draw.deal(players_active)
        a_pg_tmp = draw.get_display(hands, 'player1')
        b_pg_tmp = draw.get_display(hands, 'player2')
        k_pg_tmp = draw.get_display(hands, 'player3')
        p_pg_tmp = draw.get_display(hands, 'player4')
        s_pg_tmp = draw.get_display(hands, 'player5')
        g_pg_tmp = draw.get_display(hands, 'player6')
    elif 'omaha' in http_ref:
        print(f'\n from deal_click(), game is omaha, omaha.stage = {omaha.stage}')
        if len(omaha.stage) == 0: # re-activate all tonight's players
            players_active = players_tonight.copy()
        hands = omaha.deal(players_active)
        a_pg_tmp = omaha.get_display(hands, 'player1')
        b_pg_tmp = omaha.get_display(hands, 'player2')
        k_pg_tmp = omaha.get_display(hands, 'player3')
        p_pg_tmp = omaha.get_display(hands, 'player4')
        s_pg_tmp = omaha.get_display(hands, 'player5')
        g_pg_tmp = omaha.get_display(hands, 'player6')
    elif 'monty' in http_ref:
        print(f'\n from deal_click(), game is monty, monty.stage = {monty.stage}')
        if len(monty.stage) == 0: # re-activate all tonight's players
            players_active = players_tonight.copy()
        hands = monty.deal(players_active)
        a_pg_tmp = monty.get_display(hands, 'player1')
        b_pg_tmp = monty.get_display(hands, 'player2')
        k_pg_tmp = monty.get_display(hands, 'player3')
        p_pg_tmp = monty.get_display(hands, 'player4')
        s_pg_tmp = monty.get_display(hands, 'player5')
        g_pg_tmp = monty.get_display(hands, 'player6')
    elif 'spit' in http_ref:
        print(f'\n from deal_click(), game is spit, spit.stage = {spit.stage}')
        if len(monty.stage) == 0: # re-activate all tonight's players
            players_active = players_tonight.copy()
        hands = spit.deal(players_active)
        a_pg_tmp = spit.get_display(hands, 'player1')
        b_pg_tmp = spit.get_display(hands, 'player2')
        k_pg_tmp = spit.get_display(hands, 'player3')
        p_pg_tmp = spit.get_display(hands, 'player4')
        s_pg_tmp = spit.get_display(hands, 'player5')
        g_pg_tmp = spit.get_display(hands, 'player6')
        
    for key in a_pg_tmp.keys():
        cards_player1_pg[key] = a_pg_tmp[key]
        cards_player2_pg[key] = b_pg_tmp[key]
        cards_player3_pg[key] = k_pg_tmp[key]
        cards_player4_pg[key] = p_pg_tmp[key]
        cards_player5_pg[key] = s_pg_tmp[key]
        cards_player6_pg[key] = g_pg_tmp[key]
        
# Function that displays cards on pages: dynamic in that different
# players will see different pages, depending on the query string in the url
@app.route('/getimage', methods = ['GET'])
def get_img():
    if request.method == 'GET':
        print('\nget_img() is registering a GET request')       
        http_ref = request.environ['HTTP_REFERER']        
        print(f'request.eviron["HTTP_REFERER"]:{http_ref} ')
        requesting_player = http_ref[http_ref.find('player=')+7:] 
        print('requesting_player variable is computed as: ', requesting_player, '\n')
    if requesting_player == 'player1':
        #print('from get_img, cards_player1_pg = ', cards_player1_pg)
        if any([g in http_ref for g in choice_games]): #  'draw' in http_ref or 'monty' in http_ref:
            cards_player1_pg_copy = cards_player1_pg.copy()
            cards_player1_pg_copy['requesting_player'] = cards_player1_pg_copy['player1']
            cards_player1_pg_copy['player1'] = ()
            
            # This part, for Monty, is to display the player's open cards on 
            # his own page in his normal spot on the table (in addition to the 
            # central location where he holds or doesn't hold), so that he can 
            # see more easily that his cards are visible to everyone else
            if 'monty' in http_ref: 
                if monty.hold_dict['player1']  == 'hold':
                    cards_player1_pg_copy['player1'] = hands['player1']
                if reveal_players_monty == 1: # remove player's cards from center on reveal
                    cards_player1_pg_copy['requesting_player'] = ()
            return jsonify(cards_player1_pg_copy)
        else:
            return jsonify(cards_player1_pg)        
    elif requesting_player ==  'player2':
        if any([g in http_ref for g in choice_games]): 
            cards_player2_pg_copy = cards_player2_pg.copy()
            cards_player2_pg_copy['requesting_player'] = cards_player2_pg_copy['player2']
            cards_player2_pg_copy['player2'] = ()
            if 'monty' in http_ref: 
                if monty.hold_dict['player2']  == 'hold':
                    cards_player2_pg_copy['player2'] = hands['player2']
                if reveal_players_monty == 1:
                    cards_player2_pg_copy['requesting_player'] = ()
            return jsonify(cards_player2_pg_copy)
        else:
            return jsonify(cards_player2_pg)
    elif requesting_player == 'player3':
        if any([g in http_ref for g in choice_games]): 
            cards_player3_pg_copy = cards_player3_pg.copy()
            cards_player3_pg_copy['requesting_player'] = cards_player3_pg_copy['player3']
            cards_player3_pg_copy['player3'] = ()
            if 'monty' in http_ref: 
                print(f'from get_img(), reveal_players_monty = {reveal_players_monty}')
                if monty.hold_dict['player3']  == 'hold':
                    cards_player3_pg_copy['player3'] = hands['player3']
                if reveal_players_monty == 1:
                    cards_player3_pg_copy['requesting_player'] = ()
            return jsonify(cards_player3_pg_copy)
        else:
            return jsonify(cards_player3_pg)
    elif requesting_player == 'player4':
        if any([g in http_ref for g in choice_games]): 
            cards_player4_pg_copy = cards_player4_pg.copy()
            cards_player4_pg_copy['requesting_player'] = cards_player4_pg_copy['player4']
            cards_player4_pg_copy['player4'] = ()
            if 'monty' in http_ref: 
                if monty.hold_dict['player4']  == 'hold':
                    cards_player4_pg_copy['player4'] = hands['player4']
                if reveal_players_monty == 1:
                    cards_player4_pg_copy['requesting_player'] = ()
            return jsonify(cards_player4_pg_copy)
        else:
            return jsonify(cards_player4_pg)
    elif requesting_player == 'player5':
        if any([g in http_ref for g in choice_games]): 
            cards_player5_pg_copy = cards_player5_pg.copy()
            cards_player5_pg_copy['requesting_player'] = cards_player5_pg_copy['player5']
            cards_player5_pg_copy['player5'] = ()
            if 'monty' in http_ref: 
                if monty.hold_dict['player5']  == 'hold':
                    cards_player5_pg_copy['player5'] = hands['player5']
                if reveal_players_monty == 1:
                    cards_player5_pg_copy['requesting_player'] = ()
            return jsonify(cards_player5_pg_copy)
        else:
            return jsonify(cards_player5_pg)
    elif requesting_player == 'player6':
        if any([g in http_ref for g in choice_games]): 
            cards_player6_pg_copy = cards_player6_pg.copy()
            cards_player6_pg_copy['requesting_player'] = cards_player6_pg_copy.pop['player6']
            cards_player6_pg_copy['player6'] = ()
            if 'monty' in http_ref: 
                if monty.hold_dict['player6']  == 'hold':
                    cards_player6_pg_copy['player6'] = hands['player6']
                if reveal_players_monty == 1:
                    cards_player6_pg_copy['requesting_player'] = ()
            return jsonify(cards_player6_pg_copy)
        else:
            return jsonify(cards_player6_pg)
    else:
        return None

def start_new_game():
    print('\n start_new_game() has been called.')
    http_ref = request.environ['HTTP_REFERER']
    
    # What game is asking for a new game:
    if 'draw' in http_ref:        
        draw.new_game(players = players_tonight)     
    elif 'five_card_stud' in http_ref:
        five_card_stud.new_game(players = players_tonight)
    elif 'seven_card' in http_ref:
        seven_card_stud.new_game(players = players_tonight)
    elif 'omaha' in http_ref:
        omaha.new_game(players = players_tonight)
    elif 'monty' in http_ref:
        monty.new_game(players = players_tonight)
    elif 'spit' in http_ref:
        spit.new_game(players = players_tonight)
        
    ### Have to clear everybody's cards for display when "Update Cards" is called
    ### It's fine if not all these players are active
    for key in cards_player1_pg.keys():
        cards_player1_pg[key] = ()
        cards_player2_pg[key] = ()
        cards_player3_pg[key] = ()
        cards_player4_pg[key] = ()
        cards_player5_pg[key] = ()
        cards_player6_pg[key] = ()
        
def fold_hand():
    try:
        print(f'\nfrom fold_hand: request.eviron["HTTP_REFERER"]:{request.environ["HTTP_REFERER"]} ')
        http_ref = request.environ['HTTP_REFERER']
        requesting_player = http_ref[http_ref.find('player=')+7:]
        print(f'We thus conclude that {requesting_player} wants to fold, so attempting functionality...')
        hand_len = len(hands[requesting_player])
        seven_card_stud.hands[requesting_player] = [seven_card_stud.card_back] * hand_len
        five_card_stud.hands[requesting_player] = [five_card_stud.card_back] * hand_len
        omaha.hands[requesting_player] = [omaha.card_back] * hand_len
        draw.hands[requesting_player] = [draw.card_back] * hand_len
        spit.hands[requesting_player] = [spit.card_back] * hand_len
        players_active.remove(requesting_player)
        
        cards_player1_pg[requesting_player] = [seven_card_stud.card_back] * hand_len
        cards_player2_pg[requesting_player] = [seven_card_stud.card_back] * hand_len
        cards_player3_pg[requesting_player] = [seven_card_stud.card_back] * hand_len
        cards_player4_pg[requesting_player] = [seven_card_stud.card_back] * hand_len
        cards_player5_pg[requesting_player] = [seven_card_stud.card_back] * hand_len
        cards_player6_pg[requesting_player] = [seven_card_stud.card_back] * hand_len
    except Exception as e:
        print('\nno player parameter (prob w query string?), or player in query string not in active list')
        return '\nno player parameter (maybe no query string), or player in query string not in active list'

def reveal_cards(): 
    global reveal_players_monty
    #try:
    print(f'\nfrom reveal_cards(): request.eviron["HTTP_REFERER"]:{request.environ["HTTP_REFERER"]} ')
    http_ref = request.environ['HTTP_REFERER']
    requesting_player = http_ref[http_ref.find('player=')+7:]
          
        
    # REVEAL in Monty means something different from in the other games:
    # here it is the dealer's right to reveal the cards of everyone 
    # who holds, to everyone playing.
    if 'monty' in http_ref:
        reveal_players_monty = 1 # set the flag, for use in get_img()
        print('"REVEAL" for all holders in Monty has been invoked')
        print(f'contents of monty.hold_dict: {monty.hold_dict}')
        for player in monty.hold_dict.keys(): 
            print(f'value for monty.hold_dict[{player}] is {monty.hold_dict[player]}')
            if monty.hold_dict[player] == 'hold':
                cards_player1_pg[player] = hands[player]
                cards_player2_pg[player] = hands[player]
                cards_player3_pg[player] = hands[player]
                cards_player4_pg[player] = hands[player]
                cards_player5_pg[player] = hands[player]
                cards_player6_pg[player] = hands[player]
            else:
                print(f'{player} does not want to hold')  
        print(f'from reveal_cards(), reveal_players_monty = {reveal_players_monty}')
                    
    else:
        print(f'We thus conclude that {requesting_player} wants to reveal their cards.')
        print(f'here\'s what eveyone should see for {requesting_player}: {hands[requesting_player]}')
        cards_player1_pg[requesting_player] = hands[requesting_player]        
        cards_player2_pg[requesting_player] = hands[requesting_player]
        cards_player3_pg[requesting_player] = hands[requesting_player]
        cards_player4_pg[requesting_player] = hands[requesting_player]
        cards_player5_pg[requesting_player] = hands[requesting_player]
        cards_player6_pg[requesting_player] = hands[requesting_player]
        if requesting_player == 'player1':
            cards_player1_pg['player1'] = hands['player1']
        if requesting_player == 'player2':
            cards_player2_pg['player2'] = hands['player2']
        if requesting_player == 'player3':
            cards_player3_pg['player3'] = hands['player3']
        if requesting_player == 'player4':
            cards_player4_pg['player4'] = hands['player4']
        if requesting_player == 'player5':
            cards_player5_pg['player5'] = hands['player5']
        if requesting_player == 'player6':
            cards_player6_pg['player6'] = hands['player6']
    #except Exception as e:
        #print('\nreveal_cards(): well, something went wrong. Error encountered in try block.')
        
if __name__ == '__main__':
    app.run(debug=True)
    


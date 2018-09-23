from collections import Counter
import os
import pdb

hands_order = ["HC", "OP", "TP", "Th", "F", "S", "FH", "Fo", "SF"]
# no RF really needed as it's just a special case of SF

# Loading the data from the source file
# ############################################
with open("p054_poker.txt") as f:
    dat = f.readlines()

dat = [d.replace("\n", "") for d in dat]

card_suits = ["C", "D", "H", "S"]
card_numbers = [str(x+2) for x in range(8)]

for num in ["T", "J", "Q", "K", "A"]:
    card_numbers.append(num)

deck = [num + suit for num in card_numbers for suit in card_suits]
#############################################


def card_value(card_number):
    return card_numbers.index(card_number) + 2


def suit_value(suit_letter):
    return card_suits.index(suit_letter)


def hand_no(n, player=1):
    return dat[n][0:14].split() if player == 1 else dat[n][15:].split()


def hands_no(n, player=1):
    return [dat[n][0:14].split(), dat[n][15:].split()]


def cnts(hand):
    n = Counter(map(lambda x: x[0], hand))
    s = Counter(map(lambda x: x[1], hand))
    return (n, s)

def is_straight(cards):
    cards=[card_value(x[0]) for x in cards]
    cards=sorted(cards)
    cards=[c - cards[0] for c in cards]
    if cards == [0,1,2,3,4]:
        return True

def hand_configuration(cards):
    interim_result="HC"
    x=cnts(cards)
    if len(x[1])==1:
        interim_result="F"
    imm=filter(lambda y:y>1,x[0].values())
    multiple=sorted(list(imm),reverse=True)
    if len(multiple)>0:
        if multiple==[2]:
            interim_result="OP"
        if multiple==[3,2]:
            interim_result="FH"
        if multiple==[3]:
            interim_result="Th"
        if multiple==[4]:
            interim_result="Fo"
        if multiple==[2,2]:
            interim_result="TP"
    else:
        if is_straight(cards):
            if interim_result=="F":
                interim_result="SF"
            else:
                interim_result="S"
    return hands_order.index(interim_result)

def hand_value(cards):
    num_cnt=cnts(cards)[0]
    cards=[((15*card_value(x[0]))**card_value(x[0]))**(num_cnt[x[0]]) for x in cards]
    return cards

def has_player1_higher_value(game_no):
    player1_hand = hand_no(game_no, 1)
    player2_hand = hand_no(game_no, 2)
    player1_values = cards_values_in_hand(player1_hand)
    player2_values = cards_values_in_hand(player2_hand)
    p1_max = player1_values.pop()
    p2_max = player2_values.pop()
    while p1_max == p2_max:
        p1_max = player1_values.pop()
        p2_max = player2_values.pop()
    return p1_max > p2_max

def cards_values_in_hand(cards):
    cards = [card_value(x[0]) for x in cards]
    c = Counter(cards)
    cards = sorted([card_val*(15**c[card_val]) for card_val in cards])
    return cards


def run_some_test():
    for x in range(4):
        tst=hand_no(x)
        tzt=hand_no(x,2)
        conf=hand_configuration(tst)
        conf2=hand_configuration(tzt)
        print(str(tst) + "  " + str(x) + " " + str(conf) + " Val " + str(hand_value(tst)) + "=" + str(sum(hand_value(tst))))
        print(str(tzt) + "  " + str(x) + " " + str(conf2) + " Val " + str(hand_value(tzt)) + "=" + str(sum(hand_value(tzt))))
        print( "1" if sum(hand_value(tst)) > sum(hand_value(tzt)) else "2")


def both(n):
    print(str(hand_no(n)) + "  " + str(hand_configuration(hand_no(n))))
    print(str(hand_no(n,2)) + "  " + str(hand_configuration(hand_no(n, 2))))


wins=[]


if __name__ == "__main__": 
    for x in range(1000):
        if hand_configuration(hand_no(x)) > hand_configuration(hand_no(x, 2)):
            wins.append(x)
        else:
            if hand_configuration(hand_no(x)) == hand_configuration(hand_no(x, 2)) and has_player1_higher_value(x):
            # if hand_configuration(hand_no(x)) == hand_configuration(hand_no(x, 2)) and sum(hand_value(hand_no(x))) > sum(hand_value(hand_no(x, 2))):
                print(str(x) + " " + str(hand_configuration(hand_no(x))))
                wins.append(x)
    print("Number of Player 1 wins:", len(wins))


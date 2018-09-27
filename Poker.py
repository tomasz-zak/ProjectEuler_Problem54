from collections import Counter


# no RF really needed as it's just a special case of SF
hands_order = ["HC", "OP", "TP", "Th", "F", "S", "FH", "Fo", "SF"]

def read_from_source_file():
    with open("p054_poker.txt") as f:
        dat = f.readlines()

    replaced = [d.replace("\n", "") for d in dat]
    return replaced


dat = read_from_source_file()

card_suits = ["C", "D", "H", "S"]
card_numbers = [str(x + 2) for x in range(8)]

for num in ["T", "J", "Q", "K", "A"]:
    card_numbers.append(num)

deck = [num + suit for num in card_numbers for suit in card_suits]



def card_value(card_number):
    return card_numbers.index(card_number) + 2


def hand_no(n, player=1):
    return dat[n][0:14].split() if player == 1 else dat[n][15:].split()


def hands_no(n):
    return [dat[n][0:14].split(), dat[n][15:].split()]


def cnts(hand):
    numbers = Counter(map(lambda x: x[0], hand))
    suits = Counter(map(lambda x: x[1], hand))
    return numbers, suits


def is_straight(cards):
    cards = [card_value(x[0]) for x in cards]
    cards = sorted(cards)
    cards = [c - cards[0] for c in cards]
    if cards == [0, 1, 2, 3, 4]:
        return True


def hand_configuration(cards):
    interim_result = "HC"
    x = cnts(cards)
    if len(x[1]) == 1:
        interim_result = "F"
    imm = filter(lambda y: y > 1, x[0].values())
    multiple = sorted(list(imm), reverse=True)
    if len(multiple) > 0:
        if multiple == [2]:
            interim_result = "OP"
        if multiple == [3, 2]:
            interim_result = "FH"
        if multiple == [3]:
            interim_result = "Th"
        if multiple == [4]:
            interim_result = "Fo"
        if multiple == [2, 2]:
            interim_result = "TP"
    else:
        if is_straight(cards):
            if interim_result == "F":
                interim_result = "SF"
            else:
                interim_result = "S"
    return hands_order.index(interim_result)


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
    cards = sorted([card_val * (15 ** c[card_val]) for card_val in cards])
    return cards


def hand_value(cards):
    num_cnt = cnts(cards)[0]
    cards = [((15 * card_value(x[0])) ** card_value(x[0])) ** (num_cnt[x[0]]) for x in cards]
    return cards



if __name__ == "__main__":
    wins = []
    for x in range(1000):
        if hand_configuration(hand_no(x)) > hand_configuration(hand_no(x, 2)):
            wins.append(x)
        else:
            if hand_configuration(hand_no(x)) == hand_configuration(hand_no(x, 2)) and has_player1_higher_value(x):
                print(str(x) + " " + str(hand_configuration(hand_no(x))))
                wins.append(x)
    print("Number of Player 1 wins:", len(wins))

import itertools
from collections import Counter
import operator

class Card(object):
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.rank_val = rank_lookup[rank]
    def __repr__(self):
        return self.rank + self.suit
    def __str__(self):
        return self.rank + self.suit

class Hand(object):
    def __init__(self):
        self.cards = []
        self.type = "No Pair"
        self.strength_tuple = ()
    def __repr__(self):
        return str(self.cards)
    def deal(self, cards):
        self.cards += cards
    def hand_type(self):
        cards = self.cards
        if len(cards) > 4:
            ### straight flush
            flush_check = len(set([card.suit for card in cards])) == 1
            ace_high = sorted([card.rank_val for card in cards])
            ace_low = sorted([card.rank_val if card.rank_val < 14 else 1 for card in cards])
            straight_check = False
            if ace_high == range(min(ace_high), max(ace_high)+1):
                straight_check = True
                tiebreaker = sorted(ace_high, reverse = True)
            elif ace_low == range(min(ace_low), max(ace_low)+1):
                straight_check = True
                tiebreaker = sorted(ace_low, reverse = True)
            if flush_check and straight_check:
                self.type = "Straight Flush"
                self.strength_tuple = (hand_strength_dict[self.type], tiebreaker[0])
                return self.type
            ### 4 of a kind
            val_counter = Counter(ace_high).most_common()
            four_check = val_counter[0][1] > 3
            if four_check:
                self.type = "Four of a Kind"
                self.strength_tuple = (hand_strength_dict[self.type], val_counter[0][0], val_counter[1][0])
                return self.type
            ## full house
            full_check = val_counter[0][1] == 3 and val_counter[1][1] == 2
            if full_check:
                self.type = "Full House"
                self.strength_tuple = (hand_strength_dict[self.type], val_counter[0][0], val_counter[1][0])
                return self.type
            ## flush
            if flush_check:
                self.type = "Flush"
                self.strength_tuple = tuple([hand_strength_dict[self.type]] + sorted(ace_high, reverse=True))
                return self.type
            if straight_check:
                self.type = "Straight"
                self.strength_tuple = tuple([hand_strength_dict[self.type]] + tiebreaker)
                return self.type
            three_check = val_counter[0][1] > 2
            if three_check:
                self.type = "Three of a Kind"
                self.strength_tuple = tuple([hand_strength_dict[self.type]] + [val_counter[0][0]] + sorted([e for e in ace_high if e != val_counter[0][0]], reverse = True))
                return self.type
            two_pair_check = val_counter[1][1] == 2
            if two_pair_check:
                self.type = "Two Pair"
                self.strength_tuple = tuple([hand_strength_dict[self.type]] + [e[0] for e in sorted(val_counter[:2], reverse = True)] + [val_counter[2][0]])
                return self.type
            pair_check = val_counter[0][1] == 2
            if pair_check:
                self.type = "Pair"
                self.strength_tuple = tuple([hand_strength_dict[self.type]] + [val_counter[0][0]] + sorted([e for e in ace_high if e != val_counter[0][0]], reverse = True))
                return self.type
            else:
                self.type = "High Card"
                self.strength_tuple = tuple([hand_strength_dict[self.type]] + sorted(ace_high, reverse = True))
                return self.type

suits = ['h','d','s','c']
nums = [str(e) for e in xrange(1,11)]
ranks = nums + ['j','q','k']
vals = [14] + list(xrange(2, 14))
zipped_ranks = zip(ranks,vals)
rank_lookup = {e[0]: e[1] for e in zipped_ranks}


deck = []

for suit in suits:
    for rank in ranks:
        deck.append(Card(suit, rank))

hand_strength_dict = {"Straight Flush": 8, "Four of a Kind": 7,
                      "Full House": 6, "Flush": 5, "Straight": 4,
                      "Three of a Kind": 3, "Two Pair": 2, "Pair": 1,
                     "High Card": 0}

hands = list(itertools.combinations(deck,5))

### sample hand type/strength calculation
h = Hand()
h.deal(hands[1])
print h.hand_type()

def parse_hand(hand):
    h = Hand()
    h.deal(hand)
    h.hand_type()
    return h

parsed_hands = map(parse_hand, hands)

sorted_parsed_hands = sorted(parsed_hands, key = operator.attrgetter('strength_tuple'), reverse = True)
## the respective count of hand types
c = Counter(hand.type for hand in parsed_hands)
print c
## the probability of getting the various hand types
probs = {k: float(v)/len(hands) for k,v in c.iteritems()}
print probs

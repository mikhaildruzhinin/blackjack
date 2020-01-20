#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

class Suit(): # карточные масти
    suit_symbols = {
        'diamonds': '\u2666', # бубны
        'hearts': '\u2665', # червы
        'spades': '\u2660', # пики
        'clubs': '\u2663', # трефы
    }
    suit_weights = {
        'diamonds': 3, # бубны
        'hearts': 2, # червы
        'spades': 4, # пики
        'clubs': 1, # трефы
    }
    @classmethod # статический метод класса, не привязан ни к какому конкретному экземпляру
    def get_valid_names(cls):
        return list(cls.suit_weights.keys())
    @classmethod
    def all_suits(cls): # возвращает список из 4 объектов этого класса - разных мастей
        for name in cls.get_valid_names():
            yield Suit(name)
    def __init__(self, suit_name):
        # храним имя масти
        if suit_name not in self.suit_symbols:
            raise ValueError(f'Масть может быть только одной из: {self.suit_symbols.keys()}')
        self.suit_name = suit_name
    def __str__(self):
        return self.suit_symbols[self.suit_name]
    def __repr__(self):
        return str(self)
    def __eq__(self, other):
        return self.suit_weights[self.suit_name] == self.suit_weights[other.suit_name]
    def __ne__(self, other):
        return self.suit_weights[self.suit_name] != self.suit_weights[other.suit_name]
    def __gt__(self, other):
        return self.suit_weights[self.suit_name] > self.suit_weights[other.suit_name]
    def __ge__(self, other):
        return self.suit_weights[self.suit_name] >= self.suit_weights[other.suit_name]
    def __lt__(self, other):
        return self.suit_weights[self.suit_name] < self.suit_weights[other.suit_name]
    def __le__(self, other):
        return self.suit_weights[self.suit_name] <= self.suit_weights[other.suit_name]
    def __hash__(self):
        return self.suits_weights[self.suit_name]

class Card(): # класс карты
    rank = 1
    #type = '' # не понятно, зачем это здесь
    high_ranks = {
        'jack': 11,
        'queen': 12,
        'king': 13,
        'ace': 14,
    }
    rank_symbol = {
        11: 'J',
        12: 'Q',
        13: 'K',
        14: 'A',
    }
        
    def __init__(self, rank, suit):
        # старшинство
        if type(rank) is int: # 2-10
            self.rank = rank
            assert 2 <= rank <= 14 # создаём исключение AssertionError
        elif type(rank) is str: # jack - ace
            if rank.lower() not in self.high_ranks.keys():
                raise ValueError(f'Карта может быть или числом, или одним из: {self.high_ranks.keys()}')
            else:
                self.rank = self.high_ranks[rank.lower()] # если величина старшей карты передана в виде строки, переводим её в целочисленный вид 
        if isinstance(suit, str):
            # если в ctor передали название масти, создаем объект
            self.suit = Suit(suit)
        elif isinstance(suit, Suit):
            # если передали объект-масть, то просто сохраняем его
            self.suit = suit
        else:
            # если передали что-то другое, выкидываем исключение
            raise TypeError('В качестве масти можно передавать или её название, или объект класса Suit')
    def __repr__(self):
        if self.rank <=10:
            s = str(self.rank)
        else:
            s = self.rank_symbol[self.rank]
        s += str(self.suit)
        return s
        
    def __eq__(self, other_card):
        return self.rank == other_card.rank and self.suit == other_card.suit
    def __ne__(self, other_card):
        return self.rank != other_card.rank or self.suit != other_card.suit
    def __gt__(self, other_card):
        if self.rank == other_card.rank:
            return self.suit > other_card.suit
        return self.rank > other_card.rank
    def __lt__(self, other_card):
        if self.rank == other_card.rank:
            return self.suit < other_card.suit
        return self.rank < other_card.rank
    def __ge__(self, other_card):
        if self.rank == other_card.rank:
            return self.suit >= other_card.suit
        return self.rank >= other_card.rank
    def __le__(self, other_card):
        if self.rank == other_card.rank:
            return self.suit <= other_card.suit
        return self.rank <= other_card.rank
    def get_rank(self):
        return self.rank
    
class Deck(): # колода карт
    cards = []
    def __init__(self):
        for suit in Suit.all_suits():
            for rank in range(2, 15):
                self.cards.append(Card(rank, suit))
    def __str__(self):
        return str(self.cards)
    def __repr__(self):
        return str(self)
    def shuffle(self):
        random.shuffle(self.cards)
    def sort(self):
        self.cards.sort()
    def draw_card(self):
        return self.cards.pop()
    def __iter__(self):
        return reversed(self.cards).__iter__()
    def __next__(self):
        pass
    def __getstate__(self): # этот метод нужен для записи/чтения данных
        return self.cards
    def __setstate__(self, state): # этот метод нужен для записи/чтения данных
        self.cards = state

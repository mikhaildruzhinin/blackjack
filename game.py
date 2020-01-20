#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cards import Deck
import pickle

class Game(): # партия
    separator = '-' * 10
    def start_game(self, clear_stats):
        self.clear_stats = clear_stats
        if self.clear_stats:
            # содаём свежий файл со статистикой
            self.stats = self.clear_statistics()
        else:
            # Загрузка файла со статистикой
            self.stats = self.load_statistics_file()
        print(self.separator)
        print('Ход игрока')
        score_player = self.player_turn()
        # если игрок набрал 21, он уже победил
        if score_player == 21:
            score_computer = 0
        else:
            print(self.separator)
            print('Ход компьютера')
            score_computer = self.computer_turn()
        # сравниваем результаты и выявляем победителя
        print(self.separator)
        print('Результаты')
        if score_player > 21 and score_computer > 21:
            print('Ничья')
            self.stats['total_played'] += 1
            self.stats['ties'] += 1
        elif score_player == score_computer:
            print('Ничья')
            self.stats['total_played'] += 1
            self.stats['ties'] += 1
        elif score_player <= 21 and score_computer > 21:
            print('Победил игрок')
            self.stats['total_played'] += 1
            self.stats['player_wins'] += 1
        elif score_computer <= 21 and score_player > 21:
            print('Победил Компьютер')
            self.stats['total_played'] += 1
            self.stats['computer_wins'] += 1
        elif score_player > score_computer:
            print('Победил игрок')
            self.stats['total_played'] += 1
            self.stats['player_wins'] += 1
        elif score_computer > score_player:
            print('Победил Компьютер')
            self.stats['total_played'] += 1
            self.stats['computer_wins'] += 1
        self.show_and_save_statistics()
    
    def load_statistics_file(self):
        try:
            with open('data.txt', 'rb') as src:
                self.stats = pickle.load(src)
        except FileNotFoundError:
            # содаём свежий файл со статистикой
            self.stats = self.clear_statistics()
        return self.stats

    def clear_statistics(self):
        self.stats = {}
        self.stats['total_played'] = 0
        self.stats['player_wins'] = 0
        self.stats['computer_wins'] = 0
        self.stats['ties'] = 0
        return self.stats

    def show_and_save_statistics(self):
        print(self.separator)
        print('Статистика:')
        print('Всего сыграно партий:', self.stats['total_played'])
        print('Победы:', self.stats['player_wins'])
        print('Поражения:', self.stats['computer_wins'])
        print('Ничьи:', self.stats['ties'])
        print(self.separator)
        with open('data.txt', 'wb') as src:
            pickle.dump(self.stats, src, protocol=3) # используем protocol 3 для обратной совместимости со старыми версиями Python

    def player_turn(self):
        deck = Deck()
        deck.shuffle()
        hand = []
        hand.append(deck.draw_card())
        hand.append(deck.draw_card())
        while True:
            print(self.separator)
            print('Ваши карты: ')
            print(hand)
            print('Очков: ', self.calculate_score(hand))
            if self.calculate_score(hand) == 21:
                print('Blackjack!')
                break
            if self.calculate_score(hand) > 21:
                print('Перебор')
                break
            resp = input('Продолжаем? (y/n) ').lower()
            if resp == 'n':
                break
            elif resp == 'y':
                card = deck.draw_card()
                hand.append(card)

        player_score = self.calculate_score(hand)
        return player_score
        
    def computer_turn(self):
        deck = Deck()
        deck.shuffle()
        hand = []
        hand.append(deck.draw_card())
        hand.append(deck.draw_card())
        computer_score = self.calculate_score(hand)
        
        print(self.separator)
        print('Начальная рука')
        print(hand)
        print(computer_score)
        
        while True:
            if computer_score > 21:
                print('Перебор')
                break
            # Здесь можно добавить решение, если в руке есть тузы и количество очков 19-20
            odds = self.calculate_odds(deck, hand)
            if odds == -1:
                # Ровно 21 в руке
                print('Blackjack!')
                break
            #print('Вероятность не проиграть', odds)
            if odds < 0.35:
                #print('Хватит')
                break
            #print('беру карту')
            hand.append(deck.draw_card())
            computer_score = self.calculate_score(hand)
            print(self.separator)
            print('Рука')
            print(hand)
            print(computer_score)
        return computer_score
        
    def calculate_score(self, cards):
        '''
        Считаем очки в пользу игрока
        '''
        score = 0
        for card in cards:
            if card.get_rank() <=10:
                score += card.get_rank()
            elif 10 < card.get_rank() <14: # J, Q, K
                score += 10
            else: # A
                score += 11 # для начала туз всегда считаем как 11
        if score <= 21:
            return score
        # Если мы здесь, то очков больше 21
        amount_of_aces = 0
        for card in cards:
            if card.get_rank() == 14:
                amount_of_aces += 1
        for i in range(amount_of_aces):
            score -= 10
            if score <= 21:
                return score
        # Если мы дошли до сюда, то игрок 100% проиграл
        return score
    def calculate_odds(self, deck, cards):
        '''
        Возвращает вероятность не превысить 21 взяв следующую карту, либо возвращает -1, если в руке ровно 21
        '''
        # Сначала проверяем, не набралось ли 21 в руке
        score = self.calculate_score(cards)
        if score == 21:
            return -1 # возвразщаем заведомо выпадающее из смысла значение
        # В противном случае считаем кол-во очков в руке
        # При этом считая все тузы за 1
        score = 0
        for card in cards:
            rank = card.get_rank()
            if rank <= 10:
                # Обычная карта
                score += rank
            elif 11 <= rank <= 13:
                # J, Q, K
                score += 10
            elif rank == 14:
                # Тузы считаем за 1
                score += 1
        target_highest_rank = 21 - score
        if target_highest_rank <= 1:
            return 0.0
        number_of_cards_with_that_rank = 0
        for card in deck.cards:
            rank = card.get_rank()
            # В нашей игре значения считаются по-другому
            # Rank - старшинство карты
            # Value - количество очков этой карты в игре, может отличаться от rank
            if rank <= 10:
                # Обычная карта
                value = rank
            elif 11 <= rank <= 13:
                # J, Q, K
                value =  10
            elif rank == 14:
                # Тузы считаем за 1
                value = 1
            # Здесь в value попадает количество очков каждой оставшейся карты в колоде
            # И мы сравниваем с оставшимся количеством очков до 21 в руке
            if value <= target_highest_rank:
                number_of_cards_with_that_rank += 1
        return number_of_cards_with_that_rank / len(deck.cards)

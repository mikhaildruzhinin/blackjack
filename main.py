#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from game import Game
import argparse

parser = argparse.ArgumentParser('')
parser.add_argument('--clear-statistics', '-c', dest='clear_stats', action='store_true', default=False, help='Очистить статистику')

ARGS = parser.parse_args()

new_game = Game()
new_game.start_game(ARGS.clear_stats)

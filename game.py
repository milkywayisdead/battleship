"""
"""
import os
from random import randrange
from time import sleep

from _ships import _build_random_fleet
from _base import Player, LETTERS, HELP, CONFUSED, _display


def game():
	test_game = False # режим автоигры

	print('Введите Ваше имя:')
	username = input()
	print('Чтобы получить список команд, введите help во время своего хода!')

	person = Player(_build_random_fleet())
	person.name = username
	cpu = Player(_build_random_fleet(), True)
	cpu.name = 'CPU'

	players = [person, cpu]
	active_player = players[randrange(0, len(players))]
	players.remove(active_player)
	inactive_player = players[0]

	swapped = True # флаг перехода хода

	while True:

		if swapped:
			print(f'Ходит {active_player}')

		swapped = False
		target = None # атакуемое поле
		confused = False # флаг непонятной команды

		# Ход компьютера
		if active_player.is_cpu:
			sleep(1)
			target = active_player._attack()

		# Ход игрока
		else:
			if test_game:
				command = 'auto'
			else:
				command = input()
			command = command.rstrip().split(' ')
			cmd = command[0].lower()

			if cmd not in ['attack', 'fleet', 'shots', 'cls', 'help', 'q', 'auto', 'testmode']:
				confused = True			

			if cmd == 'attack':
				confused = True
				if len(command) == 2:
					field = command[1]
					
					if field:
						letter = field[0]
						letter_upper = field[0].upper()
						
						if letter != ' ' and letter_upper in LETTERS:
							x = LETTERS.index(letter_upper)
							field = field.replace(letter, '')
							if field:
								try:
									y = int(field)
								except ValueError:
									pass
								else:
									if 1 <= y <= 10:
										target = (x, y)
										confused = False

			if confused:
				print(CONFUSED)

			if cmd == 'fleet':
				_display(active_player.fleet, active_player.lost, 'fleet')

			if cmd == 'shots':
				_display(active_player.hits, active_player.shots, 'shots')

			if cmd == 'cls':
				os.system('cls')

			if cmd == 'help':
				print(HELP)

			if cmd == 'q':
				break

			if cmd == 'auto':
				target = active_player._attack()

			if cmd  == 'testmode':
				test_game = True

		""" 
		Если игрок сделал выстрел - ввел команду атаки 
		(компьютерный игрок делает это в любом случае)
		"""
		if target:
			if target in active_player.shots or target in active_player.hits:
				print('В эту клетку уже стреляли!')
				continue

			print(f'{active_player} стреляет в {LETTERS[target[0]]}{target[1]}!')
			if target in inactive_player.fleet:
				print('Попал!')
				active_player.hits.append(target)
				inactive_player.fleet.remove(target)
				inactive_player.lost.append(target)

				if not inactive_player.fleet:
					print(f'Победил {active_player}!')

					print('Результаты:')
					print(f'Флот {active_player}:')
					active_player._display(active_player.fleet, active_player.lost)
					print(f'Флот {inactive_player}:')
					inactive_player._display(inactive_player.fleet, inactive_player.lost)
					break

			else:
				print('Мимо!')
				active_player.shots.append(target)
				active_player, inactive_player = inactive_player, active_player
			swapped = True


if __name__ == '__main__':
	game()
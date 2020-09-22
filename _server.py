"""
Сервер.
Пока не работает.
"""

import os
from random import randrange
import threading
from time import sleep

from _ships import _build_random_fleet
from _base import * 


_CLIENT = None
_client_data = ''
_CONN = None

HOST = ''
PORT = 50007

def _create_server_socket(host, port):
	"""
	Создание сокета
	"""

	s = _create_socket()
	s.bind((host, port))
	s.listen(1)
	return s

def _handle_client(sock):
	"""
	Обработка сообщений от клиента
	"""
	global _CONN, _CLIENT, _client_data
	lock = threading.Lock()

	conn, addr = sock.accept()
	_CONN = conn

	with conn:
		print('Второй игрок подключился!')
		_CLIENT = Player(_build_random_fleet())
		_CLIENT.is_client = True

		while True:
			data = conn.recv(1024)
			if not data:
				break

			_client_data = _deframe(data)

			if _client_data and 'client_name' in _client_data:
				_CLIENT.name = _client_data['client_name']

_server_socket = _create_server_socket(HOST, PORT)
_client_thread = threading.Thread(target=_handle_client, args=(_server_socket, ), daemon=True)

def server():
	"""
	Сервер
	"""

	print('Введите Ваше имя:')
	username = input()
	print('Чтобы получить список команд, введите help во время своего хода!')

	server_player = Player(_build_random_fleet())
	server_player.name = username
	server.is_client = False

	_client_thread.start()
	print('Ожидание второго игрока...')
	while _CLIENT is None:
		pass

	players = [server_player, _CLIENT]
	active_player = players[randrange(0, len(players))]
	players.remove(active_player)
	inactive_player = players[0]

	swapped = True # флаг перехода хода

	def swap_message():
		swapped_message = f'Ходит {active_player}'
		swapped_message_for_client = _make_framed({
				"message": swapped_message,
				"active_player": "client" if active_player.is_client else "",
			})
		return swapped_message_for_client

	while True:

		if swapped:
			print(f'Ходит {active_player}')
			_CONN.sendall(swap_message())

		swapped = False
		target = None # атакуемое поле
		confused = False # флаг непонятной команды
		command = ''

		# Ход игрока-клиента
		if active_player.is_client:
			if _client_data and 'message' in _client_data:
				command = _client_data['message']

		# Ход игрока-сервера
		else:
			command = input()

		if command:
			command = command.rstrip().split(' ')
			cmd = command[0].lower()

			if cmd not in ['attack', 'fleet', 'shots', 'cls', 'help', 'q', 'auto']:
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
				if not active_player.is_client:
					print(CONFUSED)
				else:
					pass

			if cmd == 'fleet':
				if not active_player.is_client:
					_display(active_player.fleet, active_player.lost, 'fleet')
				else:
					_CONN.sendall(_make_framed({
							"message": "fleet",
							"data": [active_player.fleet, active_player.lost],
						}))

			if cmd == 'shots':
				if not active_player.is_client:
					_display(active_player.hits, active_player.shots, 'shots')
				else:		
					_CONN.sendall(_make_framed({
							"message": "shots",
							"data": [active_player.hits, active_player.shots],
						}))

			if cmd == 'cls':
				os.system('cls')

			if cmd == 'help':
				print(HELP)

			if cmd == 'q':
				break

			if cmd == 'auto':
				if not active_player.is_client:
					target = active_player._attack()
				else:
					pass

			command = ''

		""" 
		Если игрок ввел команду атаки
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
					active_player._show_fleet()
					print(f'Флот {inactive_player}:')
					inactive_player._show_fleet()
					break

			else:
				print('Мимо!')
				active_player.shots.append(target)
				active_player, inactive_player = inactive_player, active_player

			swapped = True


if __name__ == '__main__':
	server()
"""
Клиент.
Пока не работает.
"""


import threading
import os

from _base import *


_data = ''
_ACTIVE = False
_server_socket = _create_socket()
_fleet, _lost = None, None


def _handle_conn(host, port, username):
	"""
	Соединение с сервером
	"""

	global _data, _ACTIVE, _server_socket
	global _fleet, _lost

	try:
		_server_socket.connect((host, port))
	except:
		print('Ошибка подключения')
		return
	
	_server_socket.sendall(_make_framed({
			"client_name": username
		}))
	print('Капитан, мы подключились к серверу!')

	while True:
		data = _server_socket.recv(1024)
		if not data:
			break

		_data = _deframe(data)

		if _data and 'message' in _data:
			if _data['message'] == 'fleet':
				_fleet = _data['data'][0]
				_lost = _data['data'][1]

		if _data and 'active_player' in _data:
			_ACTIVE =  _data['active_player'] == 'client'


def client():
	"""
	Клиент
	"""

	print('Введите  своё имя: ')
	username = input()

	print('Введите адрес сервера (по умолчанию - localhost):')
	host = input()
	if not host:
		host = 'localhost'

	print('Введите номер порта для подключения (по умолчанию - 50007):')
	port = input()
	if not port:
		port = 50007

	_server_thread = threading.Thread(target=_handle_conn, args=(host, port, username,), daemon=True)
	_server_thread.start()

	print('Чтобы получить список команд, введите help во время своего хода!')

	while True:
		command = ''
		confused = False

		if _ACTIVE:
			command = input()

		if command:
			command = command.rstrip().split(' ')
			cmd = command[0].lower()

			if cmd not in ['attack', 'fleet', 'shots', 'cls', 'help', 'q']:
				confused = True

			if cmd == 'fleet' or cmd == 'shots':
				_server_socket.sendall(_make_framed({
						"message": cmd
					}))

				if cmd == 'fleet' and _fleet is not None and _lost is not None:
					_display(_fleet, _lost, 'fleet')

			if cmd == 'cls':
				os.system('cls')

			if cmd == 'q':
				break

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
										_server_socket.sendall(_make_framed({
												"message": "attack", 
												"target": target
											})
										)



if __name__ == '__main__':
	client()
from random import randrange
import json
import socket

LETTERS = [' ', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К']

letters_row = ' '
for l in LETTERS:
	letters_row = letters_row + l + ' '

HELP = """ 
attack Б5 - выстрел по клетке Б5;
fleet - показать флот;
shots - показать выстрелы/попадания;
cls - очистить экран;
auto - автоатака;
q - выход.
"""

CONFUSED = 'Непонятная команда, капитан...'


class Player:
	"""
	Игрок.
	"""

	def __init__(self, fleet, cpu=False):
		self.fleet = fleet # клетки флота
		self.lost = [] # подбитые клетки своего флота
		self.shots = [] # неудачные выстрелы
		self.hits = [] # попадания
		self.cpu = cpu # игрок управляется компьютером
		self.name = ''
		self.is_client = False # является ли клиентом при игре по сети

	@property
	def is_cpu(self):
		return self.cpu

	def __str__(self):
		return self.name

	def _attack(self):
		"""
		Создание координат клетки для атаки.
		"""

		while True:
			target = (randrange(1, 11), randrange(1, 11))
			if not target in self.shots and not target in self.hits:
				return target


def _display(fleet_or_hits, lost_or_shots, scope='fleet', as_string=False):
	"""
	Вывести на экран флот или выстрелы/попадания/промахи.
	"""

	assert scope in ('fleet', 'shots'), 'Неизвестное значение параметра для отображения'

	if scope == 'fleet':
		empty = '. '
		ship_or_hit = 'O '
		hit_or_missed = 'x '
	else:
		empty = '? '
		ship_or_hit = 'x '
		hit_or_missed = '. '

	as_str = ''
	for y in reversed(range(1, 11)):
		s = str(y) + ' '
		if y <= 9:
			s = ' ' + s

		for x in range(1, 11):
			if (x, y) in fleet_or_hits or [x, y] in fleet_or_hits:
				s += ship_or_hit
			elif (x, y) in lost_or_shots or [x, y] in lost_or_shots:
				s += hit_or_missed
			else:
				s += empty
		if not as_string:
			print(s)
		else:
			as_str += s
	if not as_string:
		print(letters_row)
	else:
		return as_str + letters_row

def _create_socket():
	return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def _make_framed(message):
	"""
	Сделать фрейм
	"""

	message = json.dumps(message)
	framed = '*0' + message + '*1'
	return framed.encode()

def _deframe(data):
	"""
	Достать сообщение из порции данных
	"""
	data = data.decode()

	frame_start, frame_end = False, False
	frame = ''
	for n, l in enumerate(data):
		if l == '0' and data[n - 1] == '*':
			frame_start = True
		
		if l == '1' and data[n - 1] == '*':
			frame_end = True
			break

		if frame_start and not frame_end:
			frame += l

	if frame.startswith('0') and frame.endswith('*'):
		frame = frame.lstrip('0').rstrip('*')
		return json.loads(frame)

__all__ = [
	'Player', 'LETTERS', 'HELP', 'CONFUSED',
	'_display', '_create_socket', '_make_framed',
	'_deframe'
]
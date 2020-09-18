from random import randrange

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

	@property
	def is_cpu(self):
		return self.cpu

	def __str__(self):
		return self.name

	def _show_fleet(self, l=False):
		"""
		Отобразить флот.
		"""

		if l:
			print(self.fleet)
			return

		for y in reversed(range(1, 11)):
			s = str(y) + ' '
			if y <= 9:
				s = ' ' + s

			for x in range(1, 11):
				if (x, y) in self.fleet:
					s += 'O '
				elif (x, y) in self.lost:
					s += 'x '
				else:
					s += '. '
			print(s)
		print(letters_row)

	def _show_shots(self):
		"""
		Отобразить выстрелы/промахи/попадания
		"""

		for y in reversed(range(1, 11)):
			s = str(y) + ' '
			if y <= 9:
				s = ' ' + s

			for x in range(1, 11):
				if (x, y) in self.hits:
					s += 'x '
				elif (x, y) in self.shots:
					s += '. '
				else:
					s += '? '
			print(s)
		print(letters_row)

	def _attack(self):
		"""
		Создание координат клетки для атаки.
		"""

		while True:
			target = (randrange(1, 11), randrange(1, 11))
			if not target in self.shots and not target in self.hits:
				return target
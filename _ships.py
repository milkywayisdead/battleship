"""
Корабли.
"""

from random import randrange

SUB = 'submarine'
DESTR = 'destroyer'
CRUIS = 'cruiser'
BS = 'battleship'
DECKS_N = [1, 2, 3, 4]


class Deck:
	"""
	Палубы (клетки), из которых состоят корабли.
	"""

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return f'{self.x}:{self.y}'

	@property
	def xy(self):
		""" Кортеж с координатами """
		return self.x, self.y

	@property
	def reserved(self):
		"""
		Зарезервированные клетки 
		(чтобы корабли не могли стоять вплотную).
		"""
		x, y = self.x, self.y
		res = [(x, y), ]

		if x + 1 <= 10:
			res.append((x + 1, y))
			if y + 1 <= 10:
				res.append((x + 1 , y + 1))
			if y - 1 >=1 :
				res.append((x + 1, y - 1))

		if x - 1 >=1:
			res.append((x - 1, y))
			if y + 1 <= 10:
				res.append((x - 1 , y + 1))
			if y - 1 >=1 :
				res.append((x - 1, y - 1))

		if y + 1 <=10:
			res.append((x, y + 1))

		if y - 1 >= 1:
			res.append((x, y - 1))

		return res
	

class Submarine:
	"""
	Одна клетка.
	"""
	desc = SUB

	def __init__(self, x, y, align='v'):
		"""
		align - вертикальное или гориз. расположение
		"""

		self.deck1 = Deck(x, y)

	@property
	def decks(self):
		decks = []

		for n in DECKS_N:
			d = f'deck{n}'
			if hasattr(self, d):
				decks.append(getattr(self, d).xy)

		return decks

	@property
	def reserved(self):
		decks_n = [1, 2, 3, 4]
		res = []

		for n in DECKS_N:
			d = f'deck{n}'
			if hasattr(self, d):
				for r in getattr(self, d).reserved:
					if not r in res:
						res.append(r)

		return res

	def __str__(self):
		decks_n = [1, 2, 3, 4]

		s = f'{self.desc}['

		for n in DECKS_N:
			d = f'deck{n}'
			if hasattr(self, d):
				s += f'({getattr(self, d).__str__()}), '

		s += ']'
		return s


class Destroyer(Submarine):
	"""
	Двухпалубник.
	"""
	desc = DESTR

	def __init__(self, x, y, align='v'):
		super().__init__(x, y, align)
		
		if align == 'h':
			self.deck2 = Deck(x+1, y) 
		else:
			self.deck2 = Deck(x, y-1)


class Cruiser(Destroyer):
	"""
	Трёхпалубник.
	"""
	desc = CRUIS

	def __init__(self, x, y, align='v'):
		super().__init__(x, y, align)

		if align == 'h':
			self.deck3 = Deck(x+2, y) 
		else:
			self.deck3 = Deck(x, y-2)


class Battleship(Cruiser):
	"""
	Четырёхпалубник.
	"""
	desc = BS

	def __init__(self, x, y, align='v'):

		super().__init__(x, y, align)
		
		if align == 'h':
			self.deck4 = Deck(x+3, y) 
		else:
			self.deck4 = Deck(x, y-3)


def _build_ship(ship=SUB, x=1, y=1, align='v'):
	"""
	Построить корабль.
	"""

	if align == 'v' and y < 4:
		y = 4

	if align == 'h' and x > 7:
		x = 7

	if ship == DESTR:
		return Destroyer(x, y, align)

	if ship == CRUIS:
		return Cruiser(x, y, align)

	if ship == BS:
		return Battleship(x, y, align)

	return Submarine(x, y, align)


def _build_random_fleet():
	"""
	Случайный флот.
	"""
	fleet = []
	reserved = [] # зарезервированные клетки
	alignment = ['v', 'h']

	# Проверка, попадает ли клетка корабля в список зарезервированных 
	f = lambda x: not x in reserved

	# счетчики новых кораблей
	counters = {
		SUB: 4,
		DESTR: 3,
		CRUIS: 2,
		BS: 1,
	}

	# типы создаваемых кораблей
	ships_types = [SUB, DESTR, CRUIS, BS]

	while len(fleet) < 20:
		rand_ship = ships_types[randrange(0, len(ships_types))]
		rand_x = randrange(1, 11)
		rand_y = randrange(1, 11)
		rand_alignment = alignment[randrange(0, 2)]
		ship = _build_ship(rand_ship, rand_x, rand_y, rand_alignment)

		ship_is_ok = all([f(cell) for cell in ship.decks])
		"""
		Если новый корабль не попадает в занятые клетки,
		то он его клетки добавляются во флот,
		и в список зарезервированных клеток добавляются его
		зарезервированные клетки.
		"""
		if ship_is_ok: 
			fleet += ship.decks
			reserved += ship.reserved

			"""
			Если построено достаточно кораблей этого типа,
			то тип корабля удаляется из доступных для строительства типов
			и из счетчиков.
			"""
			counters[rand_ship] -= 1
			if counters[rand_ship] == 0:
				counters.pop(rand_ship)
				ships_types.remove(rand_ship)

	return fleet
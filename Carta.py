import random

class Carta:
		
	def __init__(self, num, palo):
		self.num = num
		self.palo = palo
		
		if num < 10: 
			self.valor = self.valorP = num
		else:
			self.valor = num-2
			self.valorP = 0
		
		self.peso = 1

		if palo == "Oro":
			self.peso += 0.55
		if num == 6:
				self.peso += 1
		elif num == 7:
			self.peso += 5 if palo == "Oro" else 2.5

	def __add__(self, carta):
		return self.valor + carta.valor

	def __gt__(self, carta):
		if self.peso == carta.peso:
			return self.num > carta.num

		return self.peso > carta.peso

	def __repr__(self):
		return f"{self.num} de {self.palo}"

def crearMazo():
	mazo = [Carta(num, palo) for num in range(1,13) for palo in ["Espada","Basto","Oro","Copa"] if num not in [8,9]]
	random.shuffle(mazo)
	return mazo

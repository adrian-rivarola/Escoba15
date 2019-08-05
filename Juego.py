import Jugadores
import random
import Carta
import time
import os

if os.name == "nt":
	clear = 'os.system("cls")'
	pausa = 'os.system("pause")'
else:
	pausa = 'input("Presione Enter para continuar...")'
	clear = 'os.system("clear")'

class Juego:

	def set_jugadores(self):
		self.jugadores = [Jugadores.Humano(0)]

		while 1:
			eval(clear)
			print("+-------------------------------+")
			print(" Ingresar numero de Bots (1,3,5) ")
			print("+-------------------------------+")
			try:
				inp = int(input("> "))
				
				#Con un número impar de jugadores, en la última ronda se reparten menos cartas a cada jugador
				if inp not in [1,3,5]: continue

				self.jugadores.extend([Jugadores.Cpu(i+1) for i in range(inp)])
				break

			except ValueError:
				continue
		
		self.puntos = [0 for _ in self.jugadores]

	def reset(self):
		for jugador in self.jugadores:
			jugador.reset()

		self.ronda = 0
		self.ultimo_comer = None
		self.mazo = Carta.crearMazo()
		self.cartas_mesa = [self.mazo.pop() for _ in range(4)]

	def repartir(self):
		self.ronda += 1
		for i in range(3):
			for jugador in self.jugadores:
				try: jugador.cartas.append(self.mazo.pop())
				except IndexError: break
			
			eval(clear)
			print("----------------------")
			print("  Repartiendo"+"."*(i+1))
			print("----------------------")
			time.sleep(0.3)
		time.sleep(0.3)

	def comprobar_ganador(self):
		result = { n : [0, 0, ""] for n in ["Oro", "Belo", "Carta", "Primera"] }
		self.rondas = 0
		
		for i, jugador in enumerate(self.jugadores):
			jugador_pts = jugador.puntos
			
			self.puntos[i] += jugador_pts["Escobas"]

			if jugador_pts["Belo"]: result["Belo"] = [0, i, jugador.nombre]

			for n in ["Oro", "Carta", "Primera"]:
				
				if jugador_pts[n] > result[n][0]:
					result[n] = [jugador_pts[n], i, jugador.nombre]

				elif jugador_pts[n] == result[n][0]:
					result[n][1] = result[n][2] = "Pozo"

		eval(clear)
		print("==========================")
		print("=       Resultados       =")
		print("==========================")

		for key, value in result.items():  # value = [ valor , id , nombre ]
			print(f"  { key }", " " * (7-len(key)) ,f"->  { value[2] }")
			
			try:  self.puntos[value[1]] += 1
			except TypeError: pass #Llega aquí cuando hay pozo(empate).

		print("==========================\n")
		
		print("--------------------------")
		print("-        Puntos          -")
		print("--------------------------")
		
		for i, jugador in enumerate(self.jugadores):
			print(f"  { jugador.nombre }" + " " * (9-len(jugador.nombre)) + f" :   { self.puntos[i] } puntos")
			print("--------------------------")
		
		eval(pausa)

	def mostrar_cartas(self):
		if not self.cartas_mesa:
			print(" No hay cartas\n en la mesa")
			print("----------------------")
			return

		print("  Cartas en la mesa:  ")
		for i, carta in enumerate(self.cartas_mesa):
			print(f" { i+1 }. { carta }")
		
		print("----------------------")

	def jugar_ronda(self, jugador, n):

		eval(clear)
		print("======================")
		print(f"=      Ronda {self.ronda}.{n}     =")
		print("======================")

		print(f" Turno: { jugador.nombre }\n----------------------")

		self.mostrar_cartas()
		jugador.jugar(self)
		eval(pausa)

	def jugar(self):
		
		self.set_jugadores()

		while max(self.puntos) < 15:
			
			self.reset()
			
			while self.mazo:
				self.repartir()

				for n in range(1, 4):
					for jugador in self.jugadores:
						self.jugar_ronda(jugador, n)

			while self.cartas_mesa:
				cart = self.cartas_mesa.pop()
				#Agrega las cartas que sobran en la mesa al último jugador que comió algo.
				self.jugadores[self.ultimo_comer].cartas_comidas[cart.palo].append(cart.valorP)

			self.comprobar_ganador()


def main():
	juego = Juego()
	opciones = [juego.jugar, mostrar_ayuda, exit]
	while 1:
			eval(clear)
			print("==========================")
			print("=       Escoba  15       =")
			print("==========================")
			print("-  1. Inicar Juego       -")
			print("-  2. Cómo jugar?        -")
			print("-  3. Salir              -")
			print("--------------------------")
			try:
				inp = int(input("> "))-1
				opciones[inp]()
			except (ValueError, IndexError): continue

def mostrar_ayuda():
	eval(clear)
	print("--------------------------------------------")
	print("-               Cómo jugar?                -")
	print("--------------------------------------------\n")
	print(" Cuando parecezca el mensaje 'Elegir carta' ")
	print(" debes ingresar el índice de la carta que   ")
	print(" quieres jugar (1-3), si el numero ingresado")
	print(" es correcto aparecerá una línea de guiones.\n")
	print("--------------------------------------------\n")
	print(" A continuación, debes ingresar los índices ")
	print(" de las cartas que quieras comer, separados ")
	print(" por un espacio. Ejs '1 2 3', '1'. Si no    ")
	print(" puedes comer ninguna carta, ingresa 0 para ")
	print(" tirar la carta previamente seleccionada.   \n")
	print("--------------------------------------------")
	eval(pausa)

if __name__ == '__main__':
	main()

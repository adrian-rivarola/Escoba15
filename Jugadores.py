class Jugador:
	def __init__(self, _id):
		self.id = _id
		self.reset()

	def reset(self):
		self.cartas = []
		self.escobas = 0
		self.cartas_comidas = { palo : [] for palo in ["Espada", "Basto", "Copa", "Oro"] }  #Cambiar nombre

	@property
	def puntos(self):
		Carta = Primera = 0
		for cartas in self.cartas_comidas.values():
			try:
				Primera += max(cartas)
				Carta += len(cartas)
			
			except ValueError:
				pass

		return {
			"Oro" : len(self.cartas_comidas["Oro"]),
			"Belo" : 7 in self.cartas_comidas["Oro"],
			"Carta" : Carta,
			"Primera" : Primera,
			"Escobas" : self.escobas
		}

	def comer_cartas(self, cartas, juego):
				
		print("----------------------")
		print("-  Cartas agregadas  -")
		
		for carta in cartas: 
			print(f" { carta }")

			self.cartas_comidas[carta.palo].append(carta.valorP)
			
			try: juego.cartas_mesa.remove(carta)
			except ValueError: pass
		
		print("----------------------")
		if not juego.cartas_mesa:
			print(" Escoba!\n----------------------")
			self.escobas += 1

		juego.ultimo_comer = self.id

class Humano(Jugador):
	def __init__(self, id_):
		super().__init__(id_)
		self.nombre = f"Jugador { id_+1 }"

	def jugar(self, juego):

		print("-    Tus cartas:     -")
		for i, carta in enumerate(self.cartas):
			print(f" { i+1 }. { carta }")

		print("----------------------")
		print(" Elegir carta:")

		while 1:
			try:
				inp = int(input("> "))-1
				carta_sel = self.cartas.pop(inp)
				break
			except (IndexError, ValueError): continue

		print("----------------------")
		print(" Tirar/Comer carta:")

		while 1:
			try:
				inp = input("> ")
				if inp == "0":
					juego.cartas_mesa.append(carta_sel)
					print(f" { self.nombre }: \n Tira el { carta_sel }")
					print("----------------------")
					break
				
				idxs = [int(i)-1 for i in inp.split(" ")]
				cartas = [carta_sel] + [juego.cartas_mesa[i] for i in idxs]
				
				if sum([c.valor for c in cartas]) == 15:
					self.comer_cartas(cartas, juego)
					break
				else: raise ValueError

			except (ValueError, IndexError):
				print("Opcion incorrecta")
				continue


class Cpu(Jugador):
	def __init__(self, id_):
		super().__init__(id_)
		self.nombre = f"Cpu { id_ }"

	def jugar(self, juego):

		if len(self.cartas) == 3: self.cartas.sort(reverse=True)
		self.opciones = []

		for carta in self.cartas:
			self.buscar_sumas(carta, juego.cartas_mesa)

		if not self.opciones:
			carta_tirar = self.cartas.pop()
			juego.cartas_mesa.append(carta_tirar)

			print(f" { self.nombre }: \n Tira el { carta_tirar }")
			print("----------------------")
			return

		mejor_opcion = idx_m = 0

		for i,opc in enumerate(self.opciones):

			peso = sum(cart.peso for cart in opc)
			
			if juego.cartas_mesa == opc[1:]: peso += 6 #Escoba!

			if peso > mejor_opcion:
				mejor_opcion = peso
				idx_m = i

		carta_tirar = self.opciones[idx_m][0]

		print(f" { self.nombre }: \n Juega el { carta_tirar }")

		self.cartas.remove(carta_tirar)
		self.comer_cartas(self.opciones[idx_m], juego)

	def buscar_sumas(self, mi_carta, cartas_mesa, parcial=[]):
		#Busca combinaciones que sumen 15, las guarda en un array dentro de self.opciones
		nums_parcial = [cart.valor for cart in parcial]
		
		if sum(nums_parcial) + mi_carta.valor == 15:
				self.opciones.append([mi_carta] + parcial)
				return
		
		for i in range(len(cartas_mesa)):
				n = cartas_mesa[i]
				remaining = cartas_mesa[i+1:]
				self.buscar_sumas(mi_carta, remaining, parcial + [n])

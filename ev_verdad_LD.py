# Pablo Ariño | Práctica 2 | Lógica para IA | CDIA

from typing import List

# EJERCICIO 6:

# (p ∨ ¬q ∨ ¬r ∨ ¬ser rico) ∧ (¬p ∨ q ∨ r ∨ ser rico) en FNC:
formula = [["p", "!q", "!r", "!ser rico"], ["!p", "q", "r", "ser rico"]]
asignacion_verdad = {"p": 0.3, "q": 0.7, "r": 0.5, "ser rico": 0.2}
asignacion_verdad = {'p': 0.3, 'q': 0.22, 'r': 0.55, 'ser rico': 0.2}
asignacion_verdad = {'p': 0.3, 'q': 0.7, 'r': 0.01, 'ser rico': 0.7}

def ev_negacion_GD(valor_verdad):
	if valor_verdad == 0:
		return 1
	else:
		return 0

def ev_negacion_Lukasiewicz(valor_verdad): return 1 - valor_verdad

def evaluarVerdadGodelDummettFNC(formula: List[list], asignacion_verdad: dict) -> float:
	
	# Obtenemos una lista de listas con los valores de verdad
	valores_verdad = []
	for lista in formula:
		aux = []
		for literal in lista:
			if literal[0] == "!":
				valor_verdad = asignacion_verdad[literal[1:]]
				aux.append(ev_negacion_GD(valor_verdad))
			else:
				aux.append(asignacion_verdad[literal])

		valores_verdad.append(aux)

	# Obtenemos una lista con los maximos valores de verdad 
	# de las listas contenidas en valores_verdad
	max_valores = [max(lista) for lista in valores_verdad]

	return min(max_valores)

# Extra:
def evaluarVerdadLukasiewiczFNC(formula: List[list], asignacion_verdad: dict) -> float:
	
	# Obtenemos una lista de listas con los valores de verdad
	valores_verdad = []
	for lista in formula:
		aux = []
		for literal in lista:
			if literal[0] == "!":
				valor_verdad = asignacion_verdad[literal[1:]]
				aux.append(ev_negacion_Lukasiewicz(valor_verdad))
			else:
				aux.append(asignacion_verdad[literal])

		valores_verdad.append(aux)

	# Obtenemos una lista con los maximos valores de verdad 
	# de las listas contenidas en valores_verdad
	max_valores = [max(lista) for lista in valores_verdad]

	return min(max_valores)

print(evaluarVerdadGodelDummettFNC(formula, asignacion_verdad))
# print(evaluarVerdadLukasiewiczFNC(formula, asignacion_verdad))
print()


# Ejemplos
formula1 = "(((!p|q)&r)>(p>!q))"  # ((¬p ∨ q) ∧ r) → (p → ¬q)
formula2 = "((((p&!q)&!r)&!ser rico)|(((!p&q)&r)&ser rico))"  # FND
formula3 = "((((p|!q)|!r)|!ser rico)&(((!p|q)|r)|ser rico))"  # FNC

# Las siguientes dos funciones son comunes para los dos proximos ejercicios:
def dividir(formula: str) -> list:
	"""parsea la formula"""
	terminoActual = ""
	terminos = []
	numeroParentesis = 0

	if formula[0] == "!":
		return ["!", formula[1:]]

	for i in range(len(formula)):
		caracterActual = formula[i]
		# El primer termino y el ultimo no los añadimos ya que son parenteis
		if (i == 0 and caracterActual == "(") or \
			(i == len(formula) - 1 and caracterActual == ")"):
			pass
		else:
			# Si se encuentra parentesis actualizamos el valor de numeroParentesis
			if caracterActual == '(':
				numeroParentesis += 1
				terminoActual += caracterActual

			elif caracterActual == ')':
				numeroParentesis -= 1
				terminoActual += caracterActual

			elif caracterActual == '>' or caracterActual == '&' \
				 or caracterActual == '|':

				# Si estamos dentro de parentesis
				if numeroParentesis > 0:
					terminoActual += caracterActual

				# Si estamos fuera de parentesis crea un nuevo termino
				else:
					terminos.append(terminoActual)
					terminos.append(caracterActual)
					terminoActual = ""

			# Otros caracteres
			else:
				terminoActual += caracterActual
		"""
		Ejemplo
		Transformacion que le hara dividir() a "(((!p|q)&r)>(p>!q))":
			1. ["((!p|q)&r)", ">", "(p>!q)"]
			2. [["(!p|q)", "&", "r"], ">", ["p", ">", "!q"]]
			3. [[["!p, "|", "q"], "&", "r"], ">", ["p", ">", "!q"]]
		"""

	terminos.append(terminoActual)
	return terminos


def literal(formula):
	"""Esta funcion comprueba si la formula dada es o no un literal"""

	if formula[0] == "(":
		return False
	elif formula[0] == "!":
		return literal(formula[1:])
	else:
		return True
# -------

# EJERCICIO 7:

def evaluarVerdadGodelDummett(formula: str, asignacion_verdad: dict) -> float:
	"""
	Condiciones de la formula de entrada:
		- Debe ser o una cadena de texto o una lista 
		  de la forma [formula, simbolo, formula] o ["!", formula]
		- Cada vez que se tenga una formula con la estructura 
		  "formula-simbolo-formula" debe ir entre parenteis. 
		- Los literales no deben ir entre parentesis. Ej: (p|q), (!p=q)
		- No puede haber espacios (salvo si están contenidos en un literal. Ej: ser rico)
	Simbolos:
		→ = ">"
		∨ = "|"
		∧ = "&"
		¬ = "!"
		Nota: la equivalencia ha sido omitida

	Devuelve la asignacion de verdad de dicha formula, un valor entre 0 y 1, segun 
	la logica de Godel-Dummet.
	"""

	if isinstance(formula, list):
		# formula = ["formula", "símbolo", "formula"]
		
		if len(formula) == 3:
			form1 = formula[0]
			simbolo = formula[1]
			form2 = formula[2]

			# Obtenemos el valor de verdad de las formulas
			if not literal(form1):
				verdad1 = evaluarVerdadGodelDummett(dividir(form1), asignacion_verdad)
			elif form1[0] == "!":
				valor_verdad = asignacion_verdad[form1[1:]]
				verdad1 = ev_negacion_GD(valor_verdad)
			else:
				verdad1 = asignacion_verdad[form1]

			if not literal(form2):
				verdad2 = evaluarVerdadGodelDummett(dividir(form2), asignacion_verdad)
			elif form2[0] == "!":
				valor_verdad = asignacion_verdad[form2[1:]]
				verdad2 = ev_negacion_GD(valor_verdad)
			else:
				verdad2 = asignacion_verdad[form2]

		elif len(formula) == 2: # ["!", formula]
			return ev_negacion_GD(evaluarVerdadGodelDummett(dividir(formula[1]), asignacion_verdad))

		elif len(formula) == 1 and literal(formula[0]):
			return asignacion_verdad[formula[0]]

		# Obtenemos si la formula es cierta o no en funcion del simbolo
		if simbolo == "|":
			return max(verdad1, verdad2)
		elif simbolo == ">":
			if verdad1 <= verdad2:
				return 1
			else:
				return verdad2
		elif simbolo == "&":
			return min(verdad1, verdad2)

	else: # Si es la primera llamada
		return evaluarVerdadGodelDummett(dividir(formula), asignacion_verdad)

print("evaluarVerdadGodelDummett:")
print(evaluarVerdadGodelDummett(formula1, asignacion_verdad))
print(evaluarVerdadGodelDummett(formula2, asignacion_verdad))
print(evaluarVerdadGodelDummett(formula3, asignacion_verdad))
print("")

# EJERCICIO 8

def evaluarVerdadLukasiewicz(formula: str, asignacion_verdad: dict) -> float:
	"""
	Condiciones de la formula de entrada:
		- Debe ser o una cadena de texto o una lista 
		  de la forma [formula, simbolo, formula] o ["!", formula]
		- Cada vez que se tenga una formula con la estructura 
		  "formula-simbolo-formula" debe ir entre parenteis. 
		- Los literales no deben ir entre parentesis. Ej: (p|q), (!p=q)
		- No puede haber espacios (salvo si están contenidos en un literal. Ej: ser rico)
	Simbolos:
		→ = ">"
		∨ = "|"
		∧ = "&"
		¬ = "!" 
		Nota: la equivalencia ha sido omitida

	Devuelve la asignacion de verdad de dicha formula, un valor entre 0 y 1, segun 
	la logica de Lukasiewicz.
	"""

	if isinstance(formula, list):
		# formula = ["formula", "símbolo", "formula"]
		
		if len(formula) == 3:
			form1 = formula[0]
			simbolo = formula[1]
			form2 = formula[2]

			# Obtenemos el valor de verdad de las formulas
			if not literal(form1):
				verdad1 = evaluarVerdadLukasiewicz(dividir(form1), asignacion_verdad)
			elif form1[0] == "!":
				valor_verdad = asignacion_verdad[form1[1:]]
				verdad1 = ev_negacion_Lukasiewicz(valor_verdad)
			else:
				verdad1 = asignacion_verdad[form1]

			if not literal(form2):
				verdad2 = evaluarVerdadLukasiewicz(dividir(form2), asignacion_verdad)
			elif form2[0] == "!":
				valor_verdad = asignacion_verdad[form2[1:]]
				verdad2 = ev_negacion_Lukasiewicz(valor_verdad)
			else:
				verdad2 = asignacion_verdad[form2]

		elif len(formula) == 2: # ["!", formula]
			return ev_negacion_Lukasiewicz(evaluarVerdadLukasiewicz(dividir(formula[1]), asignacion_verdad))

		elif len(formula) == 1 and literal(formula[0]):
			return asignacion_verdad[formula[0]]

		# Obtenemos si la formula es cierta o no en funcion del simbolo
		if simbolo == "|":
			return max(verdad1, verdad2)
		elif simbolo == ">":
			if verdad1 <= verdad2:
				return 1
			else:
				return 1-(verdad1-verdad2)
		elif simbolo == "&":
			return min(verdad1, verdad2)

	else: # Si es la primera llamada
		return evaluarVerdadLukasiewicz(dividir(formula), asignacion_verdad)

print("evaluarVerdadLukasiewicz:")
print(evaluarVerdadLukasiewicz(formula1, asignacion_verdad))
print(evaluarVerdadLukasiewicz(formula2, asignacion_verdad))
print(evaluarVerdadLukasiewicz(formula3, asignacion_verdad))
print("")


# EXTRA2:

def convierte(n: int) -> str:
	"""
	Convierte un entero en su equivalente en deduccion_automatica.pl
	de acuerdo con la notación empleada.
	"""
	num = "zero"
	for _ in range(n):
		num = "sig("+num+")"

	return num

# print(convierte(100))


from random import random
def print_tabla_verdad(formula, literales: list):
	def valores(n_literales, n):
		# n corresponde al índice de la columna de nuestra tabla de verdad
		valores = []
		for i in range(2**(n_literales - n - 1)):
			valores.extend([round(random(), 2) for i in range(2**n)])
			valores.extend([round(random(), 2) for i in range(2**n)])
			# Con esto se generan listas de la forma:
			# [0, 1]; [0, 0, 1, 1]; [0, 0, 0, 0, 1, 1, 1, 1]; ...

		for valor in valores:
			yield valor


	asignacion_verdad = {}
	generadores = [valores(len(literales), i) for i in range(len(literales))]

	for i in range(2**len(literales)):
		for j in range(len(literales)):
			asignacion_verdad[literales[j]] = next(generadores[j])

		print(asignacion_verdad, end = ": ")
		print(evaluarVerdadGodelDummett(formula, asignacion_verdad))
		# print(evaluarVerdadLukasiewicz(formula, asignacion_verdad))
		


formula = "((p|!p)>(p&!p))"
# formula = "!p"
asignacion_verdad = {"p": 0.3, "q": 0.7, "r": 0.5}
# asignacion_verdad = {"p": 0.3}
asignacion_verdad = {"p": 0.3}
print("Comprobación ejercicio")
print(dividir(formula))
print(evaluarVerdadGodelDummett(formula, asignacion_verdad))
print(evaluarVerdadLukasiewicz(formula, asignacion_verdad))
# Pablo Ariño | Práctica 1 | Lógica para IA | CDIA

# (p ∧ ¬q ∧ ¬r ∧ ¬jugar futbol) ∨ (¬p ∧ q ∧ r ∧ jugar futbol) en FND:
formula = [["p", "!q", "!r", "!jugar futbol"], ["!p", "q", "r", "jugar futbol"]]  
asignacion_verdad = {"p": 1, "q": 0, "r": 0, "jugar futbol": 0}  
# 1 = verdad, 0 = falso


# EJERCICIO 1:

def evaluarVerdadFND(formula, asignacion_verdad): 
	verdad = False
	for i in range(len(formula)):
		if verdad:
			return 1
		verdad = True
		for literal in formula[i]:
			if literal[0] == "!":
				if asignacion_verdad[literal[1:]] == 1: 
					verdad = False
					break 
			else:
				if asignacion_verdad[literal] == 0:
					verdad = False
					break
	if verdad:
		return 1
	else:
		return 0


# EJERCICIO 2:

def evaluarVerdadFNC(formula, asignacion_verdad): 
	verdad = True
	for i in range(len(formula)):
		if not verdad:
			return 0
		verdad = False
		for literal in formula[i]:
			if literal[0] == "!":
				if asignacion_verdad[literal[1:]] == 0: 
					verdad = True
					break 
			else:
				if asignacion_verdad[literal] == 1:
					verdad = True
					break
	if verdad:
		return 1
	else:
		return 0

print("FND:")
print(evaluarVerdadFND(formula, asignacion_verdad))

print("FNC:")
print(evaluarVerdadFNC(formula, asignacion_verdad))
print("")

# EJERCICIO 3:

# Condiciones de la entrada:
	# - Debe ser o una cadena de texto o una lista 
	#   de la forma [formula, simbolo, formula] o ["!", formula]
	# - Cada vez que se tenga una formula con la estructura 
	#   "formula-simbolo-formula" debe ir entre parénteis. 
	# - Los literales no deben ir entre paréntesis. Ej: (p|q), (!p=q)
	# - No puede haber espacios (salvo si están contenidos en un literal. 
	#   Ej: Jugar futbol)
# Simbolos:
	# ↔ = "="
	# → = ">"
	# ∨ = "|"
	# ∧ = "&"
	# ¬ = "!"

# Ejemplos
formula1 = "(((!p|q)&r)>(p=!q))" # ((¬p ∨ q) ∧ r) → (p ↔ ¬q)
formula2 = "((((p&!q)&!r)&!jugar futbol)|(((!p&q)&r)&jugar futbol))"  # FND
formula3 = "((((p|!q)|!r)|!jugar futbol)&(((!p|q)|r)|jugar futbol))"  # FNC

def evaluar_verdad_LP(formula, asignacion_verdad):
	def dividir(formula):
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
					or caracterActual == '=' or caracterActual == '|':

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

			# Ejemplo
			# Transformación que le hará dividir() a "(((!p|q)&r)>(p=!q))":
				# 1. ["((!p|q)&r)", ">", "(p=!q)"]
				# 2. [["(!p|q)", "&", "r"], ">", ["p", "=", "!q"]]
				# 3. [[["!p, "|", "q"], "&", "r"], ">", ["p", "=", "!q"]]

		terminos.append(terminoActual)
		return terminos


	def literal(formula):
		# Esta función comprueba si la formula dada es o no un literal

		if formula[0] == "(":
			return False
		elif formula[0] == "!":
			return literal(formula[1:])
		else:
			return True


	if type(formula) == list and len(formula) > 1:
		# formula = ["formula", "símbolo", "formula"]
		
		if len(formula) == 3:
			form1 = formula[0]
			simbolo = formula[1]
			form2 = formula[2]

			# Obtenemos el valor de verdad de las formulas
			if not literal(form1):
				verdad1 = evaluar_verdad_LP(dividir(form1), asignacion_verdad)
			elif form1[0] == "!":
				verdad1 = int(not bool(asignacion_verdad[form1[1:]]))
			else:
				verdad1 = asignacion_verdad[form1[0]]

			if not literal(form2):
				verdad2 = evaluar_verdad_LP(dividir(form2), asignacion_verdad)
			elif form2[0] == "!":
				verdad2 = int(not bool(asignacion_verdad[form2[1:]]))
			else:
				verdad2 = asignacion_verdad[form2]

		elif len(formula) == 2: # ["!", formula]
			return int(not bool(evaluar_verdad_LP(dividir(formula[1]), asignacion_verdad)))

		# Obtenemos si la fórmula es cierta o no en función del símbolo
		if simbolo == "|":
			if bool(verdad1) or bool(verdad2):
				return 1
			else:
				return 0
		elif simbolo == ">":
			if not bool(verdad1):
				return 1
			elif bool(verdad2):
				return 1
			else:
				return 0
		elif simbolo == "&":
			if bool(verdad1) and bool(verdad2):
				return 1
			else:
				return 0
		elif simbolo == "=":
			if verdad1 == verdad2:
				return 1
			else:
				return 0

	else: # Si es la primera llamada
		return evaluar_verdad_LP(dividir(formula), asignacion_verdad)

print("evaluar_verdad_LP: ")
print(evaluar_verdad_LP(formula1, asignacion_verdad))
print(evaluar_verdad_LP(formula2, asignacion_verdad))
print(evaluar_verdad_LP(formula3, asignacion_verdad))
print("")


# EJERCICIO 4

def esTautologia(formula, literales: list):
	def valores(n_literales, n):
		# n corresponde al índice de la columna de nuestra tabla de verdad
		valores = []
		for i in range(2**(n_literales - n - 1)):
			valores.extend([0 for i in range(2**n)])
			valores.extend([1 for i in range(2**n)])
			# Con esto se generan listas de la forma:
			# [0, 1]; [0, 0, 1, 1]; [0, 0, 0, 0, 1, 1, 1, 1]; ...

		for valor in valores:
			yield valor


	asignacion_verdad = {}
	generadores = [valores(len(literales), i) for i in range(len(literales))]

	for i in range(2**len(literales)):
		for j in range(len(literales)):
			asignacion_verdad[literales[j]] = next(generadores[j])

		# print(asignacion_verdad, end = ": ")
		# print(evaluar_verdad_LP(formula, asignacion_verdad))
		if evaluar_verdad_LP(formula, asignacion_verdad) == 0:
			return 0
			
	return 1

tautologia1 = "((p&!p)>((!jugar futbol>r)&q))"
literales1 = ["p", "q", "r", "jugar futbol"]
tautologia2 = "((p&q)=!(p>!q))"
literales2 = ["p", "q"]
tautologia3 = "!(p&!p)"
literales3 = ["p"]
print("Tautologias:")
print(esTautologia(tautologia1, literales1))
print(esTautologia(tautologia2, literales2))
print(esTautologia(tautologia3, literales3))
print("No tautologia:")
print(esTautologia(formula1, literales1))


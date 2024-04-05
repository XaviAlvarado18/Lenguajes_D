from Classes_ import State
from typing import *
import time
from colorama import Back, Fore, Style
import ast
import astor

def Simulator(states: Dict[str, State], string: str, token_rules, expression=""):
    print(f"Simulating the string {string} in the automaton")
    print(f"Automaton: {expression}")
    isToken = False
    #print(token_rules)

    pathDict: Dict[str, List[State]] = dict()

    def simulation(initState: State ):
        paths: List[List[State]] = [[initState]]

        for char in string:
            newPaths: List[List[State]] = []

            for path in paths:
                evalState: State = path[-1]

                for st in evalState.getStates(char):
                    newPath = path.copy()
                    newPath.append(st)
                    newPaths.append(newPath)

                for st_e in evalState.getEpsilonClean() - {evalState}:
                    for st in st_e.getStates(char):
                        newPath = path.copy()
                        newPath.append(st)
                        newPaths.append(newPath)

            paths = newPaths

        for path in paths:
            evalState: State = path[-1]

            if evalState.isFinalState:
                return True, path

            for st_e in evalState.getEpsilonClean():
                if st_e.isFinalState:
                    finalPath = path.copy()
                    finalPath.append(st_e)
                    return True, finalPath

        return False, []

    simulationResult = True

    start = time.time()
    for key in states:
        result, simulationPaths = simulation(states[key])
        simulationResult = simulationResult and result
        pathDict[key] = simulationPaths
        print(f"Simulation for {key}: 'Excellent!'")
        if not result:
            break
    end = time.time()

    for tupla in token_rules:
        let, token = tupla
        if let == string:
            isToken = True
            break
        else:
            contiene_letras = False
            contiene_numeros = False
            contiene_punto = False
            
            # Iterar sobre cada carácter del string
            for char in string:
                # Verificar si el carácter es una letra
                if char.isalpha():
                    contiene_letras = True
                # Verificar si el carácter es un número
                elif char.isdigit():
                    contiene_numeros = True

                elif char == '.':
                    contiene_punto = True

            
            if (contiene_letras or contiene_numeros) and 'number' in let:
                isToken = True
                break
            elif (contiene_letras or contiene_numeros) and (not contiene_punto and '+' not in string and '-' not in string) and 'id' in let:
                isToken = True
                break



    if simulationResult and isToken and 'return' in token:
        print(Fore.GREEN + "The string was accepted", Style.RESET_ALL)
        print(Fore.GREEN + Back.GREEN, token, Style.RESET_ALL)
    elif simulationResult and isToken:
        print(Fore.GREEN + "The string was accepted", Style.RESET_ALL)
        print(Fore.GREEN + "Executanding command: "+ Back.GREEN, token, Style.RESET_ALL)

        # Analizar el código y obtener el AST
        tree = ast.parse(token)

        # Generar el código fuente en el formato deseado
        formatted_code = astor.to_source(tree)

        # Ejecutar el código generado
        exec(formatted_code)
    else:
        print(Fore.YELLOW + f"The string was not accepted", Style.RESET_ALL)

    print(f"Time elapsed: {end - start} seconds")

    return simulationResult, pathDict

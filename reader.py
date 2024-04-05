# Nombre: Kristopher Javier Alvarado López
# Carnet: 21188
# Archivo: reader.py

import sys
from colorama import Fore, Style

def Read_Yal(file):
    token_rules = []

    # Indicador para saber cuándo estamos procesando las reglas
    processing_rules = False

    # Leer el archivo Yalex
    with open(file+'.yal', 'r') as f:
        lines = f.readlines()

    # Almacenar las variables
    variables = {}
    numberLine = 0

    # Analizar cada línea
    for line in lines:
        numberLine +=1

        parts = line.split()

        if not parts:
            continue 


        # Analizar las variables
        if parts[0] == 'let':

            if parts[2] != '=':
                print(Fore.RED + "Line: ", numberLine, " --------> ",parts[1],parts[2:], Style.RESET_ALL)
                print(Fore.RED + "\nSegmentation Fault: '=' keyword missing or misspelled" + Style.RESET_ALL)
                sys.exit(0)

            variable_name = parts[1]
            variable_value = ' '.join(parts[3:])

            # Poner entre comillas los valores que contienen caracteres especiales
            if any(char in variable_value for char in ['\'', '+']):
                variable_value = f'{variable_value}'

            # Modificar la línea
            if variable_name in ["ws", "id"]:
                
                # Tomar el valor directamente de las variables necesarias sin comillas
                
                if variable_name == "ws":
                    val = variable_value.strip('+')
                    variable_value = ''.join(variables.get(val))+'+'
                    # Agregar el delimitador '+'
                    #variable_value += '+'
                elif variable_name == "id":
                    ############################################
                    #CREAR BUCLE PARA CONCATENAR LETRAS 'A'-'Z'#
                    ############################################

                    count = 0
                    resultado = []
                    for caracter in variables['letter']:
                        if caracter == '-':
                            for codigo in range(ord(variables['letter'][count-2]), ord(variables['letter'][count+2])+1):
                                resultado.append(chr(codigo))
                        
                        count += 1

                    resultado = '|'.join(f"[{letra}]" for letra in resultado)
                    
                    #list(resultado).insert(0,'(')
                    #list(resultado).append(')')
                    variables['letter'] = resultado
                    
                    #############################################
                    #CREAR BUCLE PARA CONCATENAR DIGITOS '0'-'9'#
                    #############################################

                    count = 0
                    resultado = []
                    for caracter in variables['digit']:   
                        if caracter == '-':
                            for codigo in range(ord(variables['digit'][count-2]), ord(variables['digit'][count+2])+1):
                                resultado.append(chr(codigo))
                        
                        count += 1

                    resultado = '|'.join(f"[{letra}]" for letra in resultado)
                    
                    variables['digit'] = str(resultado)

                    # Analizar la estructura de la variable id y construir la expresión correspondiente
                    id_components = line.split('=')[1].strip('\n')
                    id_expression = ''.join(
                        f"([{variables[token.strip('[]')].strip('[]') if token.strip('[]') in variables and token.strip('[]') != 'id' else token.strip('[]')}])" 
                        if token not in ('(', ')', '*', '|') else '.' + token.strip('[]')
                        if token == '(' else token.strip('[]')
                        for component in id_components.split() 
                        for token in component.replace('(', ' ( ').replace(')', ' ) ').replace('|', ' | ').replace('*', ' * ').split()
                    )
                    variable_value = id_expression

            elif variable_name == "digits":
                val = variable_value.strip('+')
                
                count = 0  
                resultado = []
                for caracter in variables['digit']:
                       
                    if caracter == '-':
                        for codigo in range(ord(variables['digit'][count-2]), ord(variables['digit'][count+2])+1):
                            resultado.append(chr(codigo))
                        
                        resultado = '|'.join(f"[{letra}]" for letra in resultado)
                    elif caracter == '"':
                        comilla_inicio = variables['digit'].find('"')
                        comilla_fin = variables['digit'].rfind('"')

                        # Verificar si se encontraron ambas comillas
                        if comilla_inicio != -1 and comilla_fin != -1:
                            # Obtener la subcadena entre las comillas
                            subcadena = variables['digit'][comilla_inicio + 1 : comilla_fin]

                            # Generar resultado con caracteres entre comillas
                            resultado = '|'.join(f"[{letra}]" for letra in subcadena)
                            break

                    count += 1

                    
                variables['digit'] = str(resultado)

                variable_value = ''.join(variables.get(val))+'+'

            elif variable_name == "number":
                # Analizar la estructura de la variable number y construir la expresión correspondiente
                id_components = line.split('=')[1].strip('\n')
                id_expression = ''

                for component in id_components.split():
                    tokens = component.replace('(', ' ( ').replace(')', ' ) ').replace('.', ' . ').replace('?', ' ? ').replace('[', '[').replace(']', ']').replace('E', 'E').split()

                    for token in tokens:
                        stripped_token = token.strip('[]')

                        if (
                            stripped_token not in ('(', ')', '.', '?', '[', 'E') and
                            stripped_token != "'E'" and
                            stripped_token in variables and
                            stripped_token != 'number'
                        ):
                            id_expression += f"[{variables[stripped_token]}]"
                        else:
                            id_expression += stripped_token

                # Simplificar la estructura de corchetes
                id_expression = id_expression.replace('[[', '[').replace(']]', ']').replace('+]','+').replace("'?","']?")

                # Imprimir la expresión
                print(id_expression)
                variable_value = id_expression
            else:
                variable_value = variable_value.strip('"')

            # Crear la variable en Python como string
            variables[variable_name] = variable_value


        if len(parts)<2:
            continue 
        elif parts[0] == 'rules':
            print(parts[0])
            processing_rules = True


        elif processing_rules:
            if "{" in parts and "}" in parts:
                open_brace_index = parts.index('{')
                # Encontrar la posición de la llave de cierre '}'
                close_brace_index = parts.index('}')

                # Buscar patrones en la línea que indiquen reglas
                if len(parts) >= 5 and parts[0] == '|':
                    token_name = parts[1].strip("',\"")
                    token_value = ' '.join(parts[open_brace_index+1:close_brace_index])
                    print("token_value: ", parts[4].strip("',\"}"))
                    token_rules.append((token_name, token_value))
                elif len(parts) >= 4 and parts[1] == '{':
                    token_name = parts[0].strip("',\"")
                    token_value = ' '.join(parts[open_brace_index+1:close_brace_index])
                    token_rules.append((token_name, token_value))
            
            else:
                newLines = ''
                for i in range(numberLine-1, len(lines)):
                    newLines += lines[i]

                    
                    if "{" in newLines:
                        open_brace_index = newLines.split().index("{")
                    if "}" in newLines:
                        close_brace_index = newLines.split().index("}")
                        break
                
                if newLines.count('|') == 2:
                    print(Fore.RED + "\nSegmentation Fault: The token definition is empty or incomplete", Style.RESET_ALL)
                    sys.exit(0)

                newLines = newLines.split()

                if len(newLines) >= 5 and newLines[0] == '|':
                    token_name = newLines[1].strip("',\"")
                    token_value = ' '.join(newLines[open_brace_index+1:close_brace_index])
                    #print("token_value: ", parts[4].strip("',\"}"))
                    token_rules.append((token_name, token_value))
                elif len(newLines) >= 4 and newLines[1] == '{':
                    token_name = newLines[0].strip("',\"")
                    token_value = ' '.join(newLines[open_brace_index+1:close_brace_index])
                    token_rules.append((token_name, token_value))

        else:
            # Buscar la línea que indica el comienzo de las reglas
            
            if parts[:3] == ['rule', 'tokens', '']:
                print("Segmentation Fault: Rule definition not found")
                sys.exit(0)
            elif parts[:3] == ['rule', 'tokens', '=']:
                processing_rules = True

    result = ''
#[('ws', 'WHITESPACE')]
    if ('ws', 'WHITESPACE') in token_rules:
        start_index = token_rules.index(('ws', 'RETURN WHITESPACE'))
    elif any(item[0] == 'id' for item in token_rules):
    # Hacer algo si 'id' está en token_rules:
        start_index = next(index for index, item in enumerate(token_rules) if item[0] == 'id')
    elif any(item[0] == 'number' for item in token_rules):
        start_index = next(index for index, item in enumerate(token_rules) if item[0] == 'number')
    elif ('+','PLUS') in token_rules:
        start_index = token_rules.index(('+','PLUS'))
    else:
        start_index = None  # Índice de inicio a partir de 'id'

    
    if start_index != None:
        for i in range(start_index, len(token_rules)):
            if token_rules[i][0] not in '()':
                result += "['"+token_rules[i][0]+"']" + '|'
            elif token_rules[i][0] == '(':
                result += '['+token_rules[i][0]+']' + '|'
            else:
                result += '['+token_rules[i][0]+']'
                break

    if 'ws' in [rule[0] for rule in token_rules] and 'id' in [rule[0] for rule in token_rules] and 'number' in [rule[0] for rule in token_rules]:
        esto = []
        lista = eval(variables['delim'])
        for cadena_escapada in lista:
            cadena_sin_escape = ''.join(chr(ord(caracter_escapado)) for caracter_escapado in cadena_escapada)
            esto.append(cadena_sin_escape)
        result = str(esto) + '|' + result.rstrip('|')
        result = variables['id'] + '|' + result.rstrip('|')
        result = variables['number'] + '|' + result.rstrip('|')
    elif 'ws' in [rule[0] for rule in token_rules] and 'id' in [rule[0] for rule in token_rules]:
        esto = []
        lista = eval(variables['delim'])
        for cadena_escapada in lista:
            cadena_sin_escape = ''.join(chr(ord(caracter_escapado)) for caracter_escapado in cadena_escapada)
            esto.append(cadena_sin_escape)
        result = str(esto) + '|' + result.rstrip('|')
        result = variables['id'] + '|' + result.rstrip('|')
    elif 'ws' in [rule[0] for rule in token_rules] and 'number' in [rule[0] for rule in token_rules]:
        esto = []
        lista = eval(variables['delim'])
        for cadena_escapada in lista:
            cadena_sin_escape = ''.join(chr(ord(caracter_escapado)) for caracter_escapado in cadena_escapada)
            esto.append(cadena_sin_escape)
        result = str(esto) + '|' + result.rstrip('|')
        result = variables['number'] + '|' + result.rstrip('|')
    elif 'id' in [rule[0] for rule in token_rules] and 'number' in [rule[0] for rule in token_rules]:
        result = variables['id'] + '|' + result.rstrip('|')
        result = variables['number'] + '|' + result.rstrip('|')
    
    elif 'number' in [rule[0] for rule in token_rules]:
        result = variables['number'] + '|' + result.rstrip('|')
    elif 'id' in [rule[0] for rule in token_rules]:
        result = variables['id'] + '|' + result.rstrip('|')
    

    result = result.replace("['id']|","")
    result = result.replace("['number']|","")
    result = result.replace("['ws']|","")
    result = result.replace('return LPAREN','(') 
    result = result.replace('return RPAREN',')')
    print("result: ",result)
    
    if len(result) == 0:
        print(Fore.RED + "\nSegmentation Fault: The language definition is empty", Style.RESET_ALL)
        sys.exit(0)
    else:
        return result, token_rules
    
def Read_File(nombre_archivo):
    try:
        # Abre el archivo en modo de lectura
        with open(nombre_archivo, 'r') as archivo:
            # Lee todas las líneas del archivo y guarda cada línea en una lista
            lineas = archivo.readlines()
        # Retorna la lista de líneas
        lineas = [linea.replace("\n", "") for linea in lineas]
        return lineas
    except FileNotFoundError:
        print(Fore.RED + f"\nThe file '{nombre_archivo}' was not found ", Style.RESET_ALL)
        sys.exit(0)
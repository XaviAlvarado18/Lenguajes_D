# Nombre: Kristopher Javier Alvarado López
# Carnet: 21188
# Archivo: converter.py


from typing import *
from Classes_ import FormatPointer


def is_operator(token):
    operators = "|?.+*^"
    return token in operators


def precedence(operator: str) -> int:
    return {
        '(': 1, ')': 1, '[': 1, ']': 1, '{': 1, '}': 1,
        '|': 2, '.': 3, '?': 4, '*': 4, '+': 4, '^': 5, '∗': 4,
    }.get(operator, -1)


def counterSymbol(character: str) -> str:
    return {
        '(': ')',
        '[': ']',
        '{': '}',
        ')': '(',
        ']': '[',
        '}': '{',
    }.get(character, ' ')


def is_binary(token):
    operators = "^|"
    return token in operators


def extract_alphabet(content: List[str]) -> List[str]:
    """Extracts the alphabet from the regular expressions"""
    alphabet: List[str] = []
    for expression in content:
        alphabets = {x for x in expression if x not in '[]{}|?ε'}
        alphabet.append(''.join(alphabets))

    new_alphabet = []
    i = 0
    while i < len(alphabet):
        if alphabet[i] == "'":
            new_alphabet.append(str(ord(alphabet[i])))
        elif alphabet[i] == ' ':
            new_alphabet.append(str(ord(alphabet[i])))

        elif alphabet[i] == '\\':
            # Manejando los caracteres de escape \t y \n
            if alphabet[i+1] == 't':
                new_alphabet.append(str(ord('\t')))
                i += 1  # Saltar el siguiente caracter '\t'
            elif alphabet[i+1] == 'n':
                new_alphabet.append(str(ord('\n')))
                i += 1  # Saltar el siguiente caracter '\n'
        else:
            new_alphabet.append(alphabet[i])  # Agregar el caracter sin modificar
        i += 1

    return new_alphabet


def format_regex(expression):
    """Formats the regular expressions to be used in the program"""

    formatted: List[str] = []

    def format_(expression_: str) -> str:
        
    
        
        if '[' in expression_ and ']' in expression_ and '?' not in expression_ and '+' not in expression_:
            return expression_
        
        if "'" in expression_ and '?' not in expression_ and ']+' not in expression_:
            return expression_

        pointer: FormatPointer = FormatPointer()
        operators = '*|?+'  # Operators that can be used in the regular expression

        

        if ']?' in expression_ or '+)?' in expression_ or ')?' in expression_:
            entre_comillas = False
            entre_corchetes = False


            for i in range(len(expression_)):
                c1 = expression_[i]
                c2 = "*"

                if c1 == '[':
                    c3 = expression_[i+2]
                    if c3 == ']':
                        entre_corchetes = True
                    else:
                        entre_corchetes = False

                if c1 == "'":
                    c3 = expression_[i+1]
                    if c3 == '+':
                        entre_comillas = True
                    else:
                        entre_comillas = False
                

                if not entre_comillas and not entre_corchetes and c1.isalpha():
                    c1 = f".{c1}."

                if i + 1 < len(expression_):
                    c2 = expression_[i + 1]
                    

                if c1 == '?':
                    pointer.interrogation2()
                elif c1 == '+' and not entre_comillas:
                    pointer.plus()
                else:
                    if c1 not in "({)}":
                        pointer.push(c1)


            result = pointer.__str__()

            if '[0]' in result:
                result = result.replace('[0]', '([0]')

            if '[]|[]' in result:
                result = result.replace('[]|[]','[(]|[)]')


            return result
        

        elif ']+' in expression_:
            for i in range(len(expression_)):
                c1 = expression_[i]
                c2 = "*"

                if i + 1 < len(expression_):
                    c2 = expression_[i + 1]

                if c1 == '+':
                    pointer.plus()
                else:
                    if c1 not in '({)}':
                        pointer.push(c1)

            result = pointer.__str__()

            return result
        else:
            for i in range(len(expression_)):
                c1 = expression_[i]
                c2 = "*"

                if i + 1 < len(expression_):
                    c2 = expression_[i + 1]

                if c1 in '([{':
                    pointer.inGroup()
                elif c1 in ')]}':
                    pointer.outGroup()

                if c1 == '?':
                    pointer.interrogation()
                elif c1 == '+':
                    pointer.plus()
                else:
                    if c1 not in '([{)]}':
                        pointer.push(c1)

                if c1 not in '|' and c2 not in operators and c2 not in ')]}':

                    if c1 not in '([{':
                        c = pointer.actual.stack.pop()
                        pointer.push(c+'.')

            result = pointer.__str__()

            

            return result
    

    def testing_(express):
        for i in range(1):
            if '[' in express and ']' in express:
                next_symbol = ""
                # Si hay corchetes, realizar un split
                start_index = express.find('[')
                end_index = express.find(']')
                if end_index + 1 < len(express):
                    next_symbol = express[end_index + 1]
                
                first_part = express[start_index:end_index + 1]

                formatted_expression = first_part 
                if next_symbol:
                    if next_symbol not in ('+','?','*','|'):
                        formatted_expression += '.'
                    elif next_symbol in ('?') and end_index + 2 < len(express):
                        if '+' or '?' in express[end_index + 2:]:
                            end_index_interrogation = express.find('?')
                            expression_aux = format_(express[end_index + 2:end_index_interrogation+1])
                            if end_index_interrogation < len(express):
                                formatted.append(format_(express[start_index:end_index + 2]) + "." + format_(expression_aux)+format_(express[end_index_interrogation+1:])+".")
                                #print("Esto: ",express[end_index_interrogation+1:])
                                break
                            formatted.append(format_(express[start_index:end_index + 2]) + "." + format_(expression_aux))
                            break
                        formatted.append(format_(express[start_index:end_index + 2]) + "." + format_(express[end_index + 2:]))
                        break
                    elif next_symbol in ('?'):
                        formatted.append(format_(express[start_index:end_index + 2]))
                        break
                    
                    elif next_symbol in ('+') and end_index + 2 < len(express):
                        if '+' or '?' in express[end_index + 2:]:
                            end_index_interrogation = express.find('?')
                            expression_aux = format_(express[end_index + 2:end_index_interrogation+1])
                            if end_index_interrogation < len(express):
                                formatted.append(format_(express[start_index:end_index + 2]) + "." + format_(expression_aux)+format_(express[end_index_interrogation+1:])+".")
                                #print("Esto: ",express[end_index_interrogation+1:])
                                break
                            formatted.append(format_(express[start_index:end_index + 2]) + "." + format_(expression_aux))
                            break
                        formatted.append(format_(express[start_index:end_index + 2]) + "." + format_(express[end_index + 2:]))
                        #print("expression[start_index:end_index + 2]: ",express[start_index:end_index + 2:])
                        break

                    elif next_symbol in ('+'):
                        formatted.append(format_(express[start_index:end_index + 2]))
                        #print("format_(expression[start_index:end_index + 2]): ",format_(express[start_index:end_index + 2]))
                        break

                    if first_part == '[0]':
                        expresion_modificada = express.replace('[0]','([0]').replace('[9]','[9])')

                        

                        #print("modified: ", expresion_modificada)
                        formatted.append(format_(expresion_modificada))
                        
                    else: formatted.append('('+formatted_expression + format_(express[end_index + 1:]))
                else:
                    first_part = express[0:start_index]
                    formatted.append(format_(first_part) + "." + format_(express[start_index:end_index+1]))
            else:
                exp = expression.replace('{', '(').replace('}', ')')
                # Aplicar el formato solo si no hay corchetes
                formatted.append(format_(exp))

    
    testing_(expression)
            
        

    return formatted


def translate_to_postfix(content: List[str]) -> List[str]:
    postfix_format: List[str] = []



    def infix_to_postfix(regex):
        postfix = ""
        postfix_stack = []
        escape_char = False
        inside_square_brackets = False

        for character in regex:
            if character == '\\':
                escape_char = True
            elif character == ' ':
                escape_char = True
            elif character == '[':
                inside_square_brackets = True
                postfix += character
            elif character == ']':
                inside_square_brackets = False
                postfix += character
            elif character in '{([' and not inside_square_brackets:
                postfix_stack.append(character)
            elif character in '})]' and not inside_square_brackets:
                while postfix_stack and postfix_stack[-1] != counterSymbol(character):
                    postfix += postfix_stack.pop()
                postfix_stack.pop()  # Eliminar el paréntesis izquierdo '(' de la pila
            else:
                if (not is_operator(character) and not is_binary(character)) or escape_char or inside_square_brackets:
                    escape_char = False
                    postfix += character
                else:
                    while postfix_stack:
                        picked_char = postfix_stack[-1]
                        pd_picked_char = precedence(picked_char)
                        pd_actual_char = precedence(character)
                        if pd_picked_char >= pd_actual_char:
                            postfix += postfix_stack.pop()
                        else:
                            break
                    postfix_stack.append(character)

        while postfix_stack:
            postfix += postfix_stack.pop()

        return postfix

    for expression in content:
        postfix_format.append(infix_to_postfix(expression))

    if '*[0]' in postfix_format[0]:
        postfix_format[0] = postfix_format[0].replace('*[0]',"*['.'][0]|")
    if '.εE' in postfix_format[0]:
        postfix_format[0] = postfix_format[0].replace('.εE','ε.E.')
    if '|ε[0]' in postfix_format[0]:
        postfix_format[0] = postfix_format[0].replace('|ε[0]','|ε.[0]')
    if '|[]*' in postfix_format[0]:
        postfix_format[0] = postfix_format[0].replace('|[]*','*')
    if '[_*]*|'in postfix_format[0]:
        postfix_format[0] = postfix_format[0].replace('[_*]*|','[_*]|*')
    if '[z]*|'in postfix_format[0]:
        postfix_format[0] = postfix_format[0].replace('[z]*|','[z]|*')
    if "['id']|" in postfix_format[0]:
        postfix_format[0] = postfix_format[0].replace("['id']|",'')
    if "[9]]." in postfix_format[0]:
        postfix_format[0] = postfix_format[0].replace("[9]].",'[9]')
    if "[9]|+" in postfix_format[0]:
        postfix_format[0] = postfix_format[0].replace("[9]|+",'[9]|')
    if "['+''-']" in postfix_format[0]:
        postfix_format[0] = postfix_format[0].replace("['+''-']","['+']-|.['-']")
    if "|ε.[0][1]|[2]|[3]|[4]|[5]|[6]|[7]|[8]|[9]|*|ε" in postfix_format[0]:
        postfix_format[0] = postfix_format[0].replace("|ε.[0][1]|[2]|[3]|[4]|[5]|[6]|[7]|[8]|[9]|*|ε","|ε[0][1]|[2]|[3]|[4]|[5]|[6]|[7]|[8]|[9]|*..|ε")



    return postfix_format


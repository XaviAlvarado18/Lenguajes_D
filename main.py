# Nombre: Kristopher Javier Alvarado López
# Carnet: 21188
# Archivo: main.py

from reader import Read_Yal, Read_File
from converter import extract_alphabet,format_regex, translate_to_postfix
from Tree_ import make_direct_tree
from AFD import make_direct_AFD
from draw import draw_tree, draw_AF
from Simulator import Simulator

def main():
    # Read the file and return its contents
    token_rules = []
    expression, token_rules = Read_Yal('slr-2')  
    
    # Format the regular expression
    formatted_expression = format_regex(expression)
    print("Formatted expression:", formatted_expression)

    # Translate the formatted expression to postfix
    postfix_expression = translate_to_postfix(formatted_expression)
    print("Postfix expression:", postfix_expression[0])

    # Build a direct tree from the postfix expression
    direct_tree, nodes = make_direct_tree(postfix_expression[0])
    draw_tree(direct_tree)


    # Build a direct AFD from the direct tree
    alphabets = extract_alphabet(expression)  # You need to define the extract_alphabet function
    direct_states, direct_initS, total_d = make_direct_AFD(direct_tree, nodes, alphabets)

    #print("ALPHA: ", alphabets)

    # Draw the direct AFD
    draw_AF(direct_initS, legend='AFD direct', expression='default', direct=True, name='AFD_direct')

    ListInputs = Read_File('input.txt')
    print("Lista de inputs: ", ListInputs)

    afDict = {
        #'FNA': afnInit,
        #'FDA': afdN_Init['q0'],
        #'Minimized FDA': initMAFD,
        'Direct FDA': direct_initS,
    }

    print("Welcome to the regex evaluator - ")
    for input in ListInputs:
        print(f"\nString to evaluate: '{input}'")
        simulationResult, _paths = Simulator(afDict, input, token_rules)
    
    

if __name__ == '__main__':
    main()

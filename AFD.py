from Classes_ import State, Node
from typing import *


def make_direct_AFD(tree: Node, nodes: Dict[str, Node], alpha: str):
    states: Dict[Tuple[str, ...], State] = {tuple(tree.first_pos): State('q0')}
    toEvaluate: List[Tuple[str, ...]] = [tuple(tree.first_pos)]
    total_states: Dict[str, State] = dict()
    total_states['q0'] = states[tuple(tree.first_pos)]
    finalState: str = ''
    for state in nodes:
        #print("states?:", nodes[state].value)
        #print("Tipo de datos de nodes[state].value:", type(nodes[state].value))
        if nodes[state].value == '#':
            

            finalState = state
            break
    gen = 1

    while len(toEvaluate) > 0:
        actualState: Tuple[str, ...] = toEvaluate[0]
        if len(toEvaluate) > 1:
            toEvaluate = toEvaluate[1:]
        else:
            toEvaluate.clear()

        for letter in alpha:
            #print("alpha: ", alpha)
            nextState_st: Set[str] = set()
            for state in actualState:
                #print("states?:", nodes[state].value)
                
                # Verificar el tipo de datos de nodes[state].value
                if nodes[state].value.strip("'") == letter:
                    #print("Este es:", nodes[state].value)
                    nextState_st = nextState_st.union(nodes[state].follow_pos)
            if len(nextState_st) <= 0:
                continue
            nextState: Tuple[str, ...] = tuple(nextState_st)
            if nextState not in states:
                states[nextState] = State('q' + str(gen))
                total_states['q' + str(gen)] = states[nextState]
                if finalState in nextState_st:
                    states[nextState].isFinalState = True
                toEvaluate.append(nextState)
                gen += 1
            states[actualState].add_transition(letter, states[nextState])

    for state in states:
        if finalState in state:
            states[state].isFinalState = True

    return states, states[tuple(tree.first_pos)], total_states

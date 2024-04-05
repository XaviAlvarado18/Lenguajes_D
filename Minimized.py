from Classes_ import State
from typing import *


def minimizeAFD(states2: Dict[str, State], alpha: str):
    initSt = states2['q0']
    initState = tuple([states2[x] for x in states2 if not states2[x].isFinalState])
    finalState = tuple([states2[x] for x in states2 if states2[x].isFinalState])
    minimized_states: Dict[str, Tuple[State, ...]] = {'Q0': initState, 'Q1': finalState}

    not_toDo = True

    while not_toDo:
        evaluated = 1
        new_minimized_states: Dict[str, Tuple[State, ...]] = dict()
        for subStates in minimized_states:
            transitionsDict: Dict[str, Set[State]] = dict()
            for minState in minimized_states[subStates]:
                transitions: List[Tuple[str, str]] = []
                for letter in alpha:
                    if len(minState.getStates(letter)) <= 0:
                        pass
                    else:
                        newState = minState.getStates(letter).copy().pop()
                        for subStates2 in minimized_states:
                            if newState in minimized_states[subStates2]:
                                transition: Tuple[str, str] = (subStates2, letter)
                                transitions.append(transition)

                tupleTransitions: str = str(transitions)
                if tupleTransitions in transitionsDict:
                    transitionsDict[tupleTransitions].add(minState)
                else:
                    transitionsDict[tupleTransitions] = {minState}

            for transition_ in transitionsDict:
                if initSt in transitionsDict[transition_]:
                    new_minimized_states['Q' + str(0)] = tuple(transitionsDict[transition_])
                    continue
                new_minimized_states['Q' + str(evaluated)] = tuple(transitionsDict[transition_])
                evaluated += 1

        if new_minimized_states == minimized_states:
            not_toDo = False
        else:
            minimized_states = new_minimized_states

    newMin_States: Dict[str, State] = dict()
    initial = ''
    for subStates in minimized_states:
        index = subStates

        if states2['q0'] in minimized_states[subStates]:
            initial = index
        newMin_States[index] = State(index)

        for minState in minimized_states[subStates]:
            if minState.isFinalState:
                newMin_States[index].isFinalState = True
                break

    for subStates in minimized_states:
        index = subStates
        tryState: State = tuple(minimized_states[subStates])[0]
        newMinState: State = newMin_States[index]

        for letter in alpha:
            if len(tryState.getStates(letter)) <= 0:
                continue

            tranState = tryState.getStates(letter).copy().pop()
            for subStates2 in minimized_states:
                if tranState in minimized_states[subStates2]:
                    newMinState.add_transition(letter, newMin_States[subStates2])
                    break

    newMin_States[initial].value = 'Q0'

    return newMin_States, newMin_States[initial]

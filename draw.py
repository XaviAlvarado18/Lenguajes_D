from Classes_ import *
import graphviz


def draw_tree(f_node: Node, expression='default', direct=False):
    dot = graphviz.Digraph(comment='Tree')

    def draw_node(node: Node):
        label = chr(node.value) if isinstance(node.value, int) else str(node.value)
        dot.node(str(node.getId()), label=label)
        if node.left is not None:
            dot.edge(str(node.getId()), str(node.left.getId()))
            draw_node(node.left)
        if node.right is not None:
            dot.edge(str(node.getId()), str(node.right.getId()))
            draw_node(node.right)

    draw_node(f_node)

    dot.render('Syntax_Tree.gv', view=True, directory='./Tree/'+expression+'/'+('Direct' if direct else 'Infix'))


def draw_AF(initState: State, legend: str = 'AF', expression='default', direct=False, name='AFN'):
    dot: 'graphviz.graphs.Digraph' = graphviz.Digraph(comment='AFN')
    dot.attr(rankdir='LR')
    setStates = set()

    dot.attr(label=legend)

    def draw_state(state: 'State'):
        setStates.add(state.getId())
        label = str(state.value) if isinstance(state.value, int) else state.value
        dot.node(state.getId(), label=label, shape='doublecircle' if state.isFinalState else 'circle')
        for transition in state.transitions:
            #print(transition)
            for destiny in state.transitions[transition]:
                if destiny.getId() not in setStates:
                    draw_state(destiny)
                if transition == '43':
                    dot.edge(state.getId(), destiny.getId(), label='+')
                else: 
                    dot.edge(state.getId(), destiny.getId(), label=str(transition))


    draw_state(initState)

    dot.render(name+'.gv', view=True, directory='./Tree/'+expression+'/'+('Direct' if direct else 'Infix'))

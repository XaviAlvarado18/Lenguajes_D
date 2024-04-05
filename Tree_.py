from Classes_ import Node
from typing import *


from typing import Union, List

def make_tree(expression: str) -> Node:
    stack = []
    id_ = 1
    is_inside_square_brackets = False
    current_square_brackets_content = ""

    for char in expression:
        if char == '[':
            is_inside_square_brackets = True
            current_square_brackets_content = ""
        elif char == ']':
            is_inside_square_brackets = False
            # Crear un nodo para representar el conjunto y añadirlo a la pila
            stack.append(Node(current_square_brackets_content, id_=id_))
            stack[-1].is_nullable = False
            stack[-1].first_pos.add(id_)
            stack[-1].last_pos.add(id_)
            id_ += 1
        elif is_inside_square_brackets:
            current_square_brackets_content += char
        elif char == '.':
            right = stack.pop()
            left = stack.pop()
            stack.append(Node(char, left, right))
            stack[-1].is_nullable = left.is_nullable and right.is_nullable
            if left.is_nullable:
                stack[-1].first_pos = left.first_pos.union(right.first_pos)
            else:
                stack[-1].first_pos = left.first_pos
            if right.is_nullable:
                stack[-1].last_pos = left.last_pos.union(right.last_pos)
            else:
                stack[-1].last_pos = right.last_pos
        elif char == '|':
            right = stack.pop()
            left = stack.pop()
            stack.append(Node(char, left, right))
            stack[-1].is_nullable = left.is_nullable or right.is_nullable
            stack[-1].first_pos = left.first_pos.union(right.first_pos)
            stack[-1].last_pos = left.last_pos.union(right.last_pos)
        elif char == '*':
            left = stack.pop()
            stack.append(Node(char, left))
            stack[-1].is_nullable = True
            stack[-1].first_pos = left.first_pos
            stack[-1].last_pos = left.last_pos
        else:
            stack.append(Node(char, id_=id_))
            stack[-1].is_nullable = char == 'ε'
            stack[-1].first_pos.add(id_)
            stack[-1].last_pos.add(id_)
            id_ += 1
    return stack.pop()



def make_direct_tree(expression: str) -> Tuple[Node, Dict[str, Node]]:
    
    expression = expression + '#.'
    nodes: Dict[str, Node] = {}
    
    tree_node = make_tree(expression)

    def explore_node(node: Node):
        if node.value == '.':
            explore_node(node.left)
            explore_node(node.right)
        elif node.value == '|':
            explore_node(node.left)
            explore_node(node.right)
        elif node.value == '*':
            explore_node(node.left)
        else:
            nodes[node.id_] = node

    def explore_followPos(node: Node):
        if node.value == '.':
            for element in node.left.last_pos:
                nodes[element].follow_pos = nodes[element].follow_pos.union(node.right.first_pos)
            explore_followPos(node.left)
            explore_followPos(node.right)
        elif node.value == '*':
            for element in node.last_pos:
                nodes[element].follow_pos = nodes[element].follow_pos.union(node.first_pos)
            explore_followPos(node.left)
        elif node.value == '|':
            explore_followPos(node.left)
            explore_followPos(node.right)

    explore_node(tree_node)
    explore_followPos(tree_node)
    return tree_node, nodes

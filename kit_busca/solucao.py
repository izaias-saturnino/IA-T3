import queue
import time
from typing import Iterable, Set, Tuple
from copy import deepcopy

class Nodo:
    """
    Implemente a classe Nodo com os atributos descritos na funcao init
    """
    def __init__(self, estado:str, pai, acao:str, custo:int):
        """
        Inicializa o nodo com os atributos recebidos
        :param estado:str, representacao do estado do 8-puzzle
        :param pai:Nodo, referencia ao nodo pai, (None no caso do nó raiz)
        :param acao:str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
        :param custo:int, custo do caminho da raiz até este nó
        """
        # substitua a linha abaixo pelo seu codigo
        self.estado = estado
        self.acao = acao
        self.custo = custo
        self.pai = pai
    def __lt__(self, other):
        return 0< 1

def matrix_to_string(matrix):
    col_string = ["", "", ""]
    for i in range(3):
        for j in range(3):
            matrix[i][j] = str(matrix[i][j])
        row_string = "".join(matrix[i])
        col_string[i] = row_string
    return str("".join(col_string))

def sucessor(estado:str)->Set[Tuple[str,str]]:
    """
    Recebe um estado (string) e retorna um conjunto de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado:
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    
    estado_list = list(estado)

    matrix = [["0","0","0"],
              ["0","0","0"],
              ["0","0","0"]]
    for i in range(3):
        for j in range(3):
            matrix[i][j] = estado_list[3*i+j]
    
    action_state_tuple_list = []

    for i in range(3):
        for j in range(3):
            if matrix[i][j] == "_":
                if i > 0:
                    action_matrix = deepcopy(matrix)
                    action_matrix[i][j], action_matrix[i-1][j] = action_matrix[i-1][j], action_matrix[i][j]
                    action_state_tuple_list.append(("acima", matrix_to_string(action_matrix)))
                if i < 2:
                    action_matrix = deepcopy(matrix)
                    action_matrix[i][j], action_matrix[i+1][j] = action_matrix[i+1][j], action_matrix[i][j]
                    action_state_tuple_list.append(("abaixo", matrix_to_string(action_matrix)))
                if j > 0:
                    action_matrix = deepcopy(matrix)
                    action_matrix[i][j], action_matrix[i][j-1] = action_matrix[i][j-1], action_matrix[i][j]
                    action_state_tuple_list.append(("esquerda", matrix_to_string(action_matrix)))
                if j < 2:
                    action_matrix = deepcopy(matrix)
                    action_matrix[i][j], action_matrix[i][j+1] = action_matrix[i][j+1], action_matrix[i][j]
                    action_state_tuple_list.append(("direita", matrix_to_string(action_matrix)))
    return action_state_tuple_list

def expande(nodo:Nodo)->Set[Nodo]:
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um conjunto de nodos.
    Cada nodo do conjunto é contém um estado sucessor do nó recebido.
    :param nodo: objeto da classe Nodo
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    node_list = []
    action_state_tuple_list = sucessor(nodo.estado)
    for action, state in action_state_tuple_list:
        node_list.append(Nodo(state, nodo, action, nodo.custo+1))
    return node_list

def hamming_distance(estado_atual):
    estado_final = "12345678_"
    distance = 0
    for i in range(len(estado_atual)):
        if(estado_atual[i] != estado_final[i] and estado_atual[i] != "_"):
            distance += 1
    return distance

def manhattan_distance(estado_atual):
    estado_list = list(estado_atual)

    matrix = [[0,0,0],
              [0,0,0],
              [0,0,0]]
    
    for i in range(3):
        for j in range(3):
            if estado_list[3*i+j] == "_":
                estado_list[3*i+j] = "9"
            matrix[i][j] = int(estado_list[3*i+j])

    distance = 0

    for i in range(3):
        for j in range(3):
            currentCol = j
            current_row = i
            expectedCol = (matrix[i][j] - 1) % 3
            expected_row = ((matrix[i][j] - 1) - expectedCol)/3 - 1

            row_diff = current_row - expected_row
            if row_diff < 0:
                row_diff = -row_diff

            col_diff = currentCol - expectedCol
            if col_diff < 0:
                col_diff = -col_diff

            distance += row_diff + col_diff

    return distance

def get_action_list(nodo:Nodo):
    action_list = []

    while(nodo.pai != None):
        action_list.insert(0, nodo.acao)
        nodo = nodo.pai

    return action_list

def print_node(nodo:Nodo):
    print(nodo.estado)
    print(nodo.acao)
    print(nodo.custo)

def print_node_list(node_list:list[Nodo]):
    for node in node_list:
        print("node_list item")
        print_node(node)
    print("node_list end")

def astar_hamming(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    start = time.time()
    expanded_nodes = 0
    estado_final = "12345678_"
    
    x = set(())
    f = queue.PriorityQueue()
    v = Nodo(estado, None, None, 0)
    f.put((v.custo + hamming_distance(v.estado),v))

    while not f.empty():
        (_,v) = f.get()
        if(v.estado == estado_final):
            end = time.time()
            print("estado")
            print(estado)
            print("expanded_nodes")
            print(expanded_nodes)
            print("cost")
            print(v.custo)
            print("time")
            print(end-start)
            return get_action_list(v)
        if(v.estado not in x):
            x.add(v.estado)
            node_list = expande(v)
            expanded_nodes += 1
            for node in node_list:
                if(node.estado not in x):
                    f.put((node.custo + hamming_distance(node.estado),node))
        end = time.time()
    print("estado")
    print(estado)
    print("expanded_nodes")
    print(expanded_nodes)
    print("cost")
    print(v.custo)
    print("time")
    print(end-start)
    return None

def astar_manhattan(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    start = time.time()
    expanded_nodes = 0
    estado_final = "12345678_"
    
    x = set(())
    f = queue.PriorityQueue()
    v = Nodo(estado, None, None, 0)
    f.put((v.custo + manhattan_distance(v.estado),v))

    while not f.empty():
        (_,v) = f.get()
        if(v.estado == estado_final):
            end = time.time()
            print("estado")
            print(estado)
            print("expanded_nodes")
            print(expanded_nodes)
            print("cost")
            print(v.custo)
            print("time")
            print(end-start)
            return get_action_list(v)
        if(v.estado not in x):
            x.add(v.estado)
            node_list = expande(v)
            expanded_nodes += 1
            for node in node_list:
                if(node.estado not in x):
                    f.put((node.custo + manhattan_distance(node.estado),node))
        end = time.time()
    print("estado")
    print(estado)
    print("expanded_nodes")
    print(expanded_nodes)
    print("cost")
    print(v.custo)
    print("time")
    print(end-start)
    return None

def bfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em LARGURA e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError


def dfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError

def astar_new_heuristic(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = sua nova heurística e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError

def main():
    str="2_3541687"
    astar_hamming(str)
    astar_manhattan(str)

if __name__ == '__main__':
    main()
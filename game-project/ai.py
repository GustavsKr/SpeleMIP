from __future__ import annotations
from typing import List, Tuple, Dict, Optional

# State ir tuple ar 7 veseliem skaitļiem, kas glabā spēles stāvokli:
# (c1, c2, c3, c4, p1, p2, player)
# c1..c4 = katras bumbiņas vērtības atlikums virknē
# p1 = Player 1 punkti
# p2 = Player 2 punkti
# player = kurš spēlētājs ir gājienā (1 vai 2)
State = Tuple[int, int, int, int, int, int, int]

# -----------------------------
# SPĒLES KOKA DATU STRUKTŪRA
# -----------------------------
class Node:
    """Spēles koka mezgls"""
    def __init__(self, state: State, player: int):
        self.state = state          # pašreizējais spēles stāvoklis
        self.player = player        # kurš spēlētājs ir gājienā
        self.children: List[Node] = []  # saraksts ar zariem (nākotnes stāvokļi)
        self.value: Optional[int] = None  # heiristiskā vērtība šim mezglam
        self.move: Optional[int] = None   # gājiens, kas noved pie šī mezgla

# -----------------------------
# Heiristiskā novērtējuma funkcija
# -----------------------------
def _evaluate(p1, p2, c1, c2, c3, c4, player, limit=70) -> int:
    """
    Aprēķina heiristisko vērtību dotajam stāvoklim.
    Mērķis: palikt virs 70 un pēc iespējas tuvāk limitam.
    Ņem vērā:
      - Punktu starpību
      - Labāko nākotnes gājienu
      - Paritātes bonusu bumbiņām
    """
    score_diff = p2 - p1 if player == 2 else p1 - p2
    best_local = -10**9 if player == 2 else 10**9

    # Iet cauri katrai bumbiņas vērtībai
    for pick in [1, 2, 3, 4]:
        count = {1: c1, 2: c2, 3: c3, 4: c4}[pick]
        if count == 0:
            continue

        # Aprēķina nākamo stāvokli pēc izvēlētā gājiena
        nxt_state = _apply_pick(c1, c2, c3, c4, p1, p2, player, pick)
        _, _, _, _, nxt_p1, nxt_p2, _ = nxt_state
        my_score = nxt_p2 if player == 2 else nxt_p1
        distance = abs(my_score - limit)
        score = 0

        # Heiristikas aprēķins
        if my_score < limit:
            score -= 3000 + (100 * distance)
        else:
            score += 200 - distance
            if my_score == limit:
                score += 5000

        # Maksimizācija / minimizācija
        if player == 2:
            best_local = max(best_local, score)
        else:
            best_local = min(best_local, score)

    # Paritātes bonuss (pāra skaitļi plus, nepāra skaitļi mīnuss)
    parity_bonus = c2 * 2 + c4 * 4 - c1 - c3

    # Gala heuristiskā vērtība
    return score_diff * 2 + best_local * 3 + parity_bonus

# -----------------------------
# Funkcija iespējamajiem gājieniem
# -----------------------------
def _moves(c1, c2, c3, c4) -> List[int]:
    """Atgriež sarakstu ar iespējamiem gājieniem, atkarībā no atlikušajām bumbiņām"""
    moves = []
    if c1 > 0: moves.append(1)
    if c2 > 0: moves.append(2)
    if c3 > 0: moves.append(3)
    if c4 > 0: moves.append(4)
    return moves

# -----------------------------
# Funkcija gājiena piemērošanai
# -----------------------------
def _apply_pick(c1, c2, c3, c4, p1, p2, player, pick):
    """
    Atjaunina stāvokli pēc gājiena izvēles.
    Ņem vērā spēlētāja identitāti un noteikumus:
      - Nepāra bumbas (+ pretinieka punkti)
      - Pāra bumbas (- savi punkti)
    Atgriež jaunu State un maina spēlētāju.
    """
    if pick == 1:
        c1 -= 1
        if player == 1: p2 += 1
        else: p1 += 1
    elif pick == 2:
        c2 -= 1
        if player == 1: p1 -= 4
        else: p2 -= 4
    elif pick == 3:
        c3 -= 1
        if player == 1: p2 += 3
        else: p1 += 3
    elif pick == 4:
        c4 -= 1
        if player == 1: p1 -= 8
        else: p2 -= 8

    p1 = max(p1, 0)
    p2 = max(p2, 0)
    next_player = 2 if player == 1 else 1
    return (c1, c2, c3, c4, p1, p2, next_player)

# -----------------------------
# Rekursīvs Minimax ar Node
# -----------------------------
def build_minimax_tree(node: Node, depth: int, memo: Dict[Tuple[State, int], int]):
    """
    Rekursīvi veido Minimax koku līdz noteiktam dziļumam.
    Saglabā mezglu bērnus un heuristiskās vērtības.
    Memoizācija novērš atkārtotus aprēķinus.
    """
    key = (node.state, depth)
    if key in memo:
        node.value = memo[key]
        return node.value

    c1, c2, c3, c4, p1, p2, player = node.state

    # Bāzes gadījumi: tukša virkne, dziļuma limits, punkti < 70
    if (c1 + c2 + c3 + c4) == 0 or depth == 0 or p1 < 70 or p2 < 70:
        node.value = _evaluate(p1, p2, c1, c2, c3, c4, player)
        memo[key] = node.value
        return node.value

    possible = _moves(c1, c2, c3, c4)
    if not possible:
        node.value = _evaluate(p1, p2, c1, c2, c3, c4, player)
        memo[key] = node.value
        return node.value

    # Rekursīvi izvērtē bērnus
    if player == 1:
        best_val = -10**9
        for move in possible:
            nxt_state = _apply_pick(c1, c2, c3, c4, p1, p2, player, move)
            child = Node(nxt_state, nxt_state[6])
            node.children.append(child)
            val = build_minimax_tree(child, depth - 1, memo)
            if val > best_val:
                best_val = val
                node.move = move
        node.value = best_val
    else:
        best_val = 10**9
        for move in possible:
            nxt_state = _apply_pick(c1, c2, c3, c4, p1, p2, player, move)
            child = Node(nxt_state, nxt_state[6])
            node.children.append(child)
            val = build_minimax_tree(child, depth - 1, memo)
            if val < best_val:
                best_val = val
                node.move = move
        node.value = best_val

    memo[key] = node.value
    return node.value

# -----------------------------
# Rekursīvs Alpha-Beta ar Node
# -----------------------------
def build_alphabeta_tree(node: Node, depth: int, alpha: int, beta: int, memo: Dict[Tuple[State, int], int]):
    """
    Rekursīvi veido Alpha-Beta koku līdz noteiktam dziļumam.
    Ievieš pruning (alpha-beta) un memoizāciju.
    """
    key = (node.state, depth)
    if key in memo:
        node.value = memo[key]
        return node.value

    c1, c2, c3, c4, p1, p2, player = node.state

    # Bāzes gadījumi
    if (c1 + c2 + c3 + c4) == 0 or depth == 0 or p1 < 70 or p2 < 70:
        node.value = _evaluate(p1, p2, c1, c2, c3, c4, player)
        memo[key] = node.value
        return node.value

    possible = _moves(c1, c2, c3, c4)
    if not possible:
        node.value = _evaluate(p1, p2, c1, c2, c3, c4, player)
        memo[key] = node.value
        return node.value

    if player == 1:
        value = -10**9
        for move in possible:
            nxt_state = _apply_pick(c1, c2, c3, c4, p1, p2, player, move)
            child = Node(nxt_state, nxt_state[6])
            node.children.append(child)
            val = build_alphabeta_tree(child, depth - 1, alpha, beta, memo)
            if val > value:
                value = val
                node.move = move
            alpha = max(alpha, value)
            if alpha >= beta:  # pruning
                break
        node.value = value
    else:
        value = 10**9
        for move in possible:
            nxt_state = _apply_pick(c1, c2, c3, c4, p1, p2, player, move)
            child = Node(nxt_state, nxt_state[6])
            node.children.append(child)
            val = build_alphabeta_tree(child, depth - 1, alpha, beta, memo)
            if val < value:
                value = val
                node.move = move
            beta = min(beta, value)
            if alpha >= beta:  # pruning
                break
        node.value = value

    memo[key] = node.value
    return node.value

# -----------------------------
# Comouter chooses move based on algorithm and heuretic
# -----------------------------
def choose_move(sequence: List[int], p1: int, p2: int, current_player: int, algorithm="alphabeta", depth: int = 4) -> int:
    """
    Izvēlas labāko gājienu no dotās virknēs un punktiem.
    sequence: saraksts ar bumbiņām (1–4)
    p1, p2: spēlētāju punkti
    current_player: kurš spēlētājs gājienā
    algorithm: 'alphabeta' vai 'minimax'
    depth: cik gājienus uz priekšu apskatīt
    Atgriež izvēlēto gājienu (1–4)
    """
    c1, c2, c3, c4 = sequence.count(1), sequence.count(2), sequence.count(3), sequence.count(4)
    state = (c1, c2, c3, c4, p1, p2, current_player)
    root = Node(state, current_player)
    memo: Dict[Tuple[State, int], int] = {}

    if algorithm == "alphabeta":
        build_alphabeta_tree(root, depth, -10**9, 10**9, memo)
    else:
        build_minimax_tree(root, depth, memo)

    return root.move


# https://chatgpt.com/share/69b2f796-2cbc-8010-9b04-14cfceff0d98 (minimax algoritms)
# https://chatgpt.com/share/69bf2a18-881c-8010-aa82-28c8eac65b9b (heuristiskā funkcija)
# https://chatgpt.com/share/69bfcfa6-4034-8008-9d44-ce4bbefba8be (koka ģenerēšana)
# https://chatgpt.com/share/69bfecaf-a9e4-8008-93cb-6e1edb2a5717
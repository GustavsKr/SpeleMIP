from __future__ import annotations
from typing import List, Tuple, Dict, Optional

# ---------------------------------
# State definīcija
# ---------------------------------
State = Tuple[int, int, int, int, int, int, int]
# (c1, c2, c3, c4, p1, p2, player)

# ---------------------------------
# Spēles koks
# ---------------------------------
class Node:
    def __init__(self, state: State, player: int):
        self.state = state
        self.player = player
        self.value: Optional[int] = None
        self.move: Optional[int] = None

# ---------------------------------
# Heiristiskā funkcija
# ---------------------------------
def _evaluate(p1, p2, c1, c2, c3, c4, player, limit=70) -> int:
    score_diff = p2 - p1 if player == 2 else p1 - p2
    best_local = -10**9 if player == 2 else 10**9

    for pick in [1, 2, 3, 4]:
        count = {1: c1, 2: c2, 3: c3, 4: c4}[pick]
        if count == 0:
            continue

        nxt_state = _apply_pick(c1, c2, c3, c4, p1, p2, player, pick)
        _, _, _, _, nxt_p1, nxt_p2, _ = nxt_state
        my_score = nxt_p2 if player == 2 else nxt_p1
        distance = abs(my_score - limit)

        if my_score < limit:
            score = -3000 - (100 * distance)
        else:
            score = 200 - distance
            if my_score == limit:
                score += 5000

        if player == 2:
            best_local = max(best_local, score)
        else:
            best_local = min(best_local, score)

    parity_bonus = c2 * 2 + c4 * 4 - c1 - c3
    return score_diff * 2 + best_local * 3 + parity_bonus

# ---------------------------------
# Iespējamie gājieni
# ---------------------------------
def _moves(c1, c2, c3, c4) -> List[int]:
    moves = []
    if c1 > 0: moves.append(1)
    if c2 > 0: moves.append(2)
    if c3 > 0: moves.append(3)
    if c4 > 0: moves.append(4)
    return moves

# ---------------------------------
# Piemēro gājienu
# ---------------------------------
def _apply_pick(c1, c2, c3, c4, p1, p2, player, pick):
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

# ---------------------------------
# MINIMAX
# ---------------------------------
def build_minimax_tree(node: Node, depth: int, memo: Dict[Tuple[State, int], Tuple[int, Optional[int]]]):
    key = (node.state, depth)

    if key in memo:
        node.value, node.move = memo[key]
        return node.value

    c1, c2, c3, c4, p1, p2, player = node.state

    if (c1 + c2 + c3 + c4) == 0 or depth == 0 or p1 < 70 or p2 < 70:
        node.value = _evaluate(p1, p2, c1, c2, c3, c4, player)
        memo[key] = (node.value, None)
        return node.value

    possible = _moves(c1, c2, c3, c4)

    if player == 1:
        best_val = -10**9
        best_move = None

        for move in possible:
            nxt_state = _apply_pick(c1, c2, c3, c4, p1, p2, player, move)
            child = Node(nxt_state, nxt_state[6])

            val = build_minimax_tree(child, depth - 1, memo)

            if val > best_val:
                best_val = val
                best_move = move

        node.value = best_val
        node.move = best_move

    else:
        best_val = 10**9
        best_move = None

        for move in possible:
            nxt_state = _apply_pick(c1, c2, c3, c4, p1, p2, player, move)
            child = Node(nxt_state, nxt_state[6])

            val = build_minimax_tree(child, depth - 1, memo)

            if val < best_val:
                best_val = val
                best_move = move

        node.value = best_val
        node.move = best_move

    memo[key] = (node.value, node.move)
    return node.value

# ---------------------------------
# ALPHA-BETA
# ---------------------------------
def build_alphabeta_tree(node: Node, depth: int, alpha: int, beta: int, memo: Dict[Tuple[State, int], Tuple[int, Optional[int]]]):
    key = (node.state, depth)

    if key in memo:
        node.value, node.move = memo[key]
        return node.value

    c1, c2, c3, c4, p1, p2, player = node.state

    if (c1 + c2 + c3 + c4) == 0 or depth == 0 or p1 < 70 or p2 < 70:
        node.value = _evaluate(p1, p2, c1, c2, c3, c4, player)
        memo[key] = (node.value, None)
        return node.value

    possible = _moves(c1, c2, c3, c4)

    if player == 1:
        value = -10**9
        best_move = None

        for move in possible:
            nxt_state = _apply_pick(c1, c2, c3, c4, p1, p2, player, move)
            child = Node(nxt_state, nxt_state[6])

            val = build_alphabeta_tree(child, depth - 1, alpha, beta, memo)

            if val > value:
                value = val
                best_move = move

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        node.value = value
        node.move = best_move

    else:
        value = 10**9
        best_move = None

        for move in possible:
            nxt_state = _apply_pick(c1, c2, c3, c4, p1, p2, player, move)
            child = Node(nxt_state, nxt_state[6])

            val = build_alphabeta_tree(child, depth - 1, alpha, beta, memo)

            if val < value:
                value = val
                best_move = move

            beta = min(beta, value)
            if alpha >= beta:
                break

        node.value = value
        node.move = best_move

    memo[key] = (node.value, node.move)
    return node.value

# ---------------------------------
# GALVENĀ FUNKCIJA
# ---------------------------------
def choose_move(sequence: List[int], p1: int, p2: int, current_player: int, algorithm="alphabeta", depth: int = 4) -> int:
    c1, c2, c3, c4 = sequence.count(1), sequence.count(2), sequence.count(3), sequence.count(4)

    state = (c1, c2, c3, c4, p1, p2, current_player)
    root = Node(state, current_player)

    memo: Dict[Tuple[State, int], Tuple[int, Optional[int]]] = {}

    if algorithm == "alphabeta":
        build_alphabeta_tree(root, depth, -10**9, 10**9, memo)
    else:
        build_minimax_tree(root, depth, memo)

    # fallback (drošībai)
    if root.move is None:
        possible = _moves(c1, c2, c3, c4)
        return possible[0]

    return root.move

# https://chatgpt.com/share/69b2f796-2cbc-8010-9b04-14cfceff0d98 (minimax algoritms)
# https://chatgpt.com/share/69bf2a18-881c-8010-aa82-28c8eac65b9b (heuristiskā funkcija)
# https://chatgpt.com/share/69bfcfa6-4034-8008-9d44-ce4bbefba8be (koka ģenerēšana)
# https://chatgpt.com/share/69bfecaf-a9e4-8008-93cb-6e1edb2a5717
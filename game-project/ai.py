from __future__ import annotations

from typing import Dict, List, Tuple

_PRIORITY = {4: 4, 2: 3, 3: 2, 1: 1}

# (c1, c2, c3, c4, p1, p2, player)
State = Tuple[int, int, int, int, int, int, int]


def _evaluate(p1: int, p2: int) -> int:
    return p2 - p1


def _moves(c1: int, c2: int, c3: int, c4: int) -> List[int]:
    moves: List[int] = []
    if c1 > 0:
        moves.append(1)
    if c2 > 0:
        moves.append(2)
    if c3 > 0:
        moves.append(3)
    if c4 > 0:
        moves.append(4)
    moves.sort(key=lambda x: _PRIORITY[x], reverse=True)
    return moves


def _apply_pick(
    c1: int,
    c2: int,
    c3: int,
    c4: int,
    p1: int,
    p2: int,
    player: int,
    pick: int,
) -> State:
    if pick == 1:
        c1 -= 1
        if player == 1:
            p2 += 1
        else:
            p1 += 1
    elif pick == 2:
        c2 -= 1
        if player == 1:
            p1 -= 4
        else:
            p2 -= 4
    elif pick == 3:
        c3 -= 1
        if player == 1:
            p2 += 3
        else:
            p1 += 3
    elif pick == 4:
        c4 -= 1
        if player == 1:
            p1 -= 8
        else:
            p2 -= 8
    else:
        raise ValueError("pick must be 1..4")

    next_player = 2 if player == 1 else 1
    return (c1, c2, c3, c4, p1, p2, next_player)


def alphabeta(
    state: State,
    depth: int,
    alpha: int,
    beta: int,
    memo: Dict[Tuple[State, int], int],
) -> int:
    key = (state, depth)
    if key in memo:
        return memo[key]

    c1, c2, c3, c4, p1, p2, player = state

    if (c1 + c2 + c3 + c4) == 0 or depth == 0:
        val = _evaluate(p1, p2)
        memo[key] = val
        return val

    possible = _moves(c1, c2, c3, c4)

    if player == 1:
        value = -10**9
        for move in possible:
            nxt = _apply_pick(c1, c2, c3, c4, p1, p2, player, move)
            value = max(value, alphabeta(nxt, depth - 1, alpha, beta, memo))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
    else:
        value = 10**9
        for move in possible:
            nxt = _apply_pick(c1, c2, c3, c4, p1, p2, player, move)
            value = min(value, alphabeta(nxt, depth - 1, alpha, beta, memo))
            beta = min(beta, value)
            if alpha >= beta:
                break

    memo[key] = value
    return value


def choose_move(
    sequence: List[int],
    p1: int,
    p2: int,
    current_player: int,
    depth: int = 8,
) -> int:
    if not sequence:
        raise ValueError("sequence is empty")
    if current_player not in (1, 2):
        raise ValueError("current_player must be 1 or 2")

    c1 = sequence.count(1)
    c2 = sequence.count(2)
    c3 = sequence.count(3)
    c4 = sequence.count(4)

    memo: Dict[Tuple[State, int], int] = {}
    possible = _moves(c1, c2, c3, c4)
    best_move = possible[0]

    if current_player == 1:
        best_val = -10**9
        alpha, beta = -10**9, 10**9
        for move in possible:
            nxt = _apply_pick(c1, c2, c3, c4, p1, p2, current_player, move)
            val = alphabeta(nxt, depth - 1, alpha, beta, memo)
            if (val > best_val) or (
                val == best_val and _PRIORITY[move] > _PRIORITY[best_move]
            ):
                best_val = val
                best_move = move
            alpha = max(alpha, best_val)
    else:
        best_val = 10**9
        alpha, beta = -10**9, 10**9
        for move in possible:
            nxt = _apply_pick(c1, c2, c3, c4, p1, p2, current_player, move)
            val = alphabeta(nxt, depth - 1, alpha, beta, memo)
            if (val < best_val) or (
                val == best_val and _PRIORITY[move] > _PRIORITY[best_move]
            ):
                best_val = val
                best_move = move
            beta = min(beta, best_val)

    return best_move

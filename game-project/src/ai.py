from __future__ import annotations
from typing import List, Tuple

_PRIORITY = {4: 4, 2: 3, 3: 2, 1: 1}


def _apply_rules(p1: int, p2: int, current_player: int, number: int) -> Tuple[int, int]:
    if number % 2 == 0:
        if current_player == 1:
            p1 -= 2 * number
        else:
            p2 -= 2 * number
    else:
        if current_player == 1:
            p2 += number
        else:
            p1 += number
    return p1, p2


def choose_move(sequence: List[int], p1: int, p2: int, current_player: int) -> int:
    
    
    if not sequence:
        raise ValueError("sequence is empty")
    if current_player not in (1, 2):
        raise ValueError("current_player must be 1 or 2")

    best_eval = None
    best_candidates: List[int] = []

    for i, number in enumerate(sequence):
        new_p1, new_p2 = _apply_rules(p1, p2, current_player, number)

        if current_player == 1:
            my_score, opp_score = new_p1, new_p2
        else:
            my_score, opp_score = new_p2, new_p1

        eval_value = opp_score - my_score

        if best_eval is None or eval_value > best_eval:
            best_eval = eval_value
            best_candidates = [i]
        elif eval_value == best_eval:
            best_candidates.append(i)

    # если один кандидат — вернуть число
    if len(best_candidates) == 1:
        return sequence[best_candidates[0]]

    # tie-break by priority (4>2>3>1)
    best_index = best_candidates[0]
    best_pr = _PRIORITY.get(sequence[best_index], 0)

    for i in best_candidates[1:]:
        pr = _PRIORITY.get(sequence[i], 0)
        if pr > best_pr:
            best_pr = pr
            best_index = i

    return sequence[best_index]
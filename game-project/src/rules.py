# Spēlētāju sākotnējie punkti
p1, p2 = 100, 100

# Noteikumu funkcija
def apply_rules(p1, p2, current_player, number):
    if number == 1:
        if current_player == 1:
            p2 += 1
        else:
            p1 += 1
    elif number == 3:
        if current_player == 1:
            p2 += 3
        else:
            p1 += 3
    elif number == 2:
        if current_player == 1:
            p1 -= 4
        else:
            p2 -= 4
    elif number == 4:
        if current_player == 1:
            p1 -= 8
        else:
            p2 -= 8
    return p1, p2

print("Pēdējie rezultāti:")
print("Spēlētājs 1:", p1)
print("Spēlētājs 2:", p2)

# https://chatgpt.com/share/699f5f9e-d234-8010-83b5-d1d331d7c133

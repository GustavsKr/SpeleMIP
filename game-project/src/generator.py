import random

def generate_sequence(input_number: int):
    num_sequence = []
    if input_number < 15 or input_number > 25:
        print("error: numbers must be between 15 and 25")
    else:
        for n in range(input_number):
            random_int = random.randint(1, 4)
            num_sequence.append(random_int)

    return num_sequence 

test = generate_sequence(15)
print(test)

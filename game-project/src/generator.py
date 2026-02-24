import random

def generate_sequence(input_number: int):
    
    num_sequence = []

    #check for  data type 
    if not isinstance(input_number, int):
        print("error: input must be integer")
        return None

    if input_number < 15 or input_number > 25:
        print("error: numbers must be between 15 and 25")
        return None

    
    for n in range(input_number):
            random_int = random.randint(1, 4)
            num_sequence.append(random_int)

    return num_sequence 



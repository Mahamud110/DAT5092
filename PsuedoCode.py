import random
N_Min = 1
N_Max = 1
N_Rand = random.randint(N_Min,N_Max)

i = 1
y = 1


while (y = 1):
    guess = input("Guess a Number")
    if (guess > N_Rand):
        print("Too High")
        i+=1

    elif (guess<N_Rand):
        print("Too Low")
        i+=1
    else:
        print("Well done! Guessed in" +i "attempts")
        y = 0
    










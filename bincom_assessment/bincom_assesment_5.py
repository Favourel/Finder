
# QUESTION 5: if a colour is chosen at random, what is the probability that the color is red?

colors = ["GREEN", "YELLOW", "GREEN", "BROWN", "BLUE", "PINK", "BLUE", "YELLOW", "ORANGE", "CREAM", "ORANGE", "RED", "WHITE", "BLUE", "WHITE", "BLUE", "BLUE", "BLUE", "GREEN"]
num_red = colors.count("RED")
probability = num_red / len(colors)
print(probability)


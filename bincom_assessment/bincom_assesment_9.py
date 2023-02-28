# question 9: Write a program to sum the first 50 fibonacci sequence in python
# Function to calculate the nth Fibonacci number
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


# Sum the first 50 Fibonacci numbers
fib_sum = 0
for i in range(50):
    fib_sum += fibonacci(i)

print("Sum of the first 50 Fibonacci numbers:", fib_sum)

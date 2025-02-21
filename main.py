import random


def find_big_primes():
    start = int("1" + 151 * "0")
    stop = int("1" + 150 * "0")
    primes = []
    count = 0
    for number in range(start - 1, stop, -2):
        if miller_rabin_test(number):
            count += 1
            primes.append(number)
            if count == 50:
                break
    first = random.choice(primes)
    primes.remove(first)
    second = random.choice(primes)
    return first, second


def miller_rabin_test(number, k=100):
    # find indicator and odd_factor from n-1 = 2^s * odd_factor
    indicator = 0
    odd_factor = number - 1
    while odd_factor % 2 == 0:
        odd_factor //= 2
        indicator += 1

    # perform k iterations of the test
    viewed = []
    for _ in range(k):
        a = random.randint(2, number - 2)
        while a in viewed:
            a = random.randint(2, number - 2)
        x = pow(a, odd_factor, number)
        if x == 1 or x == number - 1:
            continue
        for _ in range(indicator - 1):
            x = pow(x, 2, number)
            if x == number - 1:
                break
        else:
            return False
    return True


def greatest_common_divisor(number_1, number_2):  # implemented with Euclidian algorithm
    gcd = 0
    while number_2 > 0:
        gcd = number_2
        remainder = number_1 - number_1 // number_2 * number_2
        number_1, number_2 = number_2, remainder
    return gcd


def find_private_exponent(number_1, number_2):  # implemented with extended Euclidian algorithm
    x1, x2 = 0, 1
    y1, y2 = 1, 0
    while number_2 > 0:
        coefficient = number_1 // number_2
        remainder = number_1 - coefficient * number_2
        x = x2 - coefficient * x1
        y = y2 - coefficient * y1
        number_1, number_2 = number_2, remainder
        x2, x1 = x1, x
        y2, y1 = y1, y
    return y2


first_prime, second_prime = find_big_primes()
n = first_prime * second_prime
euler_func = (first_prime - 1) * (second_prime - 1)

public_exp = 65537
while greatest_common_divisor(euler_func, public_exp) != 1:
    public_exp += 2

private_exp = find_private_exponent(euler_func, public_exp)
while private_exp < 0:
    private_exp += euler_func

print("Bob wanted to send to Alice a secret message (!tell her how he feels!)")
print(f"Alice sent to Bob a public key: ({public_exp}, {n})")
message = [ord(symbol) for symbol in input("Bob composed the message: ").strip()]
print("and encrypted it letter by letter with public key and then sent it to Alice")
encrypted_message = [pow(order, public_exp, n) for order in message]
print(f"Alice used her private key: ({private_exp}, {n})")
decrypted_message = [pow(cipher, private_exp, n) for cipher in encrypted_message]
print("and decrypted the Bob's message:", "".join([chr(order) for order in decrypted_message]))

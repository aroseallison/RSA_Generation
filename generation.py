import random
from random import randrange, getrandbits


def Miller_Rabins(a, n):
    if a == 0:
        return True
    s = n - 1
    t = 0 
    u = pow(a, s, n)
    if u - 1 == 0 or u + 1 == n:
        return True
    for i in range(t - 1):
        u = pow(u, 2, n)
        if u + 1 == n:
            return True
    return False


def generate_prime(n):
    assert n > 1
    while True:
        m = randrange(2 ** (n - 1) + 1, 2 ** (n), 2)
        find = True
        for i in range(2, n - 1):
            a = getrandbits(n) % m
            if not Miller_Rabins(a, m):
                find = False
                break
        if find:
            return m


def euclidean_alg(a, b):
    r = a % b
    q = int(a / b)
    while (r != 0):
        a = b
        b = r
        q = int(a / b)
        r = a - (b * q)
    return (b)


def extended_ea(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_ea(b % a, a)
        s = (y - (b // a) * x)
        return gcd, s, x


def powmod_sm(b, e, n):
    exp = bin(e)
    x = b
    for i in range(3, len(exp)):
        x = (x ** 2) % n
        if exp[i: i + 1] == '1':
            x = (x * b) % n
    return x


def RSA_Keygen(n):
    p = int(generate_prime(n))
    print('p is', p)
    q = int(generate_prime(n))
    print('q is ', q)
    n = p * q
    print('n is', n)
    phi_n = (p - 1) * (q - 1)
    print('phi of n is ', phi_n, "\n")
    while True:
        e = random.randrange(1, phi_n - 1)
        if euclidean_alg(e, phi_n) == 1:
            gcd, s, t, = extended_ea(phi_n, e)  # check this - i switched them
            if gcd == ((s * phi_n) + (t * e)):
                d = t % phi_n
                break
    return (n, e, d)


def encrypt(mes, e, n):
    cipher = ''
    for i in mes:
        m = ord(i)
        cipher += str(powmod_sm(m, e, n)) + " "
    return cipher


def decrypt(cipher, n, d):
    message = ''
    ciph_splilt = cipher.split()
    for i in ciph_splilt:
        if i:
            c = int(i)
            message += chr(powmod_sm(c, d, n))
    return message

def main():
    bits = 512
    keys = RSA_Keygen(bits)
    n = keys[0]
    print('n is: ', n)
    e = keys[1]
    print('e is: ', e)
    d = keys[2]
    print('d is: ', d)
    public_key = (n, e)
    private_key = d
    print('\npublic key: ', public_key)
    print('private key: ', private_key, "\n")

    message = "This is my message I'd like to send encrypted!"
    encMessage = encrypt(message, e, n)
    print('message is: ', message)
    print('encrypted message is: ', encMessage)
    decMessage = decrypt(encMessage, n, d)
    print('decrypted message: ', decMessage)
    print(extended_ea(304, 313))
main()

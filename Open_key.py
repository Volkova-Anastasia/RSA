import math
import random

import regex as re
import math
def des_numder(ch):
    number = 0
    len_dat = len(ch)
    for i in range(0, len_dat):
        number += int(ch[i]) * (2 ** (len_dat - i - 1))
    return number

def power(x, n, modul):
    step = n
    vnesh_ch = 1
    while step != 1:
        if step % 2 ==1:
            vnesh_ch = vnesh_ch * x
            vnesh_ch = vnesh_ch % modul
            step = step - 1
        x **=2
        x %= modul
        step //=2
    final_vers = vnesh_ch * x % modul
    return final_vers

def prime_number(number):
    counter = 0
    for i in range(2,number-1):
        if number % i == 0:
            counter += 1
    if counter >= 1:
        checker = 1
        return checker
    else:
        checker = 0
        return checker

def evklid(alpha, beta):
    if alpha > beta:
        a = alpha
        b = beta
    else:
        a = beta
        b = alpha

    y2 = 0
    y1 = 1
    r = 100
    while r != 0:
        q = a // b
        r = a % b
        y = y2 - q * y1
        a = b
        b = r
        y2 = y1
        y1 = y
    return y2

def generation_key(p, q):
    if p != q:
        ch1 = prime_number(p)
        ch2 = prime_number(q)
        if ch1 == 0 and ch2 == 0:
            n = p * q
            func_euler = (p - 1)*(q - 1)
            print('Введите экспоненту шифрования взамно-простое со значением - ', func_euler)
            e_z = int(input())
            d = evklid(e_z, func_euler)
            print('Открытый ключ RSA  - ', e_z, ' ', n)
            print('Private key RSA - ', d, ' ', n)
            return e_z, n, d
        else:
            print('Числа не являются простыми, измените значения p и q')

def encryption(e_z, n, place):
    with open(place, 'rb') as file:
        message = file.read()
    print('Message - ', message)
    text = ''
    message = bytes.hex(message)
    message = int(message, 16)
    message = bin(message)[2:]
    len_block = math.floor(math.log2(n))
    zero = len(message) % len_block
    text = message
    text = '0' * (len_block - zero) + text
    bi_blocks = []
    for i in range(len(text) // len_block):
        bi_blocks.append(text[i * len_block:len_block + i * len_block])
    #print(bi_blocks)
    len_block_2 = len_block + 1
    bi_blocks_ascii = []
    text_new = ''
    for i in bi_blocks:
        i = des_numder(i)
        i = i ** e_z
        i = i % n
        i = bin(i)
        i = str(i)
        i = i.replace('b', '')
        if len(i) < len_block_2:
            zero = len(i) % len_block_2
            i = '0' * (len_block_2 - zero) + i
        text_new += i
    print('Text new - ', text_new)
    text_new = int(text_new, 2)
    if len(hex(text_new)) % 2 != 0:
        text_new = '0' + hex(text_new)[2:]
    else:
        text_new = hex(text_new)[2:]
    bitici_text = bytes.fromhex(text_new)
    print('Bitici  - ',bitici_text)
    print('Куда сохранить шифртекст?')
    name_for_ciphertext = input()
    with open(name_for_ciphertext, 'wb') as file:
        file.write(bitici_text)
    print('---Проверьте файл в директории!---')


def decryption(d, n, place):
    with open(place, 'rb') as file:
        message = file.read()
    # print(message)
    text = ''
    text = bytes.hex(message)
    text_new = int(text, 16)
    text_new = bin(text_new).replace('0b','')
    blocks = []
    len_block = math.floor(math.log2(n))+1
    zero = len(text_new) % len_block
    text_new = '0' * (len_block - zero) + text_new
    text_sec = ''
    for i in range(len(text_new)//len_block):
        blocks.append(text_new[i*len_block:len_block+i*len_block])
        blocks[i] = power(int(blocks[i], 2), d, n)
        print('Hello - hui')
        # blocks[i] = (int(blocks[i], 2)**d) % n
        blocks[i] = bin(blocks[i]).replace('0b', '')
        len_block_z = math.floor(math.log2(n))
        zero = len(blocks[i]) % len_block_z
        if zero != 0:
            blocks[i] = '0' * (len_block_z - zero) + blocks[i]
        text_sec += str(blocks[i])
    print('Blocks -- ', blocks)
    print('Len - ', len(blocks))
    print('2   ', text_sec)
    text_sec = hex(int(text_sec, 2))[2:]
    print(text_sec)
    if len(text_sec) % 2 != 0:
        text_sec = '0' + text_sec
    text_sec = bytes.fromhex(text_sec)
    print('1  ', text_sec)
    print('Куда сохранить открытый текст?')
    name_for_opentext = input()
    with open(name_for_opentext, 'wb') as file:
        file.write(text_sec)
    print('---Проверьте файл в директории!---')

def random_key(dlin):
    key_len = random.getrandbits(dlin)
    key_len |= (1 << dlin - 1) | 1
    return key_len

def generation_key_random():
    p,q,e = generation_random_pub()
    func_evclid = (p-1)*(q-1)
    n = p*q
    d = generation_random_priv(n, func_evclid, e)
    print('Получившийся открытый ключ (e, n) - ', e, n)
    print('Получившийся закрытый ключ (d, n) - ', d, n)

    test_correctness = power(power(111111, e, n), d, n)
    if test_correctness != 111111:
        print('Ключ неверный, операция выполняется повторно.')
        generation_key_random()
    return 0
def generation_random_pub():
    p,q  = prime()
    e = 47
    func_evclid = (p-1)*(q-1)
    while not math.gcd(func_evclid, e) == 1:
        p,q = prime()
        e = 47
        func_evclid = (p-1)*(q-1)
    return p,q,e

def generation_random_priv(n, func_evclid, e):
    evc = evklid(func_evclid, e)
    d = evc + n * (evc<0)
    return d

def prime():
    p,q = generation_prime(), generation_prime()
    return p,q

def prime_or_not(n, k=128):
    for i in range(k):
        test_var = random.randint(2, n - 1)
        result = power(test_var, n-1, n)
        if result != 1:
            return False
    return True

def generation_prime(len = 1024):
    just_ch = 6
    while not prime_or_not(just_ch, 128):
        just_ch = random_key(len)
    return just_ch






place = 'C:/Users/nedod/PycharmProjects/Криптография 2 курс/RSA/'
print('Выберите нужное: ')
print('1. Самостоятельно ввести ключи')
print('2. Сгенерировать по длине ключа')
choice = int(input())
if choice == 1:
    print('Введите значения p и q')
    p = int(input())
    q = int(input())
    generation_key(p, q)
if choice == 2:
    print('Введите длину значений p и q в битах: ')
    generation_key_random()


print('Введите путь (название) файла: txt')
place_2 = input()
place = place + place_2
print(place)

print('Выберите необходимое действие: ')
print('1. Зашифрование')
print('2. Расшифрование')
do = int(input())
if do == 1:
    print('Введите открытый ключ - ')
    e = int(input())
    nn = int(input())
    encryption(e, nn, place)
if do == 2:
    print('Введите закрытый ключ - ')
    d = int(input())
    nn = int(input())
    decryption(d, nn, place)


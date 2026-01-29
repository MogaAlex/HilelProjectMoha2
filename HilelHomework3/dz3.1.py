
# Zadanie 1.1

def string11(a: str):
    return len(a)

# Zadanie 1.2

def string12(a: str, b: str):
    return a+b

# Zadanie 2.1

def integer11(a: int or float):
    return a**2

# Zadanie 2.2

def integer12(a: int or float, b: int or float):
    return a+b

# Zadanie 2.3

def integer13 (a: int, b: int):
    return a%b, a//b

# Zadanie 3.1

def list11(a: list):
    c = []
    sum = 0
    for b in a:
        if type(b) == int or type(b) == float:
            c.append(b)
    for d in c:
        sum = sum+d
        midsum = sum/len(c)
    return midsum

# Zadanie 3.2

def list12(a: list, b: list):
    general = []
    for c in a:
        if c in b:
            general.append(c)
    return general

# Zadanie 4.1

def Dictionaries11(a: dict):
    return a.keys()

# Zadanie 4.2

def Dictionaries12(a: dict, b: dict):
    for c in b:
        a.update({c:b[c]})
    return a

# Zadanie 5.1

def Seti1(a: set, b: set):
    return a.union(b)


# Zadanie 5.2

def Seti2(a: set, b: set):

    if len(a) > len(b):
        if len(b) == len(a.intersection(b)) and len(a.intersection(b)) !=0:
            return print("Повна підмножина")
        elif len(b) > len(a.intersection(b)) and len(a.intersection(b)) !=0 :
            return print("Часткова підмножина")
        else:
            return print("Не множина або пуста множина")

    if len(b) > len(a):
        if len(a) == len(a.intersection(b)) and len(a.intersection(b)) !=0:
            return print("Повна підмножина")
        elif len(a) > len(a.intersection(b)) and len(a.intersection(b)) !=0 :
            return print("Часткова підмножина")
        else:
            return print("Не множина або пуста множина")

    if len(a) == len(b):
        if len(b) == len(a.intersection(b)) and len(a.intersection(b)) !=0:
            return print("Повна підмножина")
        elif len(b) > len(a.intersection(b)) and len(a.intersection(b)) !=0 :
            return print("Часткова підмножина")
        else:
            return print("Не множина або пуста множина")

# Zadanie 6.1

def Cicle1(a: int):
    if a%2 == 0:
        print("Парне")
    else:
        print("Не парне")

# Zadanie 6.2

def Cicle2(a: list):
    c= []
    for b in a:
        if b%2 == 0:
            c.append(b)
    return c

# Zadanie 7.1

double = lambda a: "Парне" if a % 2 == 0 else "Не парне"

#Proverki zadaniy

# 1.1
print("Задание 1.1")
string11 = string11('Hello Git!')
print(string11)
print()

# 1.2
print("Задание 1.2")
string12 = string12('Hello Git!', 'Hello Git!')
print(string12)
print()

# 2.1
print("Задание 2.1")
integ11 = integer11(-1)
print(integ11)
print()

# 2.2
print("Задание 2.2")
integ12 = integer12(7, 8)
print(integ12)
print()

# 2.3
print("Задание 2.3")
integer13 = integer13(4,2)
print(integer13)
print()

# 3.1
print("Задание 3.1")
lst11 = list11([1,2, "ddsa", 5, 2.3, 11, "321" ])
print(lst11)
print()

# 3.2
print("Задание 3.2")
lst12 = list12 ([1,8,"a",6,5,5], [2,4,"a",4,5,5])
print(lst12)
print()

# 4.1
print("Задание 4.1")
dict1= Dictionaries11({'a':1, 'b':2, 'c':3})
print(dict1)
print()

# 4.2
print("Задание 4.2")
dict2 = Dictionaries12({'a':1, 'b': 3 }, {'e':2, 'f': 4})
print(dict2)
print()

# 5.1
print("Задание 5.1")
PharaonSeti1 = Seti1({1,2,3}, {4,5,6})
print(PharaonSeti1)
print()

# 5.2
print("Задание 5.2")
PharaonSeti2 = Seti2({1,2,4},{6,5,3})
print()

# 6.1
print("Задание 6.1")
Cicli1= Cicle1(5)
print()

# 6.2
print("Задание 6.2")
Cicli2 = Cicle2([1,2,3,4,5,6,4])
print(Cicli2)
print()

# 7.1
print("Задание 7.1")
print (double(5))
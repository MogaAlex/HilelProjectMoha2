from itertools import product


class Product:
    def __init__(self, name, autor, price):
        self.name = name
        self.autor = autor
        self.price = price



    def __str__(self):
        return f"{self.name}, {self.autor}, {self.price}"

class Summary:
    def __init__(self):
        self.items = []

    def add_item(self, product):
        self.items.append(product.name)


    def __str__(self):
        return("\n".join(self.items))





product1 = Product("100 years of solitude", "Gabriel Marquez", 20)
product2 = Product("Absalom, Absalom", "William Folkner", 20)
product3 = Product("Notre-Dame de Paris", "Victor Hugo", 30)

# Summary = Summary()
# Summary.add_item(product1)
# Summary.add_item(product2)
# Summary.add_item(product3)
#
# print(Summary)

Summname = [product1.name, product2.name, product3.name]
Summautor = [product1.autor, product2.autor, product3.autor]
Sumprice = [product1.price, product2.price, product3.price]
#print(product1)



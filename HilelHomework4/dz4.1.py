
class Product:
    def __init__(self, name, category, price, quantity):
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity

    def changeprice(self,newprice):
        self.price = newprice

    def changequantity(self, newquantity):
        self.quantity = newquantity

    def __str__(self):
        return f'{self.name} {self.category} {self.price} {self.quantity}'

class Customer:
    def __init__(self, name, mail):
        self.name = name
        self.mail = mail
        self.listorders = {}


    def  add_order(self, product, quantity):
        self.listorders[product] = quantity

    def __str__(self):
        result = ''
        for product, quantity in self.listorders.items():
            result += f'{product.name}, {quantity}\n'
        return f'{self.name} {self.mail}:\n{result}'


class Order:
    def __init__(self, ):
        self.products = {}
        self.total = 0

    def add_item(self, item, quantity):

        if item in self.products:
            self.products[item] += quantity
        else:
            self.products[item] = quantity
        self.total += item.price * quantity

    def __str__(self):
        result = ''
        for product, quantity in self.products.items():
            result += f'{product.name}, {product.price}, {quantity} \n'
        result += f'Totalsum: {self.total}'
        return result

class Shop:
    def __init__(self):
        self.products = []
        self.customers = []

    def load_from_file(self, filename):
        section = None

        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                if line == "[PRODUCTS]":
                    section = "products"
                    continue

                elif line == "[CUSTOMERS]":
                    section = "customers"
                    continue

                if section == "products":
                    name, category, price, quantity = line.split(",")
                    self.products.append(Product(name, category, int(price), quantity))


                elif section == "customers":
                    name, mail = line.split(",")
                    self.customers.append(Customer(name, mail))

    def show_products(self):
        for products in self.products:
            print(products)

    def show_customers(self):
        for cust in self.customers:
            print(cust)

#Проверка тестов
store = Shop()
store.load_from_file("shop.txt")
print("Товары:")
store.show_products()
print("\nКлиенты:")
store.show_customers()

order = Order()
order.add_item(store.products[0], 3)
order.add_item(store.products[1], 4)

print("\nЗаказ:")
print(order)
print()
Product1 = Product( "banan", "fruit", 10, 50)
Product2 = Product( "apple", "fruit", 20, 10)
Product3 = Product( "potato", "vegetable", 20, 5)

Product1.changeprice(20)
Product1.changequantity(10)

cust1 = Customer("John", "Lala@lasasa.com")

cust1.add_order(Product1,2)
cust1.add_order(Product2,1)
print(cust1)

order1 = Order()
order1.add_item(Product1, 2)
order1.add_item(Product2, 1)
order1.add_item(Product3, 3)
print(order1)


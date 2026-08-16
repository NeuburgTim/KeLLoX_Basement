from src.kellox_basement.test import Bsp
j = 0
running = 1
while running == 1:
    if True:
        print("Tab")

    for i in range(6):
        print("googoogaga" + str(i))

    while j <= 3:
        print("lol")
        j = j + 1

    a = int(input("Gib mir eine Zahl "))

    match a:
        case 0:
            print("omg ich liebe dich")
        case _:
            print("töte dich")

    class Bob:
        def __init__(self):
            self.name = "Bob"

        def namenPrint(self):
            print(self.name)

        def __call__(self, *args, **kwds):
            print("Ich wurde gecallt oder so was weiß ich")

    Person = Bob()
    Person.namenPrint()
    Person(2,4,56,7,p = 3)


    dictionaryBsp = {"Key":5}
    print(dictionaryBsp.get("Key",2))
    print(dictionaryBsp.get("Bro",2))
    print(dictionaryBsp["Key"])
    

    x = int(input("Gebe mir einen Wert a für Modulo"))
    y = int(input("Gebe mir einen Wert b für Modulo"))

    def mod(a:int, b:int ) -> int:
        c = a % b
        return c

    print(f"So sieht der Modulos aus {mod(x,y)}!")

    print(r"/////()§)(§=§!)")

    Bsp()



    running = int(input("Willst du nochmal? (1 für j)"))
from src.kellox_basement.test import Bsp #importierbefehl für einzelne Funktionen
j = 0 #variablen deklarieren. Deckt alle typen ab
running = 1
while running == 1: #while schleife zum prüfen ob Programm noch läuft. Doppelpunkt für Funktionsstart. Alles eingerückte teil des Statements
    if True: 
        print("Tab") #print funktion printet

    for i in range(6): #komische range funktion. Lauft von i = 0 bis i = 5. I wird inkrementiert
        print("googoogaga" + str(i)) #Typecast von int i zu einem String

    while j <= 3: 
        print("lol")
        j = j + 1 #manuelle erhöhung bei jedem Durchlauf

    a = int(input("Gib mir eine Zahl ")) #einlesen von Eingabe des Users

    match a: #switch case statement
        case 0: #wenn a = 0, dann ...
            print("omg ich liebe dich")
        case _: #default case. Also wenn a != eins von den anderen cases
            print("töte dich")

    class Bob: #dekleration von klasse. Alles in einrückung teil von Klasee
        def __init__(self): #Konstruktor
            self.name = "Bob" #self verweißt auf das Objekt der Klasse Bob

        def namenPrint(self): #funktion der Klasse
            print(self.name) #aufruf von Attribut des Objektes

        def __call__(self, *args, **kwds): #args und kwds fangen alle unerwünschten eingaben ab
            print("Ich wurde gecallt oder so was weiß ich")

    Person = Bob() #Objekt von Klasse Bob erstellt
    Person.namenPrint() #Funktion der Klasse aufrufen
    Person(2,4,56,7,p = 3) #lowkey keine ahnung was das ist


    dictionaryBsp = {"Key":5} #key value pair. Alles in python ist eine dictionary
    print(dictionaryBsp.get("Key",2)) #printet das gepaarte Element mit unserem Key
    print(dictionaryBsp.get("Bro",2)) #printet 2 wenn nicht findbar. Hier also 2, weil "Bro" nicht existiert
    print(dictionaryBsp["Key"]) #auch ohne get möglich.
    

    x = int(input("Gebe mir einen Wert a für Modulo"))
    y = int(input("Gebe mir einen Wert b für Modulo"))

    def mod(a:int, b:int ) -> int: #variablen die übergeben werden, sollten festgelegten typ haben. Hier int. -> int sagt welchen typ die Rückgabe hat
        c = a % b #modulo rechnung
        return c #ausgabewert
        #alternativ auch return a % c möglich

    print(f"So sieht der Modulos aus {mod(x,y)}!") #f string ermöglicht kombinationen von Typen in einen String. Mittels {}

    print(r"/////()§)(§=§!)") #r string printet raw

    Bsp() #importierte Funktion



    running = int(input("Willst du nochmal? (1 für j)")) #einfgabe für while schleife
Projekt:
Roguelike, Turnbased, Daily Run -> Seed System



Skills/Passives:
Skills spezialisiert auf Klasse
4 Aktive Skills möglich und 2 Passive(Potentiell mehr mal gucken)
Würde man ansprechen mit Aktiv Skill 1 zu Aktiv Skill 4 von Links nach Rechts
Manche Skills Statt Mana Cooldown
1 Waffen Skill extra z.B. schlagen mit der Waffe oder so (sollte nicht zu oft nutzbar sein z.B. durch Cooldown oder limit insgesamt)
1 mal bewegen
1 Standardangriff, welche gleich ist bei charakteren der selben Klasse


Effekte/Feld Effekte:
Feld Effekte durch z.b. Wasser -> gibt man an in dem Array, siehe unten bei Combat
Durch Waffen/Items/Skills natürlich auch möglich
Sollten cooldown haben


Combat Insgesamt:
10x10
Objekte und Gegner verteilt (weg von Spieler Spawn)
Feld Erstellen mit Array? Das man dann in anderen Dateien machen kann, also da wären alle Feld Arrays in einer anderen Datei
Reihenfolge zufall (vlt nach Speed?), aber am besten jeder nur 1 mal pro Turn außer Elite und Boss



Level Up Mechanic:
Squad von 4 Menschen (zwischen 1 und 4)
Skill Auswahl nach Level-Up
XP Pro Level immer gleich für Level Up
Pro Kampf 2 Level an Xp auf Gegner logisch Verteilt

Stats pro Charakter:
X = Auswahl bei Level Up
X Schaden 5         1 Stat = 1 Schaden
X Leben  5 Stats    1 Stat = 4 Leben
Rüstung  0          1 Stat = 1 Leben als Extra Rüstung
X Speed  3          1 Stat = 1 Tile Reichweite beim gehen
X Mana   3          1 Stat = 1 Mana Regeneration Pro Turn
X Max Mana 4        1 Stat = 4 Max Mana
X Luck   5          1 Stat = 1% verbesserte Chance auf was gutes oder so

Auswahl zwischen 3
Level 1 Klassenwahl -> Passive und 2 Skills durch Zufall am Anfang
Level 2 Stat
Level 3 Skill
Level 4 Stat
Level 5 Spezialisierung -> Passive und 1 Skill rerollen
Level 6 Stat
Level 7 Skill
Level 8 usw -> potentiell skills upgraden sonst immer nur 1 stat up



Ausrüstung/Items:
Waffe
Rüstung
Artefakt
Bei Shop, 
Events, 
drop chance von Gegner nach Kampf,
drop chance bei Zerstören von Umgebung



Karte zum Durchgehen:
Gegner
Elite Gegner Weg wie in Slay the Spire
Events
Shop
Am Ende Boss

Nach Kampf:
Bekommt Xp
Tote bleiben Tod -> vlt Event zum wiederbeleben
Auf 25% Leben wenn drunter



Nach Runs:
Item unlocks und Skill unlocks für die Klassen mit denen Run geschafft wurde
kann run nicht speichern sondern neu machen wenn man aufhört



Seeds:
Seed als Input ist eine Zahl:
1. 3 Map Seeds 
Aus den Map Seeds:
Wo welche Gegner/Events etc Platziert werden und dann was dadrinnen vorkommt


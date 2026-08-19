combat:
Zuständing für das Combat


effects:
zuständig für effekte wie sie mit charakteren interagieren also z.b. feuer macht feuerschaden


entities:
zuständig dafür was eine Entität ist etc und was ein player ist


game_logic:
beschreibt geradigen spiel stand -> inventar, geld, hat player party und map als parameter und bestimmt darüber


game_transitions:
wird benutzt um zum Beispiel von Map zu Combat zu wechseln oder vom Tod des Letzten zu Game Over screen etc.


graphics:
nutzt man wenn man etwas zeichnen möchte mit dem imagehandler und ist insgesamt für darstellung da


items:
definiert was ein item ist und hat implementierungen


map:
macht die standardmäßige karte wo man einen weg wählt und so


save_logic:
wird genutzt um alles wichtige zu speichern(keine runs, nur unlocks)


settings:
wird genutzt um einstellungen zum sound etc zu machen


skills:
definiert was ein skill ist, wichtiger unterschied bei player und entity skills natürlich


sound:
wird genutzt um sounds und musik abzuspielen
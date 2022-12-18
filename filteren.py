# Functie om string te scheiden in 2 delen
import collections

def contains(substring, string):
    c1 = collections.Counter(string)
    c2 = collections.Counter(substring)
    return not(c2-c1)

def scheid_str(str):
    for i, char in enumerate(str):
        # Scheid tussen de dubbele punt
        if char == ":":

            helft_1 = str[i + 1:]
            helft_2 = str[:i]

            return([helft_1, helft_2])
    # Als geen dubbele punt return de str en een "Decoy" zodat hij niet faalt als er geen tuple is
    if str != "":
        return(str, "@$^*(ASDjkas h@UEHIG@EhbmsAe2")
    else:
        return("@#*(&$RS", "@#$Y$SJKH")

# Functie om specifieke producten te verwijderen met een specifieke tekst
def check_specifiek(str, str_2):
    for woord in str:
        for i, char in enumerate(woord):
            if char == "!":
                if woord[i + 1:] in str_2:
                    return True
                else:
                    return woord[:i]

def check_of_in_woord(l, str_vergelijk):
    for word in l:
        if word in str_vergelijk:
            print(word+ " TRUE")
            continue

        else:
            print(word + " FALSE")
            return False

    return True


# Lijst om resultaten te bewaren
def filter(gewenste_file, gescrapede_file, results_file):
    results = []
    # Open file met gewenste videokaarten en de gescrapete videokaarten
    with open(gewenste_file, "r") as gewenste_f:

        # Filter de gewenste modellen
        for row in gewenste_f:

            # Maak alles kleine letters en verwijder extra lege lijnen
            row = row.replace("\n", "").lower()

            # Scheid de videokaart namen
            row = scheid_str(row)


            # Maak lijst voor matches
            matches = []

            # Open de file met gescrapete videokaarten
            with open(gescrapede_file, "r") as scraped_f:
                # Loep over de gescrapete videokaarten
                for i, line in enumerate(scraped_f.readlines()):
                    # Scheid de naam en prijs
                    naam = scheid_str(line)[1].lower()

                    if "|" in row[0]:

                        gesplit = row[0].split("|")
                        if check_of_in_woord(gesplit, naam):
                            # Voeg hem toe samen met prijs en index aan de lijst met matches
                            prijs = int(scheid_str(line)[0].strip("\n"))
                            matches.append((prijs, i))

                    check = check_specifiek(row, naam)

                    if isinstance(check, str):
                        row = list(row)
                        row[1] = check

                    if check is not True:
                        # Als de videokaart naam in de gescrapete string zit
                        if row[0] in naam or row[1] in naam:

                            # Voeg hem toe samen met prijs en index aan de lijst met matches
                            prijs = int(scheid_str(line)[0].strip("\n"))
                            matches.append((prijs, i))

            # Sorteer matches op prijs
            matches.sort()

            # Als er matches zijn
            if len(matches) != 0:
                # Voeg goedkoopste match toe aan lijst met results
                results.append(matches[0])

    # Verwijder dubbele results
    results = list(dict.fromkeys(results))

    # Open file opnieuw en lees hem zodat we er overheen kunnen loepen
    lines = open(gescrapede_file, "r").readlines()

    # Voeg results toe aan file met results
    with open(results_file, "w") as f:
        for result in results:
            f.write(lines[result[1]])

# Call filter functie op zowel videokaarten als processoren
filter("cpus.txt", "scraped_cpus.txt", "results_cpus.txt")
filter("gpus.txt", "scraped_gpus.txt", "results_gpus.txt")
filter("moederborden.txt", "scraped_moederborden.txt", "results_moederborden.txt")
filter("opslag.txt", "scraped_opslag.txt", "results_opslag.txt")

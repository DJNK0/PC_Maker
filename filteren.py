# Functie om string te scheiden in 2 delen
import collections
import pandas as pd

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

            continue

        else:

            return False

    return True


# Lijst om resultaten te bewaren
def filter(gewenste_file, gescrapede_file, results_file):
    results = []
    # Open file met gewenste videokaarten en de gescrapete videokaarten
    df_gewenst = pd.read_csv(gewenste_file)
    dinges = False
    with open(gewenste_file, "r") as gewenste_f:

        # Filter de gewenste modellen
        for row in gewenste_f:

            # Maak alles kleine letters en verwijder extra lege lijnen
            row = row.replace("\n", "").lower()

            # Scheid de videokaart namen
            row = scheid_str(row)

            # Maak lijst voor matches
            matches = []

            df_scraped = pd.read_csv(gescrapede_file, index_col=False, encoding="utf8")
            print(df_scraped.columns)
            # Loep over de gescrapete videokaarten
            for i in df_scraped.index:

                # Scheid de naam en prijs

                naam = df_scraped["productnaam"][i].lower()


                if "|" in row[0]:

                    gesplit = row[0].split("|")
                    if check_of_in_woord(gesplit, naam):
                        # Voeg hem toe samen met prijs en index aan de lijst met matches
                        prijs = df_scraped["prijs"][i]

                        matches.append((prijs, i))



                check = check_specifiek(row, naam)

                if isinstance(check, str):
                    row = list(row)
                    row[1] = check

                if check is not True:
                    # Als de videokaart naam in de gescrapete string zit
                    if row[0] in naam or row[1] in naam:
                        prijs = df_scraped["prijs"][i]
                        # Voeg hem toe samen met prijs en index aan de lijst met matches
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
    lines = open(gescrapede_file, "r", encoding="utf8").readlines()

    # Voeg results toe aan file met results
    with open(results_file, "w", encoding="utf8") as f:
        for result in results:
            f.write(lines[result[1]])

# Call filter functie op zowel videokaarten als processoren
filter("cpus.txt", "scraped_cpus.csv", "results_cpus.txt")
filter("gpus.txt", "scraped_gpus.csv", "results_gpus.txt")
filter("moederborden.txt", "scraped_moederborden.csv", "results_moederborden.txt")
filter("opslag.txt", "scraped_opslag.csv", "results_opslag.txt")

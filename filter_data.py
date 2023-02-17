# Functie om string te scheiden in 2 delen
import collections
import re

# Verwijder de haakjes van een string en return de string en data tussen haakjes lol
def verwijder_haakjes(s):
    data = re.search("<(.*)>", s)
    if data != None:
        data = data.group(1)
        data = data.split(",")
    s = re.sub('<.*?>', '', s)

    return s, data


# Scheid een string, links van een teken en rechts van een teken
def scheid_str(s, teken):
    for i, char in enumerate(s):
        # Scheid tussen de dubbele punt
        if char == teken:

            helft_1 = s[i + 1:]
            helft_2 = s[:i]

            return [helft_1, helft_2]
    # Als geen dubbele punt return de str en een "Decoy" zodat hij niet faalt als er geen tuple is
    if s != "":
        return s, "@$^*(ASDjkas h@UEHIG@EhbmsAe2"
    else:
        return "@#*(&$RS", "@#$Y$SJKH"

# Functie om specifieke producten te verwijderen met een specifieke tekst
def check_specifiek(s, str_2):
    for woord in s:
        for i, char in enumerate(woord):
            if char == "!":
                if woord[i + 1:] in s:
                    return True
                else:
                    return woord[:i]


# Kijk of een woord in een lijst in een string zit
def check_of_in_woord(l, s):
    for word in l:
        if word in s:
            continue
        else:
            return False
    return True


# Functie om gescrapete producten te filteren z
def filter_producten(gewenste_file, gescrapede_file, results_file):
    results = []
    # Open file met gewenste videokaarten en de gescrapete videokaarten
    with open(gewenste_file, "r") as gewenste_f:

        # Filter de gewenste modellen
        for row in gewenste_f:

            # Maak alles kleine letters en verwijder extra lege lijnen
            row = row.replace("\n", "").lower()
            row, data = verwijder_haakjes(row)

            # Scheid de socket van de rest als er cpu's gefilterd worden
            socket = ""
            snelheid = ""
            if gewenste_file == "data/gewenst_data/cpus.txt":
                socket, row = scheid_str(row, ";")

            # Scheid de snelheid en grootte van de ram als er ram gefilterd wordt
            elif gewenste_file == "data/gewenst_data/ram_ddr4.txt" or gewenste_file == "data/gewenst_data/ram_ddr5.txt":
                snelheid = re.search('\|(.*)\|', row).group(1)
                grootte = re.search('~(.*)~', row).group(1)
                row = row.replace("~", "")

            # Scheid de productnamen van de prijs
            row = scheid_str(row, ":")

            # Maak lijst voor matches
            matches = []

            # Open de file met gescrapete producten
            with open(gescrapede_file, "r+") as scraped_f:
                content = scraped_f.readlines()
                # Loep over de gescrapete producten
                for i, line in enumerate(content):

                    # Bewaar de oude naam voor later
                    naam_oud = line.lower()
                    naam_oud= naam_oud.strip("\n")

                    # Voeg de grootte en snelheid toe als het over ram gaat
                    if snelheid != "":
                        naam_oud += f"~{grootte}~"
                        naam_oud += f";{snelheid}\n"

                    """ 
                    Als het om videokaarten of processoren gaat,
                    voeg de data toe aan de originele naam. Deze is nodig
                    bij het samenstellen van de computer later
                    """
                    if data is not None:
                        naam_oud += "<" + ', '.join(data) + ">"

                        # Voeg de socket toe als het om processoren gaat
                        if socket != "":
                            naam_oud += f";{socket}"
                        naam_oud = "".join(line.strip() for line in naam_oud.splitlines()) + "\n"
                    else:
                        if gewenste_file == "data/gewenst_data/psus.txt":
                            naam_oud += "\n"
                    # Voeg het type opslag toe aan de oude naam als het om opslag gaat
                    if gewenste_file == "data/gewenst_data/opslag.txt":
                        opslag_type = row[0].replace("|", " ")
                        naam_oud += f";{opslag_type}\n"

                    # Scheid de naam en prijs
                    naam = scheid_str(line, ":")[1].lower()

                    """
                    Als er 2 productnamen erg op elkaar lijken,
                    check dan voor beide namen of ze in de gescrapete naam zitten.
                    """
                    if "|" in row[0]:
                        gesplit = row[0].split("|")
                        if check_of_in_woord(gesplit, naam):
                            # Voeg hem toe samen met prijs en index aan de lijst met matches
                            prijs = int(scheid_str(line, ":")[0].strip("\n"))
                            if gewenste_file == "data/gewenst_data/psus.txt":
                                naam_oud = naam_oud.strip("\n")
                                naam_oud += f";{gesplit[0]}\n"
                            matches.append((prijs,naam_oud, i))

                    check = check_specifiek(row, naam)

                    if isinstance(check, str):
                        row = list(row)
                        row[1] = check

                    if check is not True:
                        # Als de videokaart naam in de gescrapete string zit
                        if row[0] in naam or row[1] in naam:

                            # Voeg hem toe samen met prijs en index aan de lijst met matches
                            if gewenste_file == "data/gewenst_data/moederborden.txt":
                                naam_oud += f";{row[0]}\n"
                                print(naam_oud)

                            prijs = int(scheid_str(line, ":")[0].strip("\n"))
                            matches.append((prijs, naam_oud, i))

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
            f.write(result[1])


# Call filter functie op zowel videokaarten als processoren
filter_producten("data/gewenst_data/cpus.txt", "data/scraped_data/scraped_cpus.txt",
                 "data/results_data/results_cpus.txt")
filter_producten("data/gewenst_data/gpus.txt", "data/scraped_data/scraped_gpus.txt",
                 "data/results_data/results_gpus.txt")
filter_producten("data/gewenst_data/moederborden.txt", "data/scraped_data/scraped_moederborden.txt",
                 "data/results_data/results_moederborden.txt")
filter_producten("data/gewenst_data/opslag.txt", "data/scraped_data/scraped_opslag.txt",
                 "data/results_data/results_opslag.txt")
filter_producten("data/gewenst_data/ram_ddr4.txt", "data/scraped_data/scraped_ram_ddr4.txt",
                 "data/results_data/results_ram_ddr4.txt")
filter_producten("data/gewenst_data/ram_ddr5.txt", "data/scraped_data/scraped_ram_ddr5.txt",
                 "data/results_data/results_ram_ddr5.txt")
filter_producten("data/gewenst_data/psus.txt", "data/scraped_data/scraped_psus.txt",
                 "data/results_data/results_psus.txt")

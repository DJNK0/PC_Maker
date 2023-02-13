# Functie om string te scheiden in 2 delen
import collections
import re

def verwijder_haakjes(str):
    data = re.search("<(.*)>", str)
    if data != None:
        data = data.group(1)
        data = data.split(",")

    str = re.sub('<.*?>', '', str)

    return(str, data)

def scheid_str(str, teken):
    for i, char in enumerate(str):
        # Scheid tussen de dubbele punt
        if char == teken:

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

def get_psu_voeding_type():
    pass


# Lijst om resultaten te bewaren
def filter(gewenste_file, gescrapede_file, results_file):
    results = []
    # Open file met gewenste videokaarten en de gescrapete videokaarten
    with open(gewenste_file, "r") as gewenste_f:

        # Filter de gewenste modellen
        for row in gewenste_f:

            # Maak alles kleine letters en verwijder extra lege lijnen
            row = row.replace("\n", "").lower()
            row, data = verwijder_haakjes(row)

            socket = ""
            snelheid = ""
            if gewenste_file == "cpus.txt":
                socket, row = scheid_str(row, ";")

            elif gewenste_file == "ram_ddr4.txt" or gewenste_file == "ram_ddr5.txt":
                snelheid = re.search('\|(.*)\|', row).group(1)
                grootte = re.search('~(.*)~', row).group(1)
                row = row.replace("~", "")

            # Scheid de videokaart namen
            row = scheid_str(row, ":")

            # Maak lijst voor matches
            matches = []

            # Open de file met gescrapete videokaarten
            with open(gescrapede_file, "r+") as scraped_f:
                content = scraped_f.readlines()
                # Loep over de gescrapete videokaarten
                for i, line in enumerate(content):

                    naam_oud = line.lower()
                    naam_oud= naam_oud.strip("\n")

                    if snelheid != "":
                        naam_oud += f"~{grootte}~"
                        naam_oud += f";{snelheid}\n"

                    if data != None:
                        naam_oud += "<" + ', '.join(data) + ">"
                        if socket != "":
                            naam_oud += f";{socket}"
                        naam_oud = "".join(line.strip() for line in naam_oud.splitlines()) + "\n"
                    else:
                        if gewenste_file == "psus.txt":
                            naam_oud += "\n"
                    if gewenste_file == "opslag.txt":
                        opslag_type = row[0].replace("|", " ")
                        naam_oud += f";{opslag_type}\n"

                    # Scheid de naam en prijs
                    naam = scheid_str(line, ":")[1].lower()

                    if "|" in row[0]:
                        gesplit = row[0].split("|")

                        if check_of_in_woord(gesplit, naam):
                            # Voeg hem toe samen met prijs en index aan de lijst met matches
                            prijs = int(scheid_str(line, ":")[0].strip("\n"))
                            if gewenste_file == "psus.txt":
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
                            if gewenste_file == "moederborden.txt":
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
filter("cpus.txt", "scraped_cpus.txt", "results_cpus.txt")
filter("gpus.txt", "scraped_gpus.txt", "results_gpus.txt")
filter("moederborden.txt", "scraped_moederborden.txt", "results_moederborden.txt")
filter("opslag.txt", "scraped_opslag.txt", "results_opslag.txt")
filter("ram_ddr4.txt", "scraped_ram_ddr4.txt", "results_ram_ddr4.txt")
filter("ram_ddr5.txt", "scraped_ram_ddr5.txt", "results_ram_ddr5.txt")
filter("psus.txt", "scraped_psus.txt", "results_psus.txt")
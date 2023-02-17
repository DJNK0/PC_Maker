import re


"""
Scheid een string in 2 delen, 
een deel links van het teken en het andere rechts van het teken"""
def scheid_str(s, teken):
    for i, char in enumerate(s):
        if char == teken:
            helft_1 = s[:i]
            helft_2 = s[i + 1:]
            return helft_1, helft_2


""" Verwijder haakjes van een string en return de string 
en de data tussen de haakjes los van elkaar"""
def verwijder_haakjes(s):
    data = re.search("<(.*)>", s)
    if data is not None:
        data = data.group(1)
        data = data.split(",")

    s = re.sub('<.*?>', '', s)
    return s, data


# return factoren voor het budget van de computer op basis van het doel
def doeleind(doel):
    if doel == "gaming":
        return {"min_budget_gpu": 35, "max_budget_gpu": 45, "min_budget_platform": 33, "max_budget_platform": 42}

    if doel == "professioneel":
        return {"min_budget_gpu": 23, "max_budget_gpu": 33, "min_budget_platform": 40, "max_budget_platform": 55}


# Deze functie kiest een videokaart op basis van budget en het doel van de computer
def kies_gpu(budget, doel, doeleind_data):
    videokaarten = []
    gpu_opties = []
    videokaarten_f = open("data/results_data/results_gpus.txt", "r")
    videokaarten_content = videokaarten_f.readlines()

    # Loep over de gescrapete videokaarten
    for lijn in videokaarten_content:
        # Maak de prijs en de data los van elke lijn
        videokaart_met_prijs, data = verwijder_haakjes(lijn)
        videokaart, prijs = scheid_str(videokaart_met_prijs, ":")
        prijs = int(prijs.strip("\n"))

        # voeg de geformatteerde data toe aan een lijst op basis van het doel
        if doel == "gaming":
            data = [int(data[0]), (int(data[2]))]
            videokaarten.append((videokaart, prijs, data))
        else:
            data = [int(data[1]), (int(data[2]))]
            videokaarten.append((videokaart, prijs, data))

    # Bereken het minimale en maximale budget van de gpu
    min_budget_gpu = budget * doeleind_data["min_budget_gpu"] / 100
    max_budget_gpu = budget * doeleind_data["max_budget_gpu"] / 100

    # Sorteer videokaarten op basis van prijs
    videokaarten.sort(key=lambda x: x[1])

    # Loep over videokaarten
    for videokaart in videokaarten:
        # Als de videokaart binnen het minimale en maximale budget is
        if min_budget_gpu <= videokaart[1] <= max_budget_gpu:
            """Bereken de prijs/kwaliteit ratio 
            en voeg de gpu samen met bijbehorende data toe aan een lijst"""
            ratio = videokaart[2][0] / videokaart[1]
            gpu_opties.append((videokaart[0],videokaart[1], ratio, videokaart[2][1]))

    # Als er geen videokaart gevonden kan worden
    if len(gpu_opties) == 0:
        if budget < 900:
            return "error", "error"

        # Sorteer videokaarten op basis van snelheid
        videokaarten.sort(key=lambda x: x[2])

        # Vind de snelste videokaart en voeg hem toe aan de opties
        beste_videokaart = videokaarten[-1]
        beste_videokaart_ratio = beste_videokaart[2][0] / beste_videokaart[1]
        gpu_opties.append((beste_videokaart[0], beste_videokaart[1], beste_videokaart_ratio, beste_videokaart[2][1]))
    print("sssss")
    # Sorteer de opties op prijs/ratio verhouding en return de beste
    gpu_opties.sort(key=lambda x: x[2], reverse=True)

    return budget, gpu_opties[0]

""" 
Alleen ddr4 ram
Functie om de ram te berekenen op basis van doel, 
een lijn van de gescrapete ram bestand en andere data van de ram"""
def bereken_ram_ddr4(doel, lijn, socket, gewenste_grootte, data):
    # Vind de grootte van de ram
    grootte = re.search("~(.*)~", lijn).group(1)

    # Als de ram voor gaming wordt gebruikt en voldoet aan de gewenste grootte
    if doel == "gaming":
        if grootte == gewenste_grootte:
            # Formatteer de data
            ram, snelheid = scheid_str(lijn, ";")
            snelheid = int(snelheid)
            ram = re.sub('~.*?~', '', ram)

            # bereken de snelheid van de ram
            som = ((snelheid - 2666) / 1734) * 11
            som = 11 - som

            if socket == "1700":
                som = (94 - som) / 100
            else:
                som = (100 - som) / 100

            # return de ram en de snelheid van de ram verrekend met de snelheid van de cpu
            return ram, som * int(data[0])
        return None, None
    # Bereken snelheid maar nu voor productieve doeleinden
    else:
        if grootte == gewenste_grootte:
            ram, snelheid = scheid_str(lijn, ";")
            ram = re.sub('~.*?~', '', ram)

            return ram, int(data[0])
        return None, None


# Doet hetzelfde als voor ddr4 met andere waardes om de snelheid te berekenen
def bereken_ram_ddr5(doel, lijn, gewenste_grootte, data):
    grootte = re.search("~(.*)~", lijn).group(1)
    if doel == "gaming":
        if grootte == gewenste_grootte:
            ram, snelheid = scheid_str(lijn, ";")
            snelheid = int(snelheid)
            ram = re.sub('~.*?~', '', ram)
            som = ((snelheid - 4800) / 1600) * 9
            som = 9 - som
            som = (100 - som) / 100
            return ram, som * int(data[0])
        return None, None
    else:
        if grootte == gewenste_grootte:
            ram, snelheid = scheid_str(lijn, ";")
            ram = re.sub('~.*?~', '', ram)

            return ram, int(data[0])
        return None, None


# Deze functie zoekt een specifiek moederbord
def zoek_moederbord(moederbord):
    moederborden_f = open("data/results_data/results_moederborden.txt", "r")
    moederborden_content = moederborden_f.readlines()

    for lijn in moederborden_content:
        if moederbord in lijn:
            return lijn.split(";")[0]


# Deze functie zoekt een specifieke koeler
def zoek_koeler(koeler):
    koeler_f = open("data/results_data/results_coolers.txt", "r")
    koeler_content = koeler_f.readlines()

    for lijn in koeler_content:
        if koeler in lijn.lower():
            return lijn


# Functie om het moederbord te kiezen op basis van de prijs en socket van de cpu
def kies_moederbord(socket, cpu_prijs):
    if socket == "am4":
        if cpu_prijs > 200:
            if cpu_prijs > 300:
                return zoek_moederbord("msi mag b550 tomahawk")
            else:
                return zoek_moederbord("b550m aorus elite")
        else:
            return zoek_moederbord("b450")
    if socket == "am5":
        if cpu_prijs > 300:
            if cpu_prijs > 450:
                return zoek_moederbord("asus tuf gaming x670e-plus")
            else:
                aorus_elite = zoek_moederbord("b650 aorus elite ax")
                tuf_gaming = zoek_moederbord("asus tuf gaming x670e-plus")

                if int(scheid_str(tuf_gaming, ":")[1]) < int(scheid_str(aorus_elite, ":")[1]):
                    return tuf_gaming
                else:
                    return aorus_elite
        else:
            return zoek_moederbord("b650")

    if socket == "1700":
        if cpu_prijs > 200:
            if cpu_prijs > 300:
                if cpu_prijs > 400:
                    if cpu_prijs > 500:
                        return zoek_moederbord("rog maximus z790 hero")
                    else:
                        return zoek_moederbord("z790 aorus elite")
                else:
                    return zoek_moederbord("tuf gaming b660m-plus")
            else:
                return zoek_moederbord("msi pro b660m-p")
        else:
            return zoek_moederbord("b660")


# Deze functie kiest de juiste koeler op basis van tdp
def kies_koeler(data):
    if int(data[3]) != 1:
        if int(data[2]) > 105:
            if int(data[2]) > 165:
                return zoek_koeler("arctic liquid freezer")
            else:
                return zoek_koeler("arctic freezer 34")
        else:
            return zoek_koeler("cooler master hyper")


"""
Deze functie stelt het platform samen
(processor, geheugen, koeling)
"""
def kies_platform(doel, doeleind_data, budget):
    platformen = []
    min_budget_platform = budget * doeleind_data["min_budget_platform"] / 100
    max_budget_platform = budget * doeleind_data["max_budget_platform"] / 100

    with open("data/results_data/results_cpus.txt", "r") as cpu_f:
        cpu_content = cpu_f.readlines()
        for lijn in cpu_content:
            cpu_met_prijs, data = verwijder_haakjes(lijn)
            cpu_met_prijs, socket = scheid_str(cpu_met_prijs, ";")
            socket = socket.strip("\n")
            cpu, cpu_prijs = scheid_str(cpu_met_prijs, ":")
            cpu_prijs = int(cpu_prijs.strip("\n"))

            moederbord = kies_moederbord(socket, cpu_prijs)
            moederbord, moederbord_prijs = scheid_str(moederbord, ":")

            koeler = kies_koeler(data)
            koeler_prijs = 0
            if koeler != None:
                koeler, koeler_prijs = scheid_str(koeler, ":")

            ddr5_f = open("data/results_data/results_ram_ddr5.txt", "r")
            ddr5_content = ddr5_f.readlines()
            ddr4_f = open("data/results_data/results_ram_ddr4.txt", "r")
            ddr4_content = ddr4_f.readlines()

            snelheden = []
            if socket == "am4":
                ram = "ddr4"
            elif socket == "am5":
                ram = "ddr5"
            else:
                ram = "1700"

            if doel == "gaming":
                if cpu_prijs > 450:
                    gewenste_grootte = "2x16"
                elif cpu_prijs < 100:
                    gewenste_grootte = "2x4"
                else:
                    gewenste_grootte = "2x8"

                if ram == "ddr4":
                    for product in ddr4_content:
                        ram_schoon, snelheid = bereken_ram_ddr4(doel, product, socket, gewenste_grootte, data)
                        if snelheid is not None:
                            snelheden.append((ram_schoon, snelheid))
                elif ram == "ddr5":
                    for product in ddr5_content:
                        ram_schoon, snelheid = bereken_ram_ddr5(doel, product, gewenste_grootte, data)
                        if snelheid is not None:
                            snelheden.append((ram_schoon, snelheid))
                else:
                    for product in ddr5_content:

                        ram_schoon, snelheid = bereken_ram_ddr4(doel, product, socket, gewenste_grootte, data)
                        if snelheid is not None:
                            snelheden.append((ram_schoon, snelheid))

                    for product in ddr5_content:
                        ram_schoon, snelheid = bereken_ram_ddr5(doel, product, gewenste_grootte, data)
                        if snelheid is not None:
                            snelheden.append((ram_schoon, snelheid))
            else:
                if cpu_prijs > 250:
                    if cpu_prijs > 450:
                        gewenste_grootte = "4x16"
                    else:
                        gewenste_grootte = "450"
                else:
                    gewenste_grootte = "2x8"
                if ram == "ddr4":
                    for product in ddr4_content:
                        ram_schoon, snelheid = bereken_ram_ddr4(doel, product, socket, gewenste_grootte, data)
                        if snelheid is not None:
                            snelheden.append((ram_schoon, snelheid))
                elif ram == "ddr5":
                    for product in ddr5_content:
                        ram_schoon, snelheid = bereken_ram_ddr5(doel, product, gewenste_grootte, data)
                        if snelheid is not None:
                            snelheden.append((ram_schoon, snelheid))
                else:
                    if "z790" in moederbord:

                        for product in ddr5_content:
                            ram_schoon, snelheid = bereken_ram_ddr5(doel, product, gewenste_grootte, data)
                            if snelheid is not None:
                                snelheden.append((ram_schoon, snelheid))
                    else:
                        for product in ddr4_content:
                            ram_schoon, snelheid = bereken_ram_ddr4(doel, product, socket, gewenste_grootte, data)
                            if snelheid is not None:
                                snelheden.append((ram_schoon, snelheid))

            for snelheid in snelheden:
                ram, ram_prijs = scheid_str(snelheid[0], ":")
                platform_prijs = int(ram_prijs) + int(cpu_prijs) + int(koeler_prijs) + int(moederbord_prijs)
                ratio = snelheid[1] / platform_prijs

                platformen.append([ratio, platform_prijs, cpu, cpu_prijs, int(data[2]),
                                   moederbord, moederbord_prijs, ram, ram_prijs, koeler,
                                   koeler_prijs, snelheid[1]])
        mogelijke_platformen = []
        for platform in platformen:
            if min_budget_platform <= platform[1] <= max_budget_platform:
                mogelijke_platformen.append(platform)

        if len(mogelijke_platformen) == 0:
            platformen.sort(key=lambda x: x[1])
            if budget < 1000:
                return "error","error","error","error","error","error","error","error","error","error","error"
            platformen.sort(key=lambda x:x[-1], reverse=True)
            platform = platformen[0]
            platform.pop(0)
            return platform

    mogelijke_platformen.sort(reverse=True)
    platform = mogelijke_platformen[0]
    platform.pop(0)
    return platform


# Kies een voeding op basis van het budget en de tdp's van de processor en videokaart
def kies_psu(budget, tdp_cpu, tdp_gpu):
    # Bereken minimaal vereiste wattage van de voeding
    totaal_tdp = tdp_gpu + tdp_cpu
    min_watt = totaal_tdp * 1.8

    psu_f = open("data/results_data/results_psus.txt", "r")
    psu_content = psu_f.readlines()

    # Kies efficiëntie van de voeding op basis van budget
    if budget > 700:
        if budget > 2500:
            if budget > 3500:
                gewenste_eff = "titanium"
            else:
                gewenste_eff = "platinum"
        else:
            gewenste_eff = "gold"
    else:
        gewenste_eff = "bronze"

    """ Loep over de gescrapete voedingen tot een voeding gevonden wordt 
    die voldoet aan de gewenste efficiëntie en minimale wattage."""
    for line in psu_content:
        psu, wattage = scheid_str(line, ";")

        if int(wattage) < min_watt:
            continue

        if "bronze" in psu:
            eff = "bronze"
        elif "gold" in psu:
            eff = "gold"
        elif "platinum" in psu:
            eff = "platinum"
        else:
            eff = "titanium"
        if gewenste_eff == eff:
            return scheid_str(psu, ":")

    # Verwijder onnodige data van de lijn en return deze.
    psu, wattage = scheid_str(line, ";")
    psu_f.close()
    return scheid_str(psu, ":")


# Kies de gewenste behuizing op basis van budget
def kies_behuizing(budget):
    behuizing_f = open("data/results_data/results_behuizing.txt", "r")
    behuizing_content = behuizing_f.readlines()

    # kies de behuizing op basis van budget
    if budget > 700:
        if budget > 1000:
            if budget > 2500:
                gewenste_behuizing = "fractal design"
            else:
                gewenste_behuizing = "corsair 4000d"
        else:
            gewenste_behuizing = "aerocool hexform"
    else:
        # De goedkoopste behuizing
        behuizing = scheid_str(behuizing_content[0], ":")
        return behuizing

    # Loep over de gescrapete behuizingen totdat de juiste gevonden is.
    for line in behuizing_content:
        if gewenste_behuizing in line.lower():
            return scheid_str(line, ":")


# Functie om de gewenste opslag te vinden op basis van budget
def kies_opslag(budget):
    opslag_f = open("data/results_data/results_opslag.txt", "r")
    opslag_content = opslag_f.readlines()

    """ Vind het opslag type voor elke lijn en stop deze in een dictionary 
    samen met de naam van de opslag en de prijs """
    opslagen = {}
    for line in opslag_content:
        opslag, opslag_type = scheid_str(line, ";")
        opslag, opslag_prijs = scheid_str(opslag, ":")
        opslag_type = opslag_type.strip("\n")
        opslagen[opslag_type] = (opslag, int(opslag_prijs))

    # Kies de juiste opslag op basis van budget
    if budget > opslagen["ssd 480gb"][1]:
        if budget > opslagen["ssd 960gb"][1]:
            if budget > opslagen["ssd 240gb"][1] + opslagen["hdd 2tb"][1]:
                if budget > opslagen["m.2 1tb"][1]:
                    if budget > opslagen["ssd 480gb"][1] + opslagen["hdd 2tb"][1]:
                        if budget > opslagen["m.2 1tb"][1] + opslagen["hdd 2tb"][1]:
                            if budget > opslagen["m.2 2tb"][1]:
                                if budget > opslagen["m.2 1tb"][1] + opslagen["hdd 4tb"][1]:
                                    if budget > opslagen["m.2 2tb"][1] + opslagen["hdd 4tb"][1]:
                                        if budget > opslagen["m.2 1tb"][1] + opslagen["ssd 4tb"][1]:
                                            if budget > opslagen["m.2 2tb"][1] + opslagen["ssd 4tb"][1]:
                                                if budget > opslagen["m.2 2tb"][1]  + opslagen["ssd 8tb"][1]:
                                                    if budget > opslagen["m.2 4tb"][1] + opslagen["ssd 8tb"][1]:
                                                        return opslagen["m.2 4tb"] + opslagen["ssd 8tb"]
                                                    else:
                                                        return opslagen["m.2 2tb"] + opslagen["ssd 8tb"]
                                                else:
                                                    return opslagen["m.2 2tb"] + opslagen["ssd 4tb"]
                                            else:
                                                return opslagen["m.2 1tb"] + opslagen["ssd 4tb"]
                                        else:
                                            return opslagen["m.2 2tb"] + opslagen["hdd 4tb"]
                                    else:
                                        return opslagen["m.2 1tb"] + opslagen["hdd 4tb"]
                                else:
                                    return opslagen["m.2 2tb"]
                            else:
                                return opslagen["m.2 1tb"] + opslagen["hdd 2tb"]
                        else:
                            return opslagen["ssd 480gb"] + opslagen["hdd 2tb"]
                    else:
                        return opslagen["m.2 1tb"]
                else:
                    return opslagen["ssd 240gb"] + opslagen["hdd 2tb"]
            else:
                return opslagen["ssd 960gb"]
        else:
            return opslagen["ssd 480gb"]
    else:
        return opslagen["ssd 240gb"]


# Deze functie combineert alle functies en stelt de gehele computer samen
def bereken_computer(budget, doel):
    doeleind_data = doeleind(doel)

    budget, gpu_data = kies_gpu(budget, doel, doeleind_data)

    """Als er geen gpu gevonden kan worden, 
    return 0 zodat het programma weet dat er een nieuw budget gekozen moet worden """
    if gpu_data == "error":
        return 0
    gpu, gpu_prijs, _, tdp_gpu = gpu_data

    (platform_prijs,
     cpu, cpu_prijs, tdp_cpu,
     moederbord, moederbord_prijs,
     ram, ram_prijs,
     koeling, koeling_prijs, cpu_perf) = kies_platform(doel, doeleind_data, budget)

    """Als er geen platform gevonden kan worden, 
        return 0 zodat het programma weet dat er een nieuw budget gekozen moet worden """
    if cpu == "error":
        return 0

    psu, psu_prijs = kies_psu(budget, tdp_cpu, tdp_gpu)
    psu_prijs = int(psu_prijs)
    behuizing, behuizing_prijs = kies_behuizing(budget)
    behuizing_prijs = int(behuizing_prijs)

    budget_over = budget - gpu_prijs - platform_prijs - psu_prijs - behuizing_prijs
    opslag = kies_opslag(budget_over)

    if koeling is None:
        koeling = "Koeling is bij de processor geleverd."
        koeling_prijs = "-"

    """ 
    Als de opslag variabele geen string is dan bevat de configuratie meerde producten, 
    dan wordt er over de opslag lijst geloept. Als het item in de lijst een integer is, 
    dan wordt het item toegevoegd aan de totale prijs van de opslag. 
     Anders is het de naam van het opslag product, 
    in dat geval voegen we <br> tags toe zodat ze op de site mooi op losse regels verschijnen."""
    opslag_final = ""
    opslag_prijs = 0
    if not isinstance(opslag, str):
        for item in opslag:
            if not isinstance(item, int):
                opslag_final += item + "<br>"
            else:
                opslag_prijs += item

    return (gpu, gpu_prijs, cpu, cpu_prijs,
            psu, psu_prijs, moederbord, moederbord_prijs,
            ram, ram_prijs, koeling, koeling_prijs,
            behuizing,behuizing_prijs, opslag_final, opslag_prijs)


if __name__ == "__main__":
    computer = bereken_computer(550, "gaming")
    print(computer)
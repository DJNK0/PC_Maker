import re

def scheid_str(str, teken):
    for i, char in enumerate(str):
        # Scheid tussen de dubbele punt
        if char == teken:

            helft_1 = str[:i]
            helft_2 = str[i + 1:]

            return(helft_1, helft_2)

def verwijder_haakjes(str):
    data = re.search("<(.*)>", str)
    if data != None:
        data = data.group(1)
        data = data.split(",")

    str = re.sub('<.*?>', '', str)
    return(str, data)

def doeleind():
    doel = input("Wat is het doel?")
    if doel == "gaming":
        return doel, {"min_budget_gpu":35, "max_budget_gpu":45, "min_budget_platform":33, "max_budget_platform":42}

    if doel == "professioneel":
        return doel, {"min_budget_gpu":23, "max_budget_gpu":33, "min_budget_platform":40, "max_budget_platform":55}

doel, doeleind_data = doeleind()

def closest(list, Number):
    aux = []
    for valor in list:
        aux.append(abs(Number-valor))

    return aux.index(min(aux))

def kies_gpu():
    budget = int(input("wat is het budget"))
    videokaarten = []
    with open("results_gpus.txt", "r") as videokaarten_f:
        videokaarten_content = videokaarten_f.readlines()
        for lijn in videokaarten_content:
            videokaart_met_prijs, data = verwijder_haakjes(lijn)
            videokaart, prijs = scheid_str(videokaart_met_prijs, ":")
            prijs = int(prijs.strip("\n"))

            if doel == "gaming":
                data = [int(data[0]), (int(data[2]))]
                videokaarten.append((videokaart, prijs, data))
            else:
                data = [int(data[1]), (int(data[2]))]
                videokaarten.append((videokaart, prijs, data))

    min_budget_gpu = budget * doeleind_data["min_budget_gpu"] / 100
    max_budget_gpu = budget * doeleind_data["max_budget_gpu"] / 100
    videokaarten.sort(key=lambda x: x[1])

    print(min_budget_gpu, videokaarten[-1][1])
    print(max_budget_gpu, videokaarten[0][1])

    gpu_opties = []
    if min_budget_gpu <= videokaarten[-1][1] and max_budget_gpu <= videokaarten[0][1]:
        videokaart_prijzen = []
        for videokaart in videokaarten:
            print(videokaart)
            videokaart_prijzen.append(videokaart[1])

        dichtsbijzijnde = (closest(videokaart_prijzen, min_budget_gpu))
        print(videokaarten[dichtsbijzijnde])
    if min_budget_gpu >= videokaarten[-1][1]:
        videokaarten.sort(key=lambda x: x[2])
        beste_videokaart = videokaarten[-1]

        beste_videokaart_ratio = beste_videokaart[2][0] / beste_videokaart[1]
        gpu_opties.append((beste_videokaart[0], beste_videokaart[1], beste_videokaart_ratio))

    if max_budget_gpu <= videokaarten[0][1]:
        kies_gpu()


    for videokaart in videokaarten:
        if min_budget_gpu <= videokaart[1] <= max_budget_gpu:
            ratio = videokaart[2][0] / videokaart[1]
            gpu_opties.append((videokaart[0],videokaart[1], ratio))
    print(gpu_opties)
    gpu_opties.sort(key=lambda x: x[2])
    return budget, gpu_opties[0][0], gpu_opties[0][1]
gpu = kies_gpu()
print(gpu)
budget = gpu[0]
def bereken_ram_ddr4(lijn, socket, gewenste_grootte, data):

    grootte = re.search("~(.*)~", lijn).group(1)
    if grootte == gewenste_grootte:
        ram, snelheid = scheid_str(lijn, ";")
        snelheid = int(snelheid)
        ram = re.sub('~.*?~', '', ram)
        som = ((snelheid - 2666) / 1734) * 11
        som = 11 - som
        if socket == "1700":
            som = (94 - som) / 100
        else:
            som = (100 - som) / 100

        return ram, som * int(data[0])
    return None, None

def bereken_ram_ddr5(lijn, gewenste_grootte, data):
        grootte = re.search("~(.*)~", lijn).group(1)
        if grootte == gewenste_grootte:
            ram, snelheid = scheid_str(lijn, ";")
            snelheid = int(snelheid)
            ram = re.sub('~.*?~', '', ram)
            som = ((snelheid - 4800) / 1600) * 9
            som = 9 - som
            som = (100 - som) / 100

            return ram, som * int(data[0])
        return None, None

def zoek_moederbord(moederbord):
    moederborden_f = open("results_moederborden.txt", "r")
    moederborden_content = moederborden_f.readlines()

    for lijn in moederborden_content:
        if moederbord in lijn:
            return lijn.split(";")[0]

def zoek_koeler(koeler):
    koeler_f = open("results_coolers.txt", "r")
    koeler_content = koeler_f.readlines()

    for lijn in koeler_content:
        if koeler in lijn.lower():
            return lijn

def kies_moederbord(cpu, socket, prijs):
    if socket == "am4":
        if prijs > 200:
            if prijs > 300:
                return zoek_moederbord("msi mag b550 tomahawk")
            else:
                return zoek_moederbord("b550m aorus elite")
        else:
            return zoek_moederbord("b450")

    if socket == "am5":

        if prijs > 300:
            if prijs > 450:
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
        if prijs > 200:
            if prijs > 300:
                if prijs > 400:
                    if prijs > 500:
                        return zoek_moederbord("rog maximus z790 hero")
                    else:
                        return zoek_moederbord("z790 aorus elite")
                else:
                    return zoek_moederbord("tuf gaming b660m-plus")
            else:
                return zoek_moederbord("msi pro b660m-p")
        else:
            return zoek_moederbord("b660")

def kies_koeler(data):
    if int(data[3]) != 1:
        if int(data[2]) > 105:
            if int(data[2]) > 165:
                return zoek_koeler("arctic liquid freezer")
            else:
                return zoek_koeler("arctic freezer 34")
        else:
            return zoek_koeler("cooler master hyper")

def kies_platform():
    platformen = []
    min_budget_platform = budget * doeleind_data["min_budget_platform"] / 100
    max_budget_platform = budget * doeleind_data["max_budget_platform"] / 100

    with open("results_cpus.txt", "r") as cpu_f:
        cpu_content = cpu_f.readlines()
        for lijn in cpu_content:
            cpu_met_prijs, data = verwijder_haakjes(lijn)
            cpu_met_prijs, socket = scheid_str(cpu_met_prijs, ";")
            socket = socket.strip("\n")
            cpu, cpu_prijs = scheid_str(cpu_met_prijs, ":")
            cpu_prijs = int(cpu_prijs.strip("\n"))

            moederbord = kies_moederbord(cpu, socket, cpu_prijs)
            moederbord, moederbord_prijs = scheid_str(moederbord, ":")

            koeler = kies_koeler(data)
            koeler_prijs = 0
            if koeler != None:
                koeler, koeler_prijs = scheid_str(koeler, ":")

            ddr5_f = open("results_ram_ddr5.txt", "r")
            ddr5_content = ddr5_f.readlines()
            ddr4_f = open("results_ram_ddr4.txt", "r")
            ddr4_content = ddr4_f.readlines()

            snelheden = []


            if doel == "gaming":
                if cpu_prijs > 450:
                    gewenste_grootte = "2x16"
                elif cpu_prijs < 100:
                    gewenste_grootte = "2x4"
                else:
                    gewenste_grootte = "2x8"

                if socket == "am4":
                    ram = "ddr4"
                elif socket == "am5":
                    ram = "ddr5"
                else:
                    ram = "ddr4"

                if ram == "ddr4":
                    for product in ddr4_content:
                        ram_schoon, snelheid = bereken_ram_ddr4(product,socket, gewenste_grootte, data)
                        if snelheid != None:
                            snelheden.append((ram_schoon, snelheid))

                if ram == "ddr5":
                    for product in ddr5_content:
                        ram_schoon, snelheid = bereken_ram_ddr5(product, gewenste_grootte, data)
                        if snelheid != None:
                            snelheden.append((ram_schoon, snelheid))

                else:
                    ram_schoon, snelheid = bereken_ram_ddr4(product, socket, gewenste_grootte, data)
                    if snelheid != None:
                        snelheden.append((ram_schoon, snelheid))

                    ram_schoon, snelheid = bereken_ram_ddr5(product, gewenste_grootte, data)
                    if snelheid != None:
                        snelheden.append((ram_schoon, snelheid))

            for snelheid in snelheden:
                ram, ram_prijs = scheid_str(snelheid[0], ":")
                platform_prijs = int(ram_prijs) + int(cpu_prijs) + int(koeler_prijs) + int(moederbord_prijs)
                ratio = snelheid[1] / platform_prijs

                if min_budget_platform <= platform_prijs <= max_budget_platform:
                    platformen.append((ratio, platform_prijs, cpu, moederbord, ram, koeler))
        platformen.sort()
        print(platformen[0])

kies_platform()
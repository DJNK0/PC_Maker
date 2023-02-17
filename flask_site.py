from flask import Flask, render_template, request
import bereken_computer

app = Flask(__name__)

""" 
Deze functie kiest welke html template hij naar de site moet sturen, 
en welke variabelen hij moet sturen
"""
@app.route("/", methods=['GET', 'POST'])
def home():
    """
    Als er een input is van een gebruiker, bijvoorbeeld
    als er een knop wordt ingedrukt
    """
    if request.method == "POST":
        # Als het de submit knop is
        if request.form.get("submit_btn") == "0":

            # Lees het budget wat de gebruiker heeft ingevuld
            budget = request.form.get("budget")
            if budget != "":
                budget = int(budget)
            # Als het budget niet is ingevuld meld dit aan de gebruiker
            else:
                return render_template("home.html", error=1)
            # Als het budget te laag is meldt dit aan de gebruiker
            if budget < 450:
                return render_template("home.html", error=1)

            # Lees waarvoor de gebruiker de computer wilt gebruiken
            if request.form.get("Productiviteit") == "Productiviteit":
                gebruiks_case = "professioneel"
            else:
                gebruiks_case = "gaming"

            # Bereken de computer op basis van de input van de gebruiker
            computer = bereken_computer.bereken_computer(budget, gebruiks_case)

            # Als er geen mogelijke computer gevonden is voor dit budget meldt dit aan de gebruiker
            if computer == 0:
                return render_template("home.html", error=1)

            # Formatteer de juiste variabelen
            (gpu, gpu_prijs, cpu, cpu_prijs,
             psu, psu_prijs, moederbord, moederbord_prijs,
             ram, ram_prijs, koeling, koeling_prijs,
             behuizing, behuizing_prijs,
             opslag, opslag_prijs) = computer
            totaal_prijs = (int(gpu_prijs) + int(cpu_prijs) + int(psu_prijs) +
                            int(moederbord_prijs)+ int(ram_prijs) +
                            int(behuizing_prijs) + int(opslag_prijs))
            if koeling_prijs != "-":
                totaal_prijs += int(koeling_prijs)

            # Stuur de losse computeronderdelen naar de site
            return render_template("computer.html", gpu=gpu, gpu_prijs=gpu_prijs,
                                   cpu=cpu, cpu_prijs=cpu_prijs,
                                   psu=psu, psu_prijs=psu_prijs,
                                   moederbord=moederbord, moederbord_prijs=moederbord_prijs,
                                   ram=ram, ram_prijs=ram_prijs,
                                   koeling=koeling, koeling_prijs=koeling_prijs,
                                   behuizing=behuizing, behuizing_prijs=behuizing_prijs,
                                   opslag=opslag, opslag_prijs=opslag_prijs, totaal_prijs=totaal_prijs)
    # Als er geen input is van de gebruiker return de normale site
    return render_template("home.html", error=0)


# Zorg dat de app daadwerkelijk start
if __name__ == "__main__":
    app.run(debug=True)



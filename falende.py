
from flask import Flask, render_template, request
import programmayes

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        if request.form.get("submit_btn") == "0":

            budget = request.form.get("budget")
            if budget != "":
                budget = int(budget)
            else:
                return render_template("home_error.html")
            if budget < 450:
                return render_template("home_error.html")

            if request.form.get("Productiviteit") == "Productiviteit":
                gebruiks_case = "professioneel"
            else:
                gebruiks_case = "gaming"
            computer = programmayes.main(budget, gebruiks_case)
            if computer == 0:
                return render_template("home_error.html")
            (gpu, gpu_prijs, cpu, cpu_prijs,
             psu, psu_prijs, moederbord, moederbord_prijs,
             ram, ram_prijs, koeling, koeling_prijs,
             behuizing, behuizing_prijs,
             opslag, opslag_prijs) = computer

            return render_template("computer.html", gpu=gpu, gpu_prijs=gpu_prijs,
                                   cpu=cpu, cpu_prijs=cpu_prijs,
                                   psu=psu, psu_prijs=psu_prijs,
                                   moederbord=moederbord, moederbord_prijs=moederbord_prijs,
                                   ram=ram, ram_prijs=ram_prijs,
                                   koeling=koeling, koeling_prijs=koeling_prijs,
                                   behuizing=behuizing, behuizing_prijs=behuizing_prijs,
                                   opslag=opslag, opslag_prijs=opslag_prijs)
        if request.form.get("submit_btn") == "0":
            pass
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)



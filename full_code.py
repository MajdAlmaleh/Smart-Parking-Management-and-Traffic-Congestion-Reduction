"""
Smart Fuzzy Parking Management System
Dynamic Parking Pricing using Fuzzy Logic
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext

import numpy as np
import matplotlib.pyplot as plt

import skfuzzy as fuzz
from skfuzzy import control as ctrl



RANGE = np.arange(0, 101, 1)


occupancy = ctrl.Antecedent(RANGE, "occupancy")
traffic = ctrl.Antecedent(RANGE, "traffic")
arrival_rate = ctrl.Antecedent(RANGE, "arrival_rate")
time_demand = ctrl.Antecedent(RANGE, "time_demand")

price = ctrl.Consequent(RANGE, "price")







def create_three_levels(variable, names):

    variable[names[0]] = fuzz.trapmf(
        RANGE, [0, 0, 25, 40]
    )

    variable[names[1]] = fuzz.trimf(
        RANGE, [30, 50, 70]
    )

    variable[names[2]] = fuzz.trapmf(
        RANGE, [60, 80, 100, 100]
    )


create_three_levels(
    occupancy,
    ["low", "medium", "high"]
)

create_three_levels(
    traffic,
    ["low", "medium", "high"]
)

create_three_levels(
    arrival_rate,
    ["low", "medium", "high"]
)

create_three_levels(
    time_demand,
    ["offpeak", "normal", "rush"]
)


price["cheap"] = fuzz.trapmf(
    RANGE,[0,0,20,40]
)

price["normal"] = fuzz.trimf(
    RANGE,[30,50,70]
)

price["expensive"] = fuzz.trimf(
    RANGE,[60,80,95]
)

price["very_expensive"] = fuzz.trapmf(
    RANGE,[85,95,100,100]
)









rules = [



ctrl.Rule(
    occupancy["low"] &
    traffic["low"],
    price["cheap"]
),


ctrl.Rule(
    occupancy["low"] &
    traffic["medium"],
    price["normal"]
),


ctrl.Rule(
    occupancy["low"] &
    time_demand["rush"],
    price["normal"]
),




ctrl.Rule(
    occupancy["medium"] &
    traffic["low"] &
    time_demand["offpeak"],
    price["cheap"]
),


ctrl.Rule(
    occupancy["medium"] &
    arrival_rate["high"],
    price["expensive"]
),


ctrl.Rule(
    occupancy["medium"] &
    traffic["high"],
    price["expensive"]
),


ctrl.Rule(
    occupancy["medium"] &
    time_demand["rush"],
    price["expensive"]
),




ctrl.Rule(
    occupancy["high"] &
    traffic["low"],
    price["expensive"]
),


ctrl.Rule(
    occupancy["high"] &
    arrival_rate["medium"],
    price["very_expensive"]
),


ctrl.Rule(
    occupancy["high"] &
    arrival_rate["high"],
    price["very_expensive"]
),


ctrl.Rule(
    occupancy["high"] &
    traffic["medium"],
    price["very_expensive"]
),


ctrl.Rule(
    occupancy["high"] &
    traffic["high"],
    price["very_expensive"]
),




ctrl.Rule(
    traffic["high"] &
    arrival_rate["high"],
    price["very_expensive"]
),


ctrl.Rule(
    traffic["medium"] &
    arrival_rate["high"],
    price["expensive"]
),




ctrl.Rule(
    occupancy["medium"] &
    traffic["medium"] &
    arrival_rate["medium"] &
    time_demand["normal"],
    price["normal"]
)

]






system = ctrl.ControlSystem(rules)

simulation = ctrl.ControlSystemSimulation(system)







def calculate():

    try:

        simulation.reset()


        for key, entry in entries.items():

            value = float(entry.get())


            if not 0 <= value <= 100:
                raise ValueError


            simulation.input[key] = value


        simulation.compute()


        if "price" not in simulation.output:
            raise RuntimeError


        index = simulation.output["price"]


        
        if index < 35:

            message = "CHEAP\nEncourage parking"

        elif index < 70:

            message = "NORMAL\nBalanced demand"

        elif index < 85:

            message = "EXPENSIVE\nReduce demand"

        else:

            message = "VERY EXPENSIVE\nHeavy congestion"



        result_label.config(
            text=
            f"Dynamic Parking Price\n\n"
            f"Index: {((index/100)*20000):.0f}/hour\n\n"
            f"{message}"
        )


        price.view(sim=simulation)

        plt.show()



    except ValueError:

        messagebox.showerror(
            "Input Error",
            "Enter numbers between 0 and 100"
        )


    except Exception:

        messagebox.showerror(
            "System Error",
            "Could not calculate fuzzy result"
        )





tests = [

(10,20,20,20),
(50,50,50,50),
(90,90,90,90),
(70,85,80,95),
(30,20,30,20)

]



def run_tests():

    output.delete(
        "1.0",
        tk.END
    )


    for i,t in enumerate(tests):

        simulation.reset()


        simulation.input["occupancy"] = t[0]
        simulation.input["traffic"] = t[1]
        simulation.input["arrival_rate"] = t[2]
        simulation.input["time_demand"] = t[3]


        simulation.compute()


        result = simulation.output["price"]


        output.insert(
            tk.END,
            f"""
TEST {i+1}
----------------
Occupancy : {t[0]}
Traffic   : {t[1]}
Arrival   : {t[2]}
Time      : {t[3]}

PRICE INDEX = {result:.2f}

"""
        )





def graphs():

    fig, ax = plt.subplots(
        5,
        1,
        figsize=(8,15)
    )


    occupancy.view(ax=ax[0])
    traffic.view(ax=ax[1])
    arrival_rate.view(ax=ax[2])
    time_demand.view(ax=ax[3])
    price.view(ax=ax[4])


    plt.tight_layout()
    plt.show()




from tkinter import ttk


window = tk.Tk()

window.title("Smart Fuzzy Parking Controller")
window.geometry("900x700")
window.resizable(False, False)

BG = "#0f172a"
CARD = "#1e293b"
TEXT = "#e2e8f0"
ACCENT = "#38bdf8"
GREEN = "#22c55e"


window.configure(bg=BG)



style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TButton",
    font=("Segoe UI", 11, "bold"),
    padding=10
)

style.configure(
    "TLabel",
    background=BG,
    foreground=TEXT,
    font=("Segoe UI", 11)
)

style.configure(
    "Card.TFrame",
    background=CARD
)





header = tk.Frame(
    window,
    bg=BG
)

header.pack(pady=20)


tk.Label(
    header,
    text="🚗 Smart Parking AI",
    bg=BG,
    fg=ACCENT,
    font=("Segoe UI",26,"bold")
).pack()


tk.Label(
    header,
    text="Dynamic pricing using fuzzy logic",
    bg=BG,
    fg=TEXT,
    font=("Segoe UI",12)
).pack()





main = tk.Frame(
    window,
    bg=BG
)

main.pack(fill="both",expand=True,padx=30)



left = tk.Frame(
    main,
    bg=CARD,
    bd=0
)

left.pack(
    side="left",
    fill="y",
    padx=15
)


right = tk.Frame(
    main,
    bg=CARD
)

right.pack(
    side="right",
    fill="both",
    expand=True,
    padx=15
)






tk.Label(
    left,
    text="Parking Inputs",
    bg=CARD,
    fg=ACCENT,
    font=("Segoe UI",16,"bold")
).pack(pady=15)



def create_entry(label, icon):

    frame=tk.Frame(
        left,
        bg=CARD
    )

    frame.pack(
        pady=8,
        padx=20
    )


    tk.Label(
        frame,
        text=f"{icon} {label}",
        bg=CARD,
        fg=TEXT,
        anchor="w"
    ).pack(
        anchor="w"
    )


    e=tk.Entry(
        frame,
        font=("Segoe UI",12),
        width=22,
        justify="center"
    )

    e.pack(pady=5)

    return e



entries={

"occupancy":
create_entry(
"Occupancy %",
"🅿"
),


"traffic":
create_entry(
"Traffic %",
"🚦"
),


"arrival_rate":
create_entry(
"Arrival Rate %",
"🚘"
),


"time_demand":
create_entry(
"Demand %",
"⏰"
)

}



ttk.Button(
left,
text="Calculate Price",
command=calculate
).pack(
pady=20,
fill="x",
padx=25
)



ttk.Button(
left,
text="Show Graphs",
command=graphs
).pack(
pady=5,
fill="x",
padx=25
)



ttk.Button(
left,
text="Run Tests",
command=run_tests
).pack(
pady=5,
fill="x",
padx=25
)






result_label=tk.Label(

right,

text=
"""
Waiting for calculation...

Enter parking conditions
and press Calculate
""",

bg=CARD,

fg=TEXT,

font=("Segoe UI",15),

justify="center",

width=35,

height=8

)

result_label.pack(
pady=25
)





tk.Label(
right,
text="Simulation Output",
bg=CARD,
fg=ACCENT,
font=("Segoe UI",14,"bold")
).pack()



output=scrolledtext.ScrolledText(

right,

width=45,

height=14,

font=("Consolas",10),

bg="#020617",

fg=TEXT,

insertbackground="white"

)

output.pack(
padx=20,
pady=15
)



window.mainloop()

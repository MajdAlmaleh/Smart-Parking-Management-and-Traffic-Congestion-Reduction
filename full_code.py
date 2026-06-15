"""
Smart Fuzzy Parking Management System
Dynamic Pricing + Congestion + Parking Time Prediction
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk

import numpy as np
import matplotlib.pyplot as plt

import skfuzzy as fuzz
from skfuzzy import control as ctrl



RANGE=np.arange(0,101,1)



# ================= INPUTS =================


occupancy=ctrl.Antecedent(
    RANGE,
    "occupancy"
)


traffic=ctrl.Antecedent(
    RANGE,
    "traffic"
)


arrival_rate=ctrl.Antecedent(
    RANGE,
    "arrival_rate"
)


time_demand=ctrl.Antecedent(
    RANGE,
    "time_demand"
)



# ================= OUTPUTS =================


price=ctrl.Consequent(
    RANGE,
    "price"
)


congestion=ctrl.Consequent(
    RANGE,
    "congestion"
)


parking_time=ctrl.Consequent(
    RANGE,
    "parking_time"
)





# ================= INPUT MEMBERSHIP =================


def create_three(variable,names):


    variable[names[0]]=fuzz.trapmf(
        RANGE,[0,0,25,40]
    )


    variable[names[1]]=fuzz.trimf(
        RANGE,[30,50,70]
    )


    variable[names[2]]=fuzz.trapmf(
        RANGE,[60,80,100,100]
    )



create_three(
    occupancy,
    ["low","medium","high"]
)


create_three(
    traffic,
    ["low","medium","high"]
)


create_three(
    arrival_rate,
    ["low","medium","high"]
)


create_three(
    time_demand,
    ["offpeak","normal","rush"]
)

# create_three(
#     congestion,
#     ["low","medium","high"]
# )




# ================= PRICE =================


price["cheap"]=fuzz.trapmf(
    RANGE,[0,0,20,40]
)


price["normal"]=fuzz.trimf(
    RANGE,[30,50,70]
)


price["expensive"]=fuzz.trimf(
    RANGE,[60,80,95]
)


price["very_expensive"]=fuzz.trapmf(
    RANGE,[85,95,100,100]
)


# ================= CONGESTION =================

congestion["low"]=fuzz.trapmf(
    RANGE,[0,0,15,40]
)

congestion["medium"]=fuzz.trimf(
    RANGE,[20,50,80]
)

congestion["high"]=fuzz.trapmf(
    RANGE,[60,80,100,100]
)


# ================= PARKING TIME =================


parking_time["very_short"]=fuzz.trapmf(
    RANGE,[0,0,15,30]
)


parking_time["short"]=fuzz.trimf(
    RANGE,[20,35,50]
)


parking_time["long"]=fuzz.trimf(
    RANGE,[45,65,80]
)


parking_time["very_long"]=fuzz.trapmf(
    RANGE,[75,90,100,100]
)



# ================= RULE BASE =================

rules = [


# =====================================================
# LOW OCCUPANCY
# =====================================================


ctrl.Rule(
    occupancy["low"] &
    (traffic["low"] | arrival_rate["low"]),

    [
        price["cheap"],
        congestion["low"],
        parking_time["very_short"]
    ]
),



ctrl.Rule(
    occupancy["low"] &
    (traffic["medium"] | traffic["high"]),

    [
        price["normal"],
        congestion["medium"],
        parking_time["short"]
    ]
),




# =====================================================
# MEDIUM OCCUPANCY
# =====================================================



ctrl.Rule(
    occupancy["medium"] &
    traffic["low"] &
    time_demand["offpeak"],

    [
        price["normal"],
        congestion["low"],
        parking_time["short"]
    ]
),



ctrl.Rule(
    occupancy["medium"] &
    (
        traffic["medium"] |
        arrival_rate["medium"] |
        time_demand["normal"]
    ),

    [
        price["normal"],
        congestion["medium"],
        parking_time["short"]
    ]
),




ctrl.Rule(
    occupancy["medium"] &
    (
        traffic["high"] |
        arrival_rate["high"] |
        time_demand["rush"]
    ),

    [
        price["expensive"],
        congestion["high"],
        parking_time["long"]
    ]
),





# =====================================================
# HIGH OCCUPANCY
# =====================================================



ctrl.Rule(
    occupancy["high"] &
    traffic["low"],

    [
        price["expensive"],
        congestion["medium"],
        parking_time["long"]
    ]
),




ctrl.Rule(
    occupancy["high"] &
    (
        traffic["medium"] |
        traffic["high"] |
        arrival_rate["high"]
    ),

    [
        price["very_expensive"],
        congestion["high"],
        parking_time["very_long"]
    ]
),





# =====================================================
# ARRIVAL RATE EFFECT
# =====================================================



ctrl.Rule(
    arrival_rate["high"] &
    (
        occupancy["medium"] |
        occupancy["high"]
    ),

    [
        price["expensive"],
        congestion["high"],
        parking_time["long"]
    ]
),




ctrl.Rule(
    arrival_rate["low"] &
    occupancy["low"],

    [
        price["cheap"],
        congestion["low"],
        parking_time["very_short"]
    ]
),





# =====================================================
# DEMAND EFFECT
# =====================================================



ctrl.Rule(
    time_demand["rush"] &
    (
        occupancy["medium"] |
        occupancy["high"]
    ),

    [
        price["expensive"],
        congestion["high"],
        parking_time["long"]
    ]
),




ctrl.Rule(
    time_demand["offpeak"] &
    occupancy["low"],

    [
        price["cheap"],
        congestion["low"],
        parking_time["very_short"]
    ]
),





# =====================================================
# SAFETY COVERAGE
# =====================================================


ctrl.Rule(
    occupancy["low"] |
    traffic["low"],

    [
        price["cheap"],
        congestion["low"],
        parking_time["short"]
    ]
),




ctrl.Rule(
    occupancy["medium"],

    [
        price["normal"],
        congestion["medium"],
        parking_time["short"]
    ]
),




ctrl.Rule(
    occupancy["high"],

    [
        price["very_expensive"],
        congestion["high"],
        parking_time["long"]
    ]
)

]

system=ctrl.ControlSystem(
    rules
)




def new_simulation():

    return ctrl.ControlSystemSimulation(
        system
    )





# ================= CALCULATE =================


def calculate():


    try:


        sim=new_simulation()



        for key,e in entries.items():

            value=float(e.get())


            if value<0 or value>100:

                raise ValueError


            sim.input[key]=value




        sim.compute()



        p=sim.output["price"]

        c=sim.output["congestion"]

        t=sim.output["parking_time"]




        minutes=(t/100)*90





        result_label.config(
        text=
        f"Price: {p:.2f}\n\n"
        f"Congestion: {c:.2f}/100\n\n"
        f"Parking Time: {minutes:.0f} min"
)



        price.view(sim=sim)

        congestion.view(sim=sim)

        parking_time.view(sim=sim)

        plt.show()



    except Exception as e:


        messagebox.showerror(
            "Error",
            str(e)
        )





# ================= TESTS =================


tests=[

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


    for i,x in enumerate(tests):


        sim=new_simulation()


        sim.input["occupancy"]=x[0]
        sim.input["traffic"]=x[1]
        sim.input["arrival_rate"]=x[2]
        sim.input["time_demand"]=x[3]



        sim.compute()



        output.insert(
            tk.END,

f"""
TEST {i+1}
----------------

Occupancy : {x[0]}
Traffic   : {x[1]}
Arrival   : {x[2]}
Demand    : {x[3]}


PRICE:
{sim.output["price"]:.2f}


CONGESTION:
{sim.output["congestion"]:.2f}


PARKING TIME:
{(sim.output["parking_time"]/100)*90:.1f} minutes


"""
        )# ================= GRAPHS =================


def graphs():

    plt.close("all")


    fig,ax=plt.subplots(
        7,
        1,
        figsize=(8,20)
    )


    occupancy.view(ax=ax[0])

    traffic.view(ax=ax[1])

    arrival_rate.view(ax=ax[2])

    time_demand.view(ax=ax[3])

    price.view(ax=ax[4])

    congestion.view(ax=ax[5])

    parking_time.view(ax=ax[6])


    plt.tight_layout()

    plt.show()





# ================= GUI =================


window=tk.Tk()


window.title(
    "Smart Fuzzy Parking AI"
)


window.geometry(
    "900x700"
)


window.resizable(
    False,
    False
)



BG="#0f172a"

CARD="#1e293b"

TEXT="#e2e8f0"

ACCENT="#38bdf8"



window.configure(
    bg=BG
)


style=ttk.Style()

style.theme_use("clam")



style.configure(
    "TButton",
    font=("Segoe UI",11,"bold"),
    padding=10
)



header=tk.Frame(
    window,
    bg=BG
)

header.pack(
    pady=20
)




tk.Label(
    header,
    text="Smart Parking AI",
    bg=BG,
    fg=ACCENT,
    font=("Segoe UI",26,"bold")
).pack()



tk.Label(
    header,
    text="Fuzzy pricing + congestion prediction + parking time estimation",
    bg=BG,
    fg=TEXT,
    font=("Segoe UI",12)
).pack()







main=tk.Frame(
    window,
    bg=BG
)

main.pack(
    fill="both",
    expand=True,
    padx=30
)







left=tk.Frame(
    main,
    bg=CARD
)

left.pack(
    side="left",
    fill="y",
    padx=15
)







right=tk.Frame(
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
).pack(
    pady=15
)



def create_entry(name):


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
        text=f"{name}",
        bg=CARD,
        fg=TEXT
    ).pack(
        anchor="w"
    )



    e=tk.Entry(
        frame,
        width=22,
        justify="center"
    )


    e.pack(
        pady=5
    )


    return e




entries={


"occupancy":

create_entry(
    "Occupancy %"
),



"traffic":

create_entry(
    "Traffic %"
),



"arrival_rate":

create_entry(
    "Arrival Rate %"
),



"time_demand":

create_entry(
    "Demand %"
)

}









ttk.Button(
    left,
    text="Calculate",
    command=calculate
).pack(
    pady=20,
    padx=25,
    fill="x"
)





ttk.Button(
    left,
    text="Show Graphs",
    command=graphs
).pack(
    pady=5,
    padx=25,
    fill="x"
)






ttk.Button(
    left,
    text="Run Tests",
    command=run_tests
).pack(
    pady=5,
    padx=25,
    fill="x"
)









result_label=tk.Label(

    right,

    text=
"""
Waiting...

Enter values
and calculate
""",

    bg=CARD,

    fg=TEXT,

    font=("Segoe UI",15),

    justify="center",

    width=40,

    height=6

)



result_label.pack(
    pady=25
)








tk.Label(
    right,
    text="Testing Output",
    bg=CARD,
    fg=ACCENT,
    font=("Segoe UI",14,"bold")
).pack()







output=scrolledtext.ScrolledText(

    right,

    width=48,

    height=15,

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

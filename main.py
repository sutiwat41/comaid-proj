import tkinter as tk
from grantData import*
from random import *
#print(xlsxDf.sheet_names)

typePlate = ["Isothermal","Unheated starting length","Uniform heat flux"]
orientation = ["single plate","multiple plate"]
typeFluid = xlsxDf.sheet_names#["Compressible fluid(Ideal Gas)","Incompressible fluid"]

typePlate_text = [str(e+1)+" for "+typePlate[e] for e in range(len(typePlate))]
orientation_text = [str(e+1)+" for "+orientation[e] for e in range(len(orientation))]
typeFluid_text = [str(e+1)+" for "+typeFluid[e] for e in range(len(typeFluid))]


print("#"+"-"*5+"Welcome to Program Calculation of External flow over flat plate"+"-"*5+"#"+"\n")

while True:
    print("Program start")
    print("Please select orientation\n"+"\n".join(orientation_text) )
    orientation = int(input("Enter orientation :")) 
    #input("\nPress any key to continue . . .")
    print()
    if orientation == 1: n = 1
    elif orientation == 2: n = float(input("Enter Number of plates :"))
    else : print("Error")
    L = float(input("Enter Length of the plate [m]:"))*n


    print("Please select condition:\n"+"\n".join(typePlate_text) )
    condition = int(input("Enter condition :")) 
    print()

    print("Please select typeFluid:\n"+"\n".join(typeFluid_text) )
    UsertypeFluid = int(input("Enter typeFluid :")) 
    print()

    if typeFluid == 1: P_inf =  float(input("Enter p_inf :")) #External flow pressure

    T_inf =  float(input("Enter external flow temperature [K]:")) #external flow temperature
    U_inf =  float(input("Enter flow velocity [m/s] :")) #flow velocity
    #condition
    if condition == 1 : #isothermal
        Ts = float(input("Enter Surface Temperature [K]:"))
        Tf = (Ts+T_inf)/2 #display ref T = Tf 
    elif condition == 2:
        Ts = float(input("Enter Surface Temperature [K]:"))
        startHeatLen = float(input("Enter Start Heating Length [m/s] :"))
        Tf = (Ts+T_inf)/2
    elif condition == 3: 
        HeatFlux = float(input("Enter Heat Flux(W/m^2) :"))
        if (input("Local Surface Temperature known(y/n)? :").lower() == "y"):
            Ts = float(input("Enter Surface Temperature (default 0 ) :"))
            Tf = (Ts+T_inf)/2
        else: Tf = T_inf+uniform(-10,10) #random -10 to 10
            
    else: print("Error")


    #T_inf = float(input("Enter Temperature inf :"))

    UserFluidProp = grantPropFluid(UsertypeFluid,Tf) #return dict

    #check transition point
    xc = UserFluidProp["neu"]*5e5/U_inf
    flowtype = ""
    if 0.95<=xc/L<=1 : flowtype = "Laminar" #print("Laminar entire plate")
    elif 0.001<=xc/L<=0.95: flowtype = "mixed" #print("mixed bl")
    else: flowtype ="turbulent" #print("turbulent")

    UseValue = int(input("Enter 1-Local /2-avg :"))
    x = L #set default parameter
    if condition == 1: #isothermal
        
        if flowtype == "Laminar":
            if UseValue == 1: #Local
                x = float(input("Enter x(position from starting length)  [m]:"))
                Rex = U_inf*x/UserFluidProp["neu"]
                delta = 5*x/(Rex**0.5)
                delta_t = delta/(UserFluidProp["Pr"]**(1/3))
                if  UserFluidProp["Pr"] >= 0.6 : Nux = 0.332*(Rex**0.5)*(UserFluidProp["Pr"]**(1/3))
                else:
                    if UserFluidProp["Pr"]<=0.05 : Nux = 0.565*(Rex*UserFluidProp["Pr"])**0.5
                    else: Nux = 0.3387*(Rex**0.5)*(UserFluidProp["Pr"]**(1/3))/(1+(0.0468/UserFluidProp["Pr"])**(2/3))**0.25
                cfx = 0.664*(Rex**-0.5)
            else: 

                Rex = U_inf*L/UserFluidProp["neu"]
                Nux = 0.332*(Rex**0.5)*(UserFluidProp["Pr"]**(1/3)) 
                if  UserFluidProp["Pr"] < 0.6 :  Nux = Nux*2
                cfx =1.328*(Rex**-0.5)
        elif flowtype == "turbulent" :
            x = float(input("Enter x(position from starting length)  [m]:"))
            Rex = U_inf*x/UserFluidProp["neu"]
            delta = 0.37*x*(Rex**-0.2)
            cfx =0.0592*(Rex**-0.2)
            Nux = 0.0296*Rex*0.8*UserFluidProp["Pr"]**(1/3) 
        elif flowtype == "mixed":
            if UseValue == 1: #Local
                x = float(input("Enter x(position from starting length)  [m]:"))
                Rex = U_inf*x/UserFluidProp["neu"]
                delta = 5*x/(Rex**0.5)
                delta_t = delta/(UserFluidProp["Pr"]**(1/3))
                if  UserFluidProp["Pr"] >= 0.6 : Nux = 0.332*(Rex**0.5)*(UserFluidProp["Pr"]**(1/3))
                else:
                    if UserFluidProp["Pr"]<=0.05 : Nux = 0.565*(Rex*UserFluidProp["Pr"])**0.5
                    else: Nux = 0.3387*(Rex**0.5)*(UserFluidProp["Pr"]**(1/3))/(1+(0.0468/UserFluidProp["Pr"])**(2/3))**0.25
                cfx = 0.664*(Rex**-0.5)
            else:
                a = 871
                Rex = U_inf*x/UserFluidProp["neu"] 
                Nux = 0.037*Rex**(4/5)-a 
                cfx = 0.074*Rex**(-1/5)-2*a/Rex  
        #display h and q
        h = Nux*UserFluidProp["k"]/x
        print("h = ",h)
        print("q = ",h*(Ts-T_inf))
    elif condition == 2:#unheated
        if flowtype == "Laminar":
            if UseValue == 1:#Local
                x = float(input("Enter x(position from starting length)  [m]:"))
                Rex = U_inf*startHeatLen/UserFluidProp["neu"]
                if  UserFluidProp["Pr"] >= 0.6 : Nux = 0.332*(Rex**0.5)*(UserFluidProp["Pr"]**(1/3))
                else:
                    if UserFluidProp["Pr"]<=0.05 : Nux = 0.565*(Rex*UserFluidProp["Pr"])**0.5
                    else: Nux = 0.3387*(Rex**0.5)*(UserFluidProp["Pr"]**(1/3))/(1+(0.0468/UserFluidProp["Pr"])**(2/3))**0.25
                Nux= Nux/(1-(startHeatLen-x)**0.75)**(1/3)
            else: #???? check
                Rex = U_inf*L/UserFluidProp["neu"]
                Nux = 0.332*(Rex**0.5)*(UserFluidProp["Pr"]**(1/3)) 
                if  UserFluidProp["Pr"] < 0.6 :  Nux = Nux*2

                NuL = Nux*L/(L-startHeatLen)*(1-(startHeatLen/L)**15)**(2/3)
        elif flowtype == "turbulent":
            if UseValue == 1:
                x = float(input("Enter x(position from starting length)  [m]:"))
                Rex = U_inf*startHeatLen/UserFluidProp["neu"]
                Nux = 0.0296*Rex*0.8*UserFluidProp["Pr"]**(1/3)
                Nux= Nux/(1-(startHeatLen-x)**0.9)**(1/9)
            else:
                Rex = U_inf*L/UserFluidProp["neu"]
                Nux = 0.332*(Rex**0.5)*(UserFluidProp["Pr"]**(1/3)) 
                if  UserFluidProp["Pr"] < 0.6 :  Nux = Nux*2
                NuL = Nux*L/(L-startHeatLen)*(1-(startHeatLen/L)**90)**(8/9)
    elif condition ==3: 
        print("Local only")
        x = float(input("Enter x(position from starting length)  [m]:"))
        Rex = U_inf*x/UserFluidProp["neu"] 
        if flowtype == "Laminar":
            Nux = 0.453*(Rex**0.5)*(UserFluidProp["Pr"]**(1/3)) 
        elif flowtype == "turbulent":
            Nux = 0.0308*(Rex**0.8)*(UserFluidProp["Pr"]**(1/3)) 

        #display data
        h = Nux*UserFluidProp["k"]/x
        print("Ts(x) = ",T_inf+HeatFlux/(h*x))
        #NuL = 0.680
    if input("\nPress q/Q to exit or Press others keys to continue . . .").lower().strip() == "q":
        break

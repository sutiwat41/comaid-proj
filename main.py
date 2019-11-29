import tkinter as tk
from grantData import*
from random import *
#print(xlsxDf.sheet_names)

typePlate = ["Isothermal","Unheated starting length","Uniform heat flux"]
orientation = ["single plate","multiple plate"]
stateFluid = ["gas","liquid"]
typeFluid =dict()
typeFluid_text = dict()

stateFluid_text = [str(e+1)+" for "+stateFluid[e] for e in range(len(stateFluid))]
typePlate_text = [str(e+1)+" for "+typePlate[e] for e in range(len(typePlate))]
orientation_text = [str(e+1)+" for "+orientation[e] for e in range(len(orientation))]
#["Compressible fluid(Ideal Gas)","Incompressible fluid"]
for i in stateFluid:
    typeFluid[i] = xlsxDf[i].sheet_names
    typeFluid_text[i] = [str(e+1)+" for "+typeFluid[i][e] for e in range(len(typeFluid[i]))]


print("#"+"-"*5+"Welcome to Program Calculation of External flow over flat plate"+"-"*5+"#"+"\n")

while True:
    print("Program start")
    print("Please select orientation\n"+"\n".join(orientation_text) )
    orientation = int(input("Enter orientation :")) 
    #input("\nPress any key to continue . . .")
    print()



    print("Please select condition:\n"+"\n".join(typePlate_text) )
    condition = int(input("Enter condition :")) 
    print()

    print("Please select state of Fluid:\n"+"\n".join(stateFluid_text) )
    UserstateFluid  = int(input("Enter state of Fluid :")) 
    print()

    print("Please select type of Fluid:\n"+"\n".join(typeFluid_text[stateFluid[UserstateFluid-1]]) )
    UsertypeFluid = int(input("Enter typeFluid :")) 
    print()

    if orientation == 1: n = 1
    elif orientation == 2: n = float(eval(input("Enter Number of plates :")))
    else : print("Error")
    L = float(eval(input("Enter Length of the plate [m]:")))*n

    if UserstateFluid == 1 : P_inf =  float(input("Enter External flow pressure [Pa] :")) #External flow pressure

    T_inf =  float(eval(input("Enter external flow temperature [K]:"))) #external flow temperature
    U_inf =  float(eval(input("Enter flow velocity [m/s] :"))) #flow velocity
    #condition
    if condition == 1 : #isothermal
        Ts = float(eval(input("Enter Surface Temperature [K]:")))
        Tf = (Ts+T_inf)/2 #display ref T = Tf 
    elif condition == 2:
        Ts = float(eval(input("Enter Surface Temperature [K]:")))
        if (input("Do you want to assume film Temperature(y/n)? :").lower() == "y"):
            Tf = float(eval(input("Enter film Temperature [K]:")))
        else:
            Tf = (Ts+T_inf)/2
        print("Film Temperature =",Tf,"[K]")
        startHeatLen = float(input("Enter Start Heating Length [m] :"))
        
    elif condition == 3: 
        HeatFlux = float(eval(input("Enter Heat Flux [W/m^2] :")))
        if (input("Local Surface Temperature known(y/n)? :").lower() == "y"):
            Ts = float(eval(input("Enter Surface Temperature [K]:")))
            Tf = (Ts+T_inf)/2
        elif (input("Do you want to assume film Temperature(y/n)? :").lower() == "y"):
            Tf = float(eval(input("Enter film Temperature [K]:")))
        else: 
            Tf = T_inf+uniform(-10,10) #random -10 to 10
            print("Guess film Temperature =",Tf,"[K]")
            
    else: print("Error")

    select_fluid  =xlsxDf[stateFluid[UserstateFluid-1]].sheet_names[UsertypeFluid-1]
    if select_fluid != "other":
        UserFluidProp = grantPropFluid(stateFluid[UserstateFluid-1],UsertypeFluid,Tf) #return dict
    else:
        UserFluidProp = dict()
        x = float(eval(input("Enter kinematic viscosity [m^2/s] :")))
        UserFluidProp["neu"] = x
        x = float(eval(input("Enter k [W/mK] :")))
        UserFluidProp["k"] = x
        x = float(eval(input("Enter Pr Number:")))
        UserFluidProp["Pr"] = x    
    neu = UserFluidProp["neu"]
    if UserstateFluid == 1: 
        neu = neu*1.0133e5/P_inf
    #check transition point
    xc = neu*5e5/U_inf 
    #print(Tf,xc,U_inf*L/neu,neu)
    flowtype = ""
    if U_inf*L/neu < 5e5: 
        flowtype = "Laminar" 
        print("Laminar entire plate")
    else: 
        if 0.05*L<xc< 0.95*L:
            flowtype = "mixed" 
            print("mixed bl")

        elif 5e5<=U_inf*L/neu <=1e7: 
            flowtype ="turbulent" 
            print("turbulent")


    print("\nDo you want to add assumption?")
    print("L - Laminar flow")
    print("T - Turbulent flow\n")
    print("Press others key for No . . .")
    ass = input("Add assumption :").strip().upper()
    if ass == "L" :flowtype = "Laminar" 
    elif ass == "T": flowtype = "turbulent" 
    print("So flowtype is",flowtype)


    UseValue = int(input("\nEnter 1-Local /2-avg :"))
    x = L #set default parameter
    if condition == 1: #isothermal
        
        if flowtype == "Laminar":
            if UseValue == 1: #Local
                x = float(eval(input("Enter x(position from starting length)  [m]:")))
                Rex = U_inf*x/neu
                delta = 5*x/(Rex**0.5)
                delta_t = delta/(UserFluidProp["Pr"]**(1/3))
                if  UserFluidProp["Pr"] >= 0.6 : Nux = 0.332*(Rex**0.5)*(UserFluidProp["Pr"]**(1/3))
                else:
                    if UserFluidProp["Pr"]<=0.05 : Nux = 0.565*(Rex*UserFluidProp["Pr"])**0.5
                    else: Nux = 0.3387*(Rex**0.5)*(UserFluidProp["Pr"]**(1/3))/(1+(0.0468/UserFluidProp["Pr"])**(2/3))**0.25
                cfx = 0.664*(Rex**-0.5)
            else: 

                Rex = U_inf*L/neu
                #print(Rex,neu)
                Nux = 0.664*(Rex**0.5)*(UserFluidProp["Pr"]**(1/3)) 
                if  UserFluidProp["Pr"] < 0.6 :  Nux = Nux*2
                cfx =1.328*(Rex**-0.5)
        elif flowtype == "turbulent" :
            x = float(eval(input("Enter x(position from starting length)  [m]:")))
            Rex = U_inf*x/neu
            delta = 0.37*x*(Rex**-0.2)
            cfx =0.0592*(Rex**-0.2)
            Nux = 0.0296*Rex*0.8*UserFluidProp["Pr"]**(1/3) 
        elif flowtype == "mixed":
            if UseValue == 1: #Local
                x = float(input("Enter x(position from starting length)  [m]:"))
                Rex = U_inf*x/neu
                delta = 5*x/(Rex**0.5)
                delta_t = delta/(UserFluidProp["Pr"]**(1/3))
                if  UserFluidProp["Pr"] >= 0.6 : Nux = 0.332*(Rex**0.5)*(UserFluidProp["Pr"]**(1/3))
                else:
                    if UserFluidProp["Pr"]<=0.05 : Nux = 0.565*(Rex*UserFluidProp["Pr"])**0.5
                    else: Nux = 0.3387*(Rex**0.5)*(UserFluidProp["Pr"]**(1/3))/(1+(0.0468/UserFluidProp["Pr"])**(2/3))**0.25
                cfx = 0.664*(Rex**-0.5)
            else:
                a = 871
                Rex = U_inf*x/neu 
                Nux = 0.037*Rex**(4/5)-a 
                cfx = 0.074*Rex**(-1/5)-2*a/Rex  
        #display h and q
        #print(UserFluidProp["k"],x,Nux,Rex)
        print("Nu = ",round(Nux,4))
        h = Nux*UserFluidProp["k"]/x
        print("h = ",round(h,4),"[W/m^2 K]")
        print("q = ",round(h*(Ts-T_inf),4),"[W/m^2]")
    elif condition == 2:#unheated
        if flowtype == "Laminar":
            if UseValue == 1:#Local
                x = float(eval(input("Enter position from starting length (x)  [m]:")))
                Rex = U_inf*x/neu
                if  UserFluidProp["Pr"] >= 0.6 : Nux = 0.332*(Rex**0.5)*(UserFluidProp["Pr"]**(1/3))
                else:
                    if UserFluidProp["Pr"]<=0.05 : Nux = 0.565*(Rex*UserFluidProp["Pr"])**0.5
                    else: Nux = 0.3387*(Rex**0.5)*(UserFluidProp["Pr"]**(1/3))/(1+(0.0468/UserFluidProp["Pr"])**(2/3))**0.25
                Nux= Nux/(1-(startHeatLen/x)**0.75)**(1/3)

                h = Nux*UserFluidProp["k"]/x
                
                print("Nu =",Nux,"When x = %.4f m"%(x))
                print("h = ",round(h,4),"[W/m^2.K]")
            else: #???? check
                Rex = U_inf*L/neu
                Nux = 0.332*(Rex**0.5)*(UserFluidProp["Pr"]**(1/3)) 
                if  UserFluidProp["Pr"] < 0.6 :  Nux = Nux*2
                NuL = Nux*L/(L-startHeatLen)*(1-(startHeatLen/L)**12)**(2/3)
                h = NuL*UserFluidProp["k"]/L

                print("Nu =",round(NuL,4))
                print("h = ",round(h,4),"[W/m^2.K]")
            print("Rex = ",round(Rex,4))
            
        elif flowtype == "turbulent":
            if UseValue == 1:
                x = float(eval(input("Enter position from starting length (x)  [m]:")))
                Rex = U_inf*startHeatLen/neu
                Nux = 0.0296*Rex*0.8*UserFluidProp["Pr"]**(1/3)
                Nux= Nux/(1-(startHeatLen/x)**0.9)**(1/9)
            else:
                Rex = U_inf*L/neu
                Nux = 0.332*(Rex**0.5)*(UserFluidProp["Pr"]**(1/3)) 
                if  UserFluidProp["Pr"] < 0.6 :  Nux = Nux*2
                NuL = Nux*L/(L-startHeatLen)*(1-(startHeatLen/L)**90)**(8/9)
    elif condition ==3: 
        print("Local only")
        x = float(eval(input("Enter x(position from starting length)  [m]:")))
        Rex = U_inf*x/neu 
        if flowtype == "Laminar":
            Nux = 0.453*(Rex**0.5)*(UserFluidProp["Pr"]**(1/3)) 
        elif flowtype == "turbulent":
            Nux = 0.0308*(Rex**0.8)*(UserFluidProp["Pr"]**(1/3)) 

        #display data
        h = Nux*UserFluidProp["k"]/x
        print("Re =",round(Rex,4))
        print("h = ",round(h,4),"[W/m^2.K]")
        print("Ts(x) =",round(T_inf+HeatFlux/(h*x),4),"[K] When x = ",round(x,4),"[m]")
        NuL =0.68*(Rex**0.5)*(UserFluidProp["Pr"]**(1/3))
        print("NuL =",round(NuL,4))
        print("Surface Temperature average = ",round(T_inf+HeatFlux*L/(NuL*UserFluidProp["k"]),4),"[K]")
        #NuL = 0.680
    if input("\nPress q/Q to exit or Press others keys to continue . . .\n").lower().strip() == "q":
        break


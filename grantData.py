#grant data from excel
import pandas as pd

xlsxDf = {"liquid" : pd.ExcelFile('table liquid.xlsx'), "gas": pd.ExcelFile('table gas.xlsx')}


def LinearInterpolate(P1,P2,coor,val): #return type float / str "Error"
    #p1 p2 -> known variable (tuple)
    #coor  -> known value variable | val -> known value
    #return unknowns from linear interplolation 
    slope = (P2[1]-P1[1])/(P2[0]-P1[0])
    if coor == 1:  tmp = slope*(val-P1[0])+P1[1]
    elif coor == 2 :  tmp = (val-P1[1])/slope+P1[0]
    else: tmp ="Error"
    return tmp

def linearSearch(datfm,val):
    index = 0
    type_s = ""
    for i in datfm:
        if float(i) == val : 
            type_s = "found"
            break
        elif float(i) > val:
            type_s = "none" 
            break
        index+=1
    return (type_s,index)

def f(x): #temp function
    return x+5

def binarySearchVal(left,right,err): #bisection method
    
    while True:
        mid = (left+right)/2
        if f(right)*f(mid) > 0: right = mid
        elif f(left)*f(mid) < 0 : left = mid
        newMid = (left+right)/2 
        if abs((newMid-mid)/newMid)*100 < err: break
    return newMid 

def grantPropFluid(f_state,f_type,T_f): #fluid type / Temp fluid
    #print(xlsxDf[f_state].sheet_names[f_type-1])
    select_fluid =xlsxDf[f_state].sheet_names[f_type-1]

    table = pd.read_excel(xlsxDf[f_state], sheet_name=select_fluid)
    table_head = list(table.columns)
    prop = dict()
    prop["Tf"] = T_f 
    head = {4:"neu",5:"k",7:"Pr"}# neu k pr
    result = linearSearch(table[table_head[0]][2:],T_f) #0 -> found/not found #1 index
    if result[0] == "none":
        Index = 0
        if result[1] == 0: Index = 2
        else : Index =result[1]+1 #
        for i in [4,5,7]:
            e =  table_head[i]
            p1 = (table.at[Index,table_head[0]],table.at[Index,e])
            p2 = (table.at[Index+1,table_head[0]],table.at[Index+1,e])
            #print(p1,p2)
            prop[head[i]] = LinearInterpolate(p1,p2,1,T_f)/table.at[1,e]
    else:
        for i in [4,5,7]: 
            prop[head[i]] = table.at[result[1]+2,table_head[i]]/table.at[1,table_head[i]]
    return prop








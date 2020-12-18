import os
import ast

F16Mapping = {'''
"ICP 1": "ICP Priority Function Button - 1(T-ILS)",
"ICP 2": "ICP Priority Function Button - 2/N(ALOW)",
"ICP 3": "ICP Priority Function Button - 3",
"ICP 4": "ICP Priority Function Button - 4/W(STPT)",
"ICP 5": "ICP Priority Function Button - 5(CRUS)",
"ICP 6": "ICP Priority Function Button - 6/E(TIME)",
"ICP 7": "ICP Priority Function Button - 7(MARK)",
"ICP 8": "ICP Priority Function Button - 8/S(FIX)",
"ICP 9": "ICP Priority Function Button - 9(A-CAL)",
"ICP 0": "ICP Priority Function Button - 0(M-SEL)",

"ICP ENTR": "ICP Enter Button - ENTR",
"ICP RCL": "ICP Recall Button - RCL",
"ICP LEFT": "ICP Data Control Switch - RET",
"ICP RIGHT": "ICP Data Control Switch - SEQ",
"ICP UP": "ICP Data Control Switch - UP",
"ICP DOWN": "ICP Data Control Switch - DOWN",
'''
"MFD LEFT 1": "Left MFD OSB 1",
"MFD LEFT 2": "Left MFD OSB 2", 
"MFD LEFT 3": "Left MFD OSB 3", 
"MFD LEFT 4": "Left MFD OSB 4", 
"MFD LEFT 5": "Left MFD OSB 5", 
"MFD LEFT 6": "Left MFD OSB 6", 
"MFD LEFT 7": "Left MFD OSB 7", 
"MFD LEFT 8": "Left MFD OSB 8", 
"MFD LEFT 9": "Left MFD OSB 9",  
"MFD LEFT 10": "Left MFD OSB 10",  

"MFD LEFT 11": "Left MFD OSB 11",
"MFD LEFT 12": "Left MFD OSB 12", 
"MFD LEFT 13": "Left MFD OSB 13", 
"MFD LEFT 14": "Left MFD OSB 14", 
"MFD LEFT 15": "Left MFD OSB 15", 
"MFD LEFT 16": "Left MFD OSB 16", 
"MFD LEFT 17": "Left MFD OSB 17", 
"MFD LEFT 18": "Left MFD OSB 18", 
"MFD LEFT 19": "Left MFD OSB 19",
"MFD LEFT 20": "Left MFD OSB 20", 

"MFD RIGHT 1": "Right MFD OSB 1",
"MFD RIGHT 2": "Right MFD OSB 2", 
"MFD RIGHT 3": "Right MFD OSB 3", 
"MFD RIGHT 4": "Right MFD OSB 4", 
"MFD RIGHT 5": "Right MFD OSB 5", 
"MFD RIGHT 6": "Right MFD OSB 6", 
"MFD RIGHT 7": "Right MFD OSB 7", 
"MFD RIGHT 8": "Right MFD OSB 8", 
"MFD RIGHT 9": "Right MFD OSB 9",  
"MFD RIGHT 10": "Right MFD OSB 10",  

"MFD RIGHT 11": "Right MFD OSB 11",
"MFD RIGHT 12": "Right MFD OSB 12", 
"MFD RIGHT 13": "Right MFD OSB 13", 
"MFD RIGHT 14": "Right MFD OSB 14", 
"MFD RIGHT 15": "Right MFD OSB 15", 
"MFD RIGHT 16": "Right MFD OSB 16", 
"MFD RIGHT 17": "Right MFD OSB 17", 
"MFD RIGHT 18": "Right MFD OSB 18", 
"MFD RIGHT 19": "Right MFD OSB 19",
"MFD RIGHT 20": "Right MFD OSB 20"
}

F18Mapping = {
"MFD LEFT 1": "Left MDI PB 1",
"MFD LEFT 2": "Left MDI PB 2", 
"MFD LEFT 3": "Left MDI PB 3", 
"MFD LEFT 4": "Left MDI PB 4", 
"MFD LEFT 5": "Left MDI PB 5", 
"MFD LEFT 6": "Left MDI PB 6", 
"MFD LEFT 7": "Left MDI PB 7", 
"MFD LEFT 8": "Left MDI PB 8", 
"MFD LEFT 9": "Left MDI PB 9",  
"MFD LEFT 10": "Left MDI PB 10",  

"MFD LEFT 11": "Left MDI PB 11",
"MFD LEFT 12": "Left MDI PB 12", 
"MFD LEFT 13": "Left MDI PB 13", 
"MFD LEFT 14": "Left MDI PB 14", 
"MFD LEFT 15": "Left MDI PB 15", 
"MFD LEFT 16": "Left MDI PB 16", 
"MFD LEFT 17": "Left MDI PB 17", 
"MFD LEFT 18": "Left MDI PB 18", 
"MFD LEFT 19": "Left MDI PB 19",
"MFD LEFT 20": "Left MDI PB 20", 

"MFD RIGHT 1": "Right MDI PB 1",
"MFD RIGHT 2": "Right MDI PB 2", 
"MFD RIGHT 3": "Right MDI PB 3", 
"MFD RIGHT 4": "Right MDI PB 4", 
"MFD RIGHT 5": "Right MDI PB 5", 
"MFD RIGHT 6": "Right MDI PB 6", 
"MFD RIGHT 7": "Right MDI PB 7", 
"MFD RIGHT 8": "Right MDI PB 8", 
"MFD RIGHT 9": "Right MDI PB 9",  
"MFD RIGHT 10": "Right MDI PB 10",  

"MFD RIGHT 11": "Right MDI PB 11",
"MFD RIGHT 12": "Right MDI PB 12", 
"MFD RIGHT 13": "Right MDI PB 13", 
"MFD RIGHT 14": "Right MDI PB 14", 
"MFD RIGHT 15": "Right MDI PB 15", 
"MFD RIGHT 16": "Right MDI PB 16", 
"MFD RIGHT 17": "Right MDI PB 17", 
"MFD RIGHT 18": "Right MDI PB 18", 
"MFD RIGHT 19": "Right MDI PB 19",
"MFD RIGHT 20": "Right MDI PB 20",

"MFD DOWN 1": "AMPCD PB 1",
"MFD DOWN 2": "AMPCD PB 2", 
"MFD DOWN 3": "AMPCD PB 3", 
"MFD DOWN 4": "AMPCD PB 4", 
"MFD DOWN 5": "AMPCD PB 5", 
"MFD DOWN 6": "AMPCD PB 6", 
"MFD DOWN 7": "AMPCD PB 7", 
"MFD DOWN 8": "AMPCD PB 8", 
"MFD DOWN 9": "AMPCD PB 9",  
"MFD DOWN 10": "AMPCD PB 10",  

"MFD DOWN 11": "AMPCD PB 11",
"MFD DOWN 12": "AMPCD PB 12", 
"MFD DOWN 13": "AMPCD PB 13", 
"MFD DOWN 14": "AMPCD PB 14", 
"MFD DOWN 15": "AMPCD PB 15", 
"MFD DOWN 16": "AMPCD PB 16", 
"MFD DOWN 17": "AMPCD PB 17", 
"MFD DOWN 18": "AMPCD PB 18", 
"MFD DOWN 19": "AMPCD PB 19",
"MFD DOWN 20": "AMPCD PB 20"

}

nl = "\n"

def luaGenerator(setting, model):

    keySeparator = '$and$'

    if setting[0] == "[" and setting[-1] == "]":
        setting = "{" + setting[1:-1] + "}"
    else:
        raise ValueError("The setting file has formating error.")
    
    if model == "F16":
        mapdict = F16Mapping
    elif model == "F18":
        mapdict = F18Mapping

    settingDict = ast.literal_eval(setting)
    luafile = """local diff = {\n ["keyDiffs"] = {\n"""

    for key, value in settingDict.items():

        try:
            tempKey = mapdict[key]
        except:
            continue

        if keySeparator in value:
            keyCombine = value.split(keySeparator)
            keyprimary = keyCombine[1]
            keysecondary = keyCombine[0]
            temp = """  ["d3006pnilu3006cd17vd1vpnilvu0"] = {\n   ["added"] = {\n    [1] = {\n     ["key"] = """ + f""" "{keyprimary}" """ + """,\n     ["reformers"] = {\n      [1] =""" + f""" "{keysecondary}" """+ """,\n     },\n    },\n   },\n   ["name"] =""" + f""" "{tempKey}" """ + """,\n  },\n"""
        else:
            keyprimary = value
            temp = """  ["d3006pnilu3006cd17vd1vpnilvu0"] = {\n   ["added"] = {\n    [1] = {\n     ["key"] = """ + f""" "{keyprimary}" """ + """,\n    },\n   },\n   ["name"] =""" + f""" "{tempKey}" """ + """,\n  },\n"""
        
        luafile = luafile + temp

    luafile = luafile + " },\n}\nreturn diff"

    path = os.getcwd()
    print (path)
    f = open(path + f"/{model}.diff.lua", "w")
    f.write(luafile)
    f.close()




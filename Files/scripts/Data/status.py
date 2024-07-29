Status = ["BRN","PAR","SLE","POI","DRG"]

SkipTurn = {"DRG":{"Text":" è sotto effetto di funghi allucinogeni","chance":40},"PAR":{"Text":" è troppo elettrizato per attacare","chance":33},"SLE":{"Text":" è addormentato, BRUTTO PIGRONE","chance":100}}

Damage = {"BRN":{"Text":" è scottato","%":4},"POI":{"Text":" è avvelenato","%":8},"DRG":{"Text":", gli fa male la pancia","%":2}}

LowerStat = {"BRN":{"ATT":0.5},"PAR":{"VEL":0.4}}

CureChance = {"BRN":10,"PAR":5,"SLE":35,"POI":10,"DRG":5}

Color = {"BRN":(255,100,0),
         "PAR":(255,255,0),
         "SLE":(150,150,150),
         "POI":(200,0,200),
         "DRG":(50,0,50)}

ImuneTypes = {"DRG":["veleno"], "PAR":["terra"]}

ResistanceTypes = {"PAR":{"elettro":15},
                   "BRN":{"fuoco":15,"ghiaccio":5},
                   "POI":{"veleno":15,"cibo":5},
                   "SLE":{"erba":5,"gamer":15,"AI":10},
                   "DRG":{"AI":10,"cibo":5}}
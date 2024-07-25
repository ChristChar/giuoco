Status = ["BRN","PAR","SLE","POI"]

SkipTurn = {"PAR":{"Text":" è troppo elettrizato per attacare","chance":33},"SLE":{"Text":" è addormentato, BRUTTO PIGRONE","chance":100}}

Damage = {"BRN":{"Text":" è scottato","%":4},"POI":{"Text":" è avvelenato","%":8}}

LowerStat = {"BRN":{"ATT":0.5},"PAR":{"VEL":0.4}}

CureChance = {"BRN":10,"PAR":5,"SLE":35,"POI":10}

Color = {"BRN":(255,100,0),
         "PAR":(255,255,0),
         "SLE":(150,150,150),
         "POI":(200,0,200)}
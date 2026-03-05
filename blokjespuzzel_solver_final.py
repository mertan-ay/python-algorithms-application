
# # Opdracht 5: Blokjespuzzel

# << Mertan Aydogan>>



def probeer_zet(vanaf):
    for stuk in range(8):
        if vrij[stuk]:
            for stand in range(standen[stuk]):
                if past(stuk,stand,vanaf):
                    plaats(stuk,stand,vanaf)
 # Search for the next free space VV
                    vv = vanaf
                    while vakje[vv] != -1:
                        vv += 1
                    if vv != 81: 
                        probeer_zet(vv)
                    else:
                        oplossing()
                    neem_weg(stuk,stand,vanaf)


vakje = [-1] * 82




vrij = [True] * 8




# Make a border out of filled spaces
for i in range(9):
    vakje[i*9+8] = 99
for i in range(72,81):
    vakje[i] = 99



# Zwart heeft maar 1 stand om spiegelingen te voorkomen
standen = [4,2,8,4,4,1,4,4]

#.........Rood,Paars,Geel,Groen,Roze,Zwart,Blauw,Licht-Groen

viertal = [
    [ #Rood
        [1,9,10,19,20,28,29],
        [1,9,10,17,18,26,27],
        [1,9,10,11,12,20,21],
        [1,7,8,9,10,16,17]
        
    ],
    [ #Paars
        [1,2,3,9,10,11,12],
        [1,9,10,18,19,27,28]
        
    ],
    [ #Geel
        [1,9,10,18,19,17,16],
        [1,9,10,18,19,20,21],
        [1,2,3,11,12,20,21],
        [1,2,3,9,10,18,19],
        [1,2,9,10,11,18,27],
        [9,18,27,19,20,28,29],
        [1,2,9,10,11,20,29],
        [9,18,27,16,17,25,26]
        
    ],
    [ #Groen
        [9,18,19,20,21,12,3],
        [9,18,1,2,3,12,21],
        [1,2,11,20,29,28,27],
        [1,2,9,18,27,28,29]
        
    ],
    [ #Roze
        [1,2,9,10,11,19,28],
        [1,9,10,18,19,11,12],
        [1,9,10,18,19,7,8],
        [9,17,18,19,26,27,28]
    ],
    [ #Zwart
        [9,18,27,36,17,26,35]
        
    ],
    [ #Blauw
        [1,2,9,10,11,18,19],
        [1,2,9,10,11,19,20],
        [1,9,10,8,19,11,20],
        [1,9,10,18,19,8,17]
        
    ],
    [ #Licht-Groen
        [1,9,10,17,18,19,20],
        [1,2,3,10,11,19,20],
        [9,18,27,7,8,16,17],
        [9,18,27,10,11,19,20]
    ]
]



def past(stuk, stand, vanaf):
    result = True
    k = 0
    while result and (k < 7):
        index = vanaf + viertal[stuk][stand][k]
        if 0 <= index < len(vakje):  # Check if the index is inside de boundrey
            result = vakje[index] == -1
        else:
            result = False  
        k += 1
    return result


# Plaats a piece
def plaats(stuk, stand, vanaf):  
    vakje[vanaf] = stuk
    for k in range(7):
        vakje[vanaf + viertal[stuk][stand][k]] = stuk
    vrij[stuk] = False



# Take a way a piece
def neem_weg(stuk, stand, vanaf):
    vakje[vanaf] = -1
    for k in range(7):
        vakje[vanaf + viertal[stuk][stand][k]] = -1
    vrij[stuk] = True


naam = ["1", "2", "3", "4", "5", "6", "7","8"]
#-------"RO", "PA", "GE", "GR", "RZ", "ZW", "BL", "LG"
opl = 0
def oplossing():
    global opl
    opl += 1
    for r in range(8):
        rij = ""
        for k in range(8):
            rij += naam[vakje[r*9+k]]
        print(rij)
    print("Oplossing nummer:", opl)
    
    



probeer_zet(0)





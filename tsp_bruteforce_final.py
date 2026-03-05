
# # Opdracht 3: Handelsreizigersprobleem

# << Mertan Aydogan>>


import random 
import time





afstand = [[]] 



#Fill the matrix with random numbers <= to m
def vul_afstand(n, m):
    global afstand
    afstand = []
    for i in range(0, n + 1):
        rij = []
        for j in range(0, n + 1):
            if i == j:
                rij.append(0) # diagonal: distance from point to itself
            elif i < j:
                rij.append(random.randint(1,m)) # random number from 1..m
            else:
                rij.append(afstand[j][i]) 
        afstand.append(rij)
    

#show matrix 
def toon_matrix(afstand):
    n = len(afstand)
    for i in range(0,n):
        print(afstand[i])




def eerste_perm(n):
    global start
    start = [i for i in range(1, n+1)]
    return start




def volgende_perm(perm):
    n = len(perm) 
    result = False 

    # Search from the right for the first element with a larger right neighbour
    i = n - 1
    while (i > 0) and (perm[i-1] >= perm[i]):
        i -= 1
    
    if i > 0: # value found
        result = True # There is a next permutation
        
        # Search from the right for the first value greater than the found value
        waarde = perm[i-1] # value is the previously found perm[i-1]
        j = n - 1 # search from the right
        while perm[j] <= waarde:
            j -= 1
        
        # Swap these two values
        perm[i-1] = perm[j]
        perm[j] = waarde
        
        # Fix the tail
        j = n - 1;
        while i < j:
            waarde = perm[i] # swap Perm[i] and Perm[j]
            perm[i] = perm[j]
            perm[j] = waarde
            
            i += 1
            j -= 1 

    return result


def rondrit_lengte(perm):
    # Calculate the round trip length of the permutation
    lengte = 0
    vorige = 0
    for i in perm:
        w = afstand[vorige][i]
        lengte += w
        vorige = i
    lengte += afstand[vorige][0]  # Return to the starting point
    return lengte  # Make sure the length is returned



def toon_rit(perm, a):
    print("Rit: 0 - " + " - ".join(map(str, start)) + " - 0")
    print("Lengte:", a)
    # Show round trip and length





def zoek_beste(n):
    # Search for the shortest round trip over all permutations
    kortste_lengte = float('inf')

    # Start with the first permutation
    perm = eerste_perm(n)

    # Continue searching until there is no next permutation
    while True:
        # Calculate the length of the current round trip
        lengte = rondrit_lengte(perm)
        
        # Show the round trip and the length
        toon_rit(perm, lengte)
        
        # Check if this is the shortest round trip
        if lengte < kortste_lengte:
            kortste_lengte = lengte
            beste_perm = perm[:]  # Make a copy of the permutation
        
        # Find the next permutation
        if volgende_perm(perm) == False:
            break

    # Show the best round trip after the search
    print("\nKortste rondrit gevonden:")
   
    toon_rit(beste_perm, kortste_lengte)





n = int(input("Geef het aantal steden: "))
max_afstand = int(input("Geef de maximum afstand: "))



tijden = []  # List to store the computation times

# Run the measurement 10 times
for i in range(10):
    vul_afstand(n, max_afstand)
    toon_matrix(afstand)
    start1 = time.time()  # Start stopwatch
    zoek_beste(n)
    stop = time.time()  # Stop stopwatch
    verstreken_tijd = round(stop - start1, 5)  # Round time to 5 decimals
    tijden.append(verstreken_tijd)  # Add the time to the list
    kommagetal1 = str(verstreken_tijd).replace('.', ',')
    print(f"Meting {i+1}: Verstreken tijd in seconden: {kommagetal1}")

# Calculate the average time
gemiddelde_tijd = round(sum(tijden) / len(tijden), 5)
kommagetal = str(gemiddelde_tijd).replace('.', ',')
# Print the average computation time
print("\nGemiddelde rekentijd over 10 metingen in seconden:", kommagetal)

input("Press Enter to close")



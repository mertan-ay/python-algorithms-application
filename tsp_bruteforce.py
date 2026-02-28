from __future__ import annotations

import random
from dataclasses import dataclass
from time import perf_counter
from typing import List, Optional, Sequence, Tuple

Matrix = List[List[int]]
Perm = List[int]


def vul_afstand(n: int, m: int, rng: Optional[random.Random] = None) -> Matrix:
    """
    Maak een symmetrische afstandsmatrix voor steden 0..n (dus totaal n+1 steden).

    Args:
        n: aantal steden exclusief startstad 0 (n >= 1)
        m: maximale afstand (m >= 1)
        rng: optionele random generator (voor reproduceerbaarheid)

    Returns:
        (n+1)x(n+1) matrix met 0 op de diagonaal en symmetrische afstanden.
    """
    if n < 1:
        raise ValueError("n moet >= 1 zijn")
    if m < 1:
        raise ValueError("m moet >= 1 zijn")

    rng = rng or random.Random()

    afstand: Matrix = []
    for i in range(0, n + 1):
        rij: List[int] = []
        for j in range(0, n + 1):
            if i == j:
                rij.append(0)
            elif i < j:
                rij.append(rng.randint(1, m))
            else:
                rij.append(afstand[j][i])  # symmetrisch
        afstand.append(rij)
    return afstand


def toon_matrix(afstand: Sequence[Sequence[int]]) -> None:
    """Print de afstandsmatrix (handig voor debuggen bij kleine n)."""
    for rij in afstand:
        print(list(rij))


def eerste_perm(n: int) -> Perm:
    """Eerste permutatie: [1, 2, ..., n]."""
    return [i for i in range(1, n + 1)]


def volgende_perm(perm: Perm) -> bool:
    """
    Bepaal de volgende lexicografische permutatie in-place.

    Returns:
        True als er een volgende permutatie is, anders False (perm is dan de laatste).
    """
    n = len(perm)

    # Zoek vanaf rechts eerste element met grotere rechterbuurman
    i = n - 1
    while (i > 0) and (perm[i - 1] >= perm[i]):
        i -= 1

    if i <= 0:
        return False  # laatste permutatie bereikt

    # Zoek vanaf rechts de eerste waarde groter dan perm[i-1]
    waarde = perm[i - 1]
    j = n - 1
    while perm[j] <= waarde:
        j -= 1

    # Verwissel
    perm[i - 1], perm[j] = perm[j], perm[i - 1]

    # Keer de staart om (i..einde)
    j = n - 1
    while i < j:
        perm[i], perm[j] = perm[j], perm[i]
        i += 1
        j -= 1

    return True


def rondrit_lengte(perm: Sequence[int], afstand: Sequence[Sequence[int]]) -> int:
    """
    Bereken rondritlengte: 0 -> perm[0] -> ... -> perm[-1] -> 0
    """
    lengte = 0
    vorige = 0
    for stad in perm:
        lengte += afstand[vorige][stad]
        vorige = stad
    lengte += afstand[vorige][0]
    return lengte


def format_rit(perm: Sequence[int]) -> str:
    return "0 - " + " - ".join(map(str, perm)) + " - 0"


@dataclass(frozen=True)
class BesteRit:
    perm: Tuple[int, ...]
    lengte: int
    bekeken: int  # aantal geëvalueerde permutaties


def zoek_beste(
    n: int,
    afstand: Sequence[Sequence[int]],
    verbose: bool = False,
) -> BesteRit:
    """
    Brute force: zoek de kortste rondrit over alle permutaties van 1..n.

    Args:
        n: aantal steden exclusief startstad 0
        afstand: afstandsmatrix voor steden 0..n
        verbose: True om elke rit te printen (alleen voor kleine n!)

    Returns:
        BesteRit met beste perm, lengte en aantal bekeken permutaties.
    """
    perm = eerste_perm(n)
    beste_perm = perm.copy()
    kortste = rondrit_lengte(perm, afstand)
    bekeken = 0

    while True:
        bekeken += 1
        lengte = rondrit_lengte(perm, afstand)

        if verbose:
            print("Rit:", format_rit(perm))
            print("Lengte:", lengte)

        if lengte < kortste:
            kortste = lengte
            beste_perm = perm.copy()

        if not volgende_perm(perm):
            break

    return BesteRit(perm=tuple(beste_perm), lengte=kortste, bekeken=bekeken)


def benchmark(
    n: int,
    max_afstand: int,
    runs: int = 10,
    verbose_matrix: bool = False,
) -> float:
    """
    Doe 'runs' metingen op verschillende random afstandsmatrices en geef gemiddelde tijd terug.
    Print geen routes tijdens timing (belangrijk voor eerlijke meting).
    """
    tijden: List[float] = []
    rng = random.Random()  # eigen RNG (optioneel seedbaar)

    for _ in range(runs):
        afstand = vul_afstand(n, max_afstand, rng=rng)

        if verbose_matrix:
            toon_matrix(afstand)

        t0 = perf_counter()
        _ = zoek_beste(n, afstand, verbose=False)
        t1 = perf_counter()
        tijden.append(t1 - t0)

    return sum(tijden) / len(tijden)


def main() -> None:
    n = int(input("Geef het aantal steden (excl. startstad 0): "))
    max_afstand = int(input("Geef de maximum afstand: "))

    if n > 10:
        print("Waarschuwing: brute-force TSP groeit factorial; n > 10 kan erg langzaam worden.")

    # 1) Eén voorbeeld-run met output (handig bij kleine n)
    afstand = vul_afstand(n, max_afstand)
    beste = zoek_beste(n, afstand, verbose=(n <= 7))  # bij grotere n liever niet spammen
    print("\nKortste rondrit gevonden:")
    print("Rit:", format_rit(beste.perm))
    print("Lengte:", beste.lengte)
    print("Permutaties bekeken:", beste.bekeken)

    # 2) Benchmark (10 runs) zonder output tijdens meten
    avg = benchmark(n, max_afstand, runs=10, verbose_matrix=False)
    print(f"\nGemiddelde rekentijd over 10 metingen: {avg:.6f} seconden")


if __name__ == "__main__":
    main()
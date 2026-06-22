"""Schnitt zweier Ebenen in Parameterform - exakt (Brueche), Ausgabe als Schnittgerade.

E1: x = P + s*a + t*b
E2: x = Q + u*c + v*d

Gleichsetzen  ->  s*a + t*b - u*c - v*d = Q - P   (3 Gleichungen, 4 Unbekannte s,t,u,v)
Loesen mit Fraction (also nur exakte ganze/rationale Zahlen, kein Rundungsfehler),
Ergebnis wieder in E2 einsetzen -> Schnittgerade.
"""

from fractions import Fraction as F


def vec(prompt):
    return [F(x) for x in input(prompt).replace(",", " ").split()]


def rref(M):
    """Reduzierte Zeilenstufenform (in-place-frei). M: Liste von Zeilen (Fraction)."""
    M = [row[:] for row in M]
    rows, cols = len(M), len(M[0])
    pivots = []
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = M[r][c]
        M[r] = [x / inv for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        pivots.append(c)
        r += 1
        if r == rows:
            break
    return M, pivots


def fmt(x):
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def fmt_vec(v):
    return "(" + ", ".join(fmt(x) for x in v) + ")"


def solve(P, a, b, Q, c, d):
    # Unbekannte: s,t,u,v  ->  Spalten a, b, -c, -d ; rechte Seite Q-P
    A = [[a[i], b[i], -c[i], -d[i], Q[i] - P[i]] for i in range(3)]
    R, pivots = rref(A)
    ncols = 4  # s,t,u,v

    # Inkonsistent? (Pivot in der rechten Seite, Spalte 4)
    if 4 in pivots:
        # Richtungen vergleichen: parallel oder windschief gibt es bei Ebenen nicht,
        # also entweder parallel-verschieden (keine Loesung) ...
        return "Kein Schnittpunkt: Die Ebenen sind (echt) parallel.\n"

    free = [c for c in range(ncols) if c not in pivots]

    # Loesung jeder Unbekannten als: konst + sum(coeff * freevar)
    # const-Teil und je freie Variable ein Koeffizientenvektor
    const = [F(0)] * ncols
    fcoef = {fv: [F(0)] * ncols for fv in free}
    for fv in free:
        fcoef[fv][fv] = F(1)
    for row_i, pc in enumerate(pivots):
        # Pivotvariable = rhs - sum(R[row][freevar] * freevar)
        const[pc] = R[row_i][4]
        for fv in free:
            fcoef[fv][pc] = -R[row_i][fv]

    # x = P + s*a + t*b  (s=Unbekannte 0, t=1)
    def x_of(svals):
        return [P[i] + svals[0] * a[i] + svals[1] * b[i] for i in range(3)]

    if not free:
        pt = x_of(const)
        return f"Genau ein gemeinsamer Punkt: {fmt_vec(pt)}\n"

    if len(free) == 1:
        fv = free[0]
        stuetz = x_of(const)                         # freie Var = 0
        svals1 = [const[i] + fcoef[fv][i] for i in range(4)]   # freie Var = 1
        richtung = [x_of(svals1)[i] - stuetz[i] for i in range(3)]
        # Richtung auf ganzzahlig / gekuerzt bringen
        richtung = clean_dir(richtung)
        name = "r"
        return (f"Schnittgerade:\n"
                f"  g: x = {fmt_vec(stuetz)} + {name} * {fmt_vec(richtung)}\n")

    return "Die Ebenen sind identisch (unendlich viele Punkte, ganze Ebene).\n"


def clean_dir(v):
    """Richtungsvektor mit ganzzahligen, teilerfremden Komponenten."""
    from math import gcd
    dens = [x.denominator for x in v]
    # auf gemeinsamen Nenner -> ganze Zahlen
    L = 1
    for dd in dens:
        L = L * dd // gcd(L, dd)
    ints = [int(x * L) for x in v]
    g = 0
    for n in ints:
        g = gcd(g, abs(n))
    if g:
        ints = [n // g for n in ints]
    # erstes nicht-null positiv machen (Kosmetik)
    for n in ints:
        if n != 0:
            if n < 0:
                ints = [-m for m in ints]
            break
    return [F(n) for n in ints]


def _demo():
    # Beispiel aus der Aufgabe -> Schnittgerade, Richtung parallel zu (3,-4,6)
    P = [F(1), F(1), F(-1)]; a = [F(1), F(0), F(2)]; b = [F(0), F(2), F(0)]
    Q = [F(0), F(-1), F(1)]; c = [F(-1), F(2), F(-1)]; d = [F(-1), F(4), F(2)]
    out = solve(P, a, b, Q, c, d)
    assert "Schnittgerade" in out, out
    assert "(3, -4, 6)" in out, out  # Richtung = n1 x n2, gekuerzt
    print("Selbsttest ok:\n" + out)


if __name__ == "__main__":
    import sys
    if "--demo" in sys.argv:
        _demo()
        sys.exit()

    print("Zwei Ebenen in Parameterform. Vektoren mit Leerzeichen, z.B.: 1 0 2\n")
    print("E1: x = P + s*a + t*b")
    P = vec("  P (Stuetzvektor): ")
    a = vec("  a (Richtung 1):   ")
    b = vec("  b (Richtung 2):   ")
    print("E2: x = Q + u*c + v*d")
    Q = vec("  Q (Stuetzvektor): ")
    c = vec("  c (Richtung 1):   ")
    d = vec("  d (Richtung 2):   ")
    print()
    print(solve(P, a, b, Q, c, d))

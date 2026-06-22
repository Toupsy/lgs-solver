"""Schnitt zweier Ebenen in Parameterform - GUI, Schritt-fuer-Schritt, 3D-Ansicht.

E1: x = P + s*a + t*b
E2: x = Q + u*c + v*d

Rechenweg: Additionsverfahren - ganze Gleichungen werden kombiniert, sodass
je eine Variable wegfaellt. Nur ganzzahlige Multiplikation/Subtraktion, kein
Teilen waehrend der Elimination, keine Pivotsuche. Exakt mit Fraction.

Start:  python ebenen_schnitt_gui.py
Test:   python ebenen_schnitt_gui.py --demo
"""

from fractions import Fraction as F
from math import gcd, sqrt


# ---------- Formatierung ----------

def fmt(x):
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def fmt_vec(v):
    return "(" + "; ".join(fmt(x) for x in v) + ")"


def fmt_matrix(M, labels=("s", "t", "u", "v", "")):
    cols = len(M[0])
    strs = [[fmt(M[i][j]) for j in range(cols)] for i in range(len(M))]
    w = [max(len(strs[i][j]) for i in range(len(M))) for j in range(cols)]
    head = "    " + "   ".join(labels[j].rjust(w[j]) for j in range(cols))
    out = [head]
    for i in range(len(M)):
        body = "   ".join(strs[i][j].rjust(w[j]) for j in range(cols - 1))
        rhs = strs[i][cols - 1].rjust(w[cols - 1])
        out.append(f" [ {body} | {rhs} ]")
    return "\n".join(out)


def multerm(k, name, lead=False):
    """k*name huebsch: 1->name, -1->-name, sonst k*name. lead=True erzwingt + vorne."""
    if k == 1:
        s = name
    elif k == -1:
        s = f"-{name}"
    else:
        s = f"{fmt(k)}*{name}"
    if lead and k > 0:
        return "+ " + s
    if lead and k < 0:
        return "- " + (s[1:])
    return s


def expr_str(e):
    """e = [const, r-Faktor] -> z.B. '3 + 3*r'."""
    const, r = e
    if r == 0:
        return fmt(const)
    rmag = "r" if abs(r) == 1 else f"{fmt(abs(r))}*r"
    if const == 0:
        return rmag if r > 0 else "-" + rmag
    return f"{fmt(const)} {'+' if r > 0 else '-'} {rmag}"


# ---------- Vektor-Helfer ----------

def vsub(a, b):
    return [a[i] - b[i] for i in range(len(a))]


def row_gcd(row):
    g = 0
    for x in row:
        if x.denominator != 1:
            return 0          # nicht ganzzahlig -> nicht kuerzen
        g = gcd(g, abs(x.numerator))
    return g


def clean_dir(v):
    L = 1
    for x in v:
        L = L * x.denominator // gcd(L, x.denominator)
    ints = [int(x * L) for x in v]
    g = 0
    for n in ints:
        g = gcd(g, abs(n))
    if g:
        ints = [n // g for n in ints]
    for n in ints:
        if n != 0:
            if n < 0:
                ints = [-m for m in ints]
            break
    return [F(n) for n in ints]


# ---------- Loeser mit Protokoll ----------
# steps: Liste von (kind, text) ; kind in {head, text, mat, res}

def solve_with_steps(P, a, b, Q, c, d):
    steps = []
    def add(kind, text):
        steps.append((kind, text))

    geo = {"type": "none", "planes": (P, a, b, Q, c, d)}

    add("head", "Aufgabe")
    add("text", f"E1:  x = {fmt_vec(P)} + s*{fmt_vec(a)} + t*{fmt_vec(b)}\n"
                f"E2:  x = {fmt_vec(Q)} + u*{fmt_vec(c)} + v*{fmt_vec(d)}")

    add("head", "Schritt 1 - Ebenen gleichsetzen")
    add("text", "P + s*a + t*b = Q + u*c + v*d\n"
                "Unbekannte nach links, Konstanten nach rechts:\n"
                "   s*a + t*b - u*c - v*d = Q - P\n"
                f"Q - P = {fmt_vec(Q)} - {fmt_vec(P)} = {fmt_vec(vsub(Q, P))}")

    M = [[a[i], b[i], -c[i], -d[i], Q[i] - P[i]] for i in range(3)]
    add("head", "Schritt 2 - Gleichungssystem (3 Gleichungen, Unbekannte s,t,u,v)")
    add("text", "Spalten = Koeffizienten von s, t, u, v ; rechts die Konstante:")
    add("mat", fmt_matrix(M))

    add("head", "Schritt 3 - Variablen eliminieren (Additionsverfahren)")
    add("text", "Wir kombinieren ganze Gleichungen, sodass je eine Variable wegfaellt.\n"
                "Nur ganzzahlige Vielfache, kein Teilen, keine Pivotsuche.")

    names = ["s", "t", "u", "v"]
    lead = []           # (spalte, zeile) – welche Gleichung 'fuehrt' welche Variable
    srow = 0
    for col in range(4):
        r = next((i for i in range(srow, 3) if M[i][col] != 0), None)
        if r is None:
            continue
        if r != srow:
            M[srow], M[r] = M[r], M[srow]
            add("text", f"Gl.{srow+1} und Gl.{r+1} tauschen, damit '{names[col]}' "
                        f"in Gl.{srow+1} vorkommt:")
            add("mat", fmt_matrix(M))
        for i in range(srow + 1, 3):
            if M[i][col] != 0:
                n, m = M[srow][col], M[i][col]
                M[i] = [n * M[i][k] - m * M[srow][k] for k in range(5)]
                add("text", f"Gl.{i+1} := {multerm(n, f'Gl.{i+1}')} "
                            f"{multerm(-m, f'Gl.{srow+1}', lead=True)}   "
                            f"=> '{names[col]}' faellt weg")
                g = row_gcd(M[i])
                if g > 1:
                    M[i] = [x / g for x in M[i]]
                    add("text", f"Gl.{i+1} durch {g} kuerzen.")
                add("mat", fmt_matrix(M))
        lead.append((col, srow))
        srow += 1
        if srow == 3:
            break

    add("text", "Umgeformtes System (Stufenform):")
    add("mat", fmt_matrix(M))

    # Sonderfaelle
    for i in range(3):
        if all(M[i][j] == 0 for j in range(4)) and M[i][4] != 0:
            add("head", "Ergebnis")
            add("res", f"Gl.{i+1} ergibt 0 = {fmt(M[i][4])}  ->  Widerspruch.\n"
                       "Die Ebenen sind echt parallel, es gibt KEINEN Schnitt.")
            geo["type"] = "none"
            return steps, "Kein Schnitt: Ebenen echt parallel.", geo

    lead_cols = [c for c, _ in lead]
    free = [j for j in range(4) if j not in lead_cols]

    if not free:
        sol = _back_sub(M, lead, free, names, add)
        s0, t0 = sol[0][0], sol[1][0]
        pt = [P[i] + s0 * a[i] + t0 * b[i] for i in range(3)]
        add("head", "Schritt 5 - in E1 einsetzen")
        add("text", f"x = P + s*a + t*b  mit s = {fmt(s0)}, t = {fmt(t0)}\n"
                    f"x = {fmt_vec(pt)}")
        add("head", "Ergebnis")
        add("res", f"Genau ein gemeinsamer Punkt:  {fmt_vec(pt)}")
        geo.update(type="point", point=[float(x) for x in pt])
        return steps, f"Schnittpunkt: {fmt_vec(pt)}", geo

    if len(free) >= 2:
        add("head", "Ergebnis")
        add("res", "Zwei freie Parameter -> die Ebenen sind identisch (ganze Ebene).")
        geo["type"] = "plane"
        return steps, "Ebenen identisch.", geo

    fv = free[0]
    add("head", "Schritt 4 - rueckwaerts einsetzen")
    add("text", f"'{names[fv]}' wird von keiner Gleichung gebunden -> frei waehlbar.\n"
                f"Setze '{names[fv]}' = r. Jede andere Variable: [Konstante] + [Faktor]*r.")

    sol = _back_sub(M, lead, free, names, add)
    add("text", "Zusammengefasst:\n"
                f"   s = {expr_str(sol[0])}\n"
                f"   t = {expr_str(sol[1])}\n"
                f"   u = {expr_str(sol[2])}\n"
                f"   v = {expr_str(sol[3])}")

    stuetz = [P[i] + sol[0][0] * a[i] + sol[1][0] * b[i] for i in range(3)]
    richtung = [sol[0][1] * a[i] + sol[1][1] * b[i] for i in range(3)]
    richtung_c = clean_dir(richtung)

    add("head", "Schritt 5 - in E1 einsetzen")
    add("text", "x = P + s*a + t*b , s und t durch r ersetzen:\n"
                f"Stuetzvektor (r=0):       {fmt_vec(stuetz)}\n"
                f"Richtung (Faktor vor r):  {fmt_vec(richtung)}  ->  gekuerzt {fmt_vec(richtung_c)}")

    res = f"g:  x = {fmt_vec(stuetz)} + r * {fmt_vec(richtung_c)}"
    add("head", "Ergebnis - Schnittgerade")
    add("res", res)
    geo.update(type="line",
               stuetz=[float(x) for x in stuetz],
               richtung=[float(x) for x in richtung_c])
    return steps, res, geo


def _back_sub(M, lead, free, names, add):
    sol = {j: [F(0), F(1)] for j in free}
    for col, row in reversed(lead):
        pv = M[row][col]
        acc = [M[row][4], F(0)]
        for j in range(4):
            if j != col and M[row][j] != 0:
                xj = sol[j]
                acc = [acc[0] - M[row][j] * xj[0], acc[1] - M[row][j] * xj[1]]
        sol[col] = [acc[0] / pv, acc[1] / pv]
        add("text", f"Gl.{row+1} nach '{names[col]}' aufloesen:  "
                    f"{names[col]} = {expr_str(sol[col])}")
    return [sol[j] for j in range(4)]


# ---------- 3D-Zeichnung (reines tkinter) ----------

def _iso(p):
    x, y, z = p
    return (x - y) * 0.8660, z - (x + y) * 0.5     # (rechts, oben)


def _norm(v, length):
    n = sqrt(sum(c * c for c in v)) or 1.0
    return [c / n * length for c in v]


def draw_geometry(canvas, geo):
    canvas.delete("all")
    W = canvas.winfo_width() or 460
    H = canvas.winfo_height() or 460
    P, a, b, Q, c, d = geo["planes"]
    P = [float(x) for x in P]; a = [float(x) for x in a]; b = [float(x) for x in b]
    Q = [float(x) for x in Q]; c = [float(x) for x in c]; d = [float(x) for x in d]

    S = 4.0
    def corners(mitte, d1, d2):
        # Ebenen-Stueck um einen Punkt 'mitte' (der auf der Ebene liegt) herum.
        u1, u2 = _norm(d1, S), _norm(d2, S)
        return [[mitte[k] + i * u1[k] + j * u2[k] for k in range(3)]
                for i, j in ((-1, -1), (1, -1), (1, 1), (-1, 1))]

    # Beide Patches um einen gemeinsamen Punkt zeichnen, der auf beiden Ebenen
    # liegt -> sie kreuzen sich sichtbar entlang der Schnittgeraden/des Punktes.
    if geo["type"] == "line":
        fokus1 = fokus2 = geo["stuetz"]
    elif geo["type"] == "point":
        fokus1 = fokus2 = geo["point"]
    else:
        fokus1, fokus2 = P, Q

    poly1 = corners(fokus1, a, b)
    poly2 = corners(fokus2, c, d)
    pts = poly1 + poly2

    line_pts = None
    if geo["type"] == "line":
        dirn = _norm(geo["richtung"], S + 1.5)
        s = geo["stuetz"]
        line_pts = [[s[k] - dirn[k] for k in range(3)],
                    [s[k] + dirn[k] for k in range(3)]]
        pts = pts + line_pts
    elif geo["type"] == "point":
        pts = pts + [geo["point"]]

    # Projektor an Canvas anpassen
    raw = [_iso(p) for p in pts]
    xs = [r[0] for r in raw]; ys = [r[1] for r in raw]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    margin = 36
    k = min((W - 2 * margin) / (maxx - minx or 1),
            (H - 2 * margin) / (maxy - miny or 1))

    def proj(p):
        rx, ry = _iso(p)
        return margin + (rx - minx) * k, H - margin - (ry - miny) * k

    def flat(poly):
        out = []
        for p in poly:
            sx, sy = proj(p)
            out += [sx, sy]
        return out

    canvas.create_polygon(*flat(poly1), fill="#4a90d9", outline="#1c5a96",
                          width=2, stipple="gray25")
    canvas.create_polygon(*flat(poly2), fill="#d9534f", outline="#9c2b27",
                          width=2, stipple="gray25")

    if line_pts:
        x1, y1 = proj(line_pts[0]); x2, y2 = proj(line_pts[1])
        canvas.create_line(x1, y1, x2, y2, fill="white", width=7)      # Kontur
        canvas.create_line(x1, y1, x2, y2, fill="#1a7d33", width=4)
        sx, sy = proj(geo["stuetz"])
        canvas.create_oval(sx - 5, sy - 5, sx + 5, sy + 5, fill="#1a7d33",
                          outline="white", width=2)
    elif geo["type"] == "point":
        sx, sy = proj(geo["point"])
        canvas.create_oval(sx - 6, sy - 6, sx + 6, sy + 6, fill="#f0ad4e",
                          outline="#9c6a13", width=2)

    # Legende
    leg = [("#4a90d9", "E1"), ("#d9534f", "E2")]
    if geo["type"] == "line":
        leg.append(("#1a7d33", "Schnittgerade g"))
    elif geo["type"] == "point":
        leg.append(("#f0ad4e", "Schnittpunkt"))
    elif geo["type"] == "plane":
        leg.append(("#888888", "Ebenen identisch"))
    else:
        leg.append(("#888888", "kein Schnitt (parallel)"))
    for i, (col, lab) in enumerate(leg):
        y = 14 + i * 20
        canvas.create_rectangle(12, y, 28, y + 12, fill=col, outline="")
        canvas.create_text(34, y + 6, text=lab, anchor="w",
                           font=("Segoe UI", 9), fill="#222")


# ---------- GUI ----------

def launch_gui():
    import tkinter as tk
    from tkinter import ttk, messagebox

    root = tk.Tk()
    root.title("Schnitt zweier Ebenen (Parameterform)")
    root.configure(bg="#f4f4f4")

    entries = {}
    last_geo = {"g": None}

    left = tk.Frame(root, padx=12, pady=12, bg="#f4f4f4")
    left.grid(row=0, column=0, sticky="nw")

    def vec_row(parent, key, label, r, color):
        tk.Label(parent, text=label, width=16, anchor="w", bg="#f4f4f4"
                 ).grid(row=r, column=0, sticky="w")
        es = []
        for j in range(3):
            e = tk.Entry(parent, width=6, justify="center")
            e.grid(row=r, column=1 + j, padx=2, pady=2)
            es.append(e)
        entries[key] = es

    tk.Label(left, text="E1:  x = P + s·a + t·b", font=("Segoe UI", 10, "bold"),
             fg="#1c5a96", bg="#f4f4f4").grid(row=0, column=0, columnspan=4, sticky="w")
    vec_row(left, "P", "P (Stütze)", 1, None)
    vec_row(left, "a", "a (Richtung 1)", 2, None)
    vec_row(left, "b", "b (Richtung 2)", 3, None)
    tk.Label(left, text="E2:  x = Q + u·c + v·d", font=("Segoe UI", 10, "bold"),
             fg="#9c2b27", bg="#f4f4f4").grid(row=4, column=0, columnspan=4,
                                              sticky="w", pady=(10, 0))
    vec_row(left, "Q", "Q (Stütze)", 5, None)
    vec_row(left, "c", "c (Richtung 1)", 6, None)
    vec_row(left, "d", "d (Richtung 2)", 7, None)
    tk.Label(left, text="ganze Zahlen oder Brüche wie 1/2", fg="gray", bg="#f4f4f4"
             ).grid(row=8, column=0, columnspan=4, sticky="w", pady=(4, 0))

    # rechts: Notebook mit Rechenweg + 3D
    nb = ttk.Notebook(root)
    nb.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)

    txt = tk.Text(nb, width=58, height=34, font=("Consolas", 10), wrap="none",
                  bg="white", relief="flat", padx=8, pady=8)
    yscroll = tk.Scrollbar(txt, command=txt.yview)
    txt.configure(yscrollcommand=yscroll.set)
    yscroll.pack(side="right", fill="y")
    txt.tag_configure("head", font=("Segoe UI", 11, "bold"), foreground="#1c5a96",
                      spacing1=10, spacing3=4)
    txt.tag_configure("text", font=("Segoe UI", 10), foreground="#222", spacing3=2)
    txt.tag_configure("mat", font=("Consolas", 10), foreground="#444",
                      background="#f0f4f8", lmargin1=10, lmargin2=10)
    txt.tag_configure("res", font=("Consolas", 11, "bold"), foreground="#1a7d33",
                      background="#eaf7ec", lmargin1=8, lmargin2=8, spacing1=4, spacing3=6)

    canvas = tk.Canvas(nb, width=460, height=460, bg="white", highlightthickness=0)

    nb.add(txt, text="  Rechenweg  ")
    nb.add(canvas, text="  3D-Ansicht  ")

    state = {"steps": [], "shown": 0, "geo": None}
    hilfe = tk.BooleanVar(value=True)

    def read_vec(key):
        return [F(e.get().strip().replace(",", ".")) for e in entries[key]]

    def render():
        n, shown = len(state["steps"]), state["shown"]
        txt.delete("1.0", "end")
        for kind, text in state["steps"][:shown]:
            txt.insert("end", text + "\n", kind)
        txt.see("end")
        done = shown >= n
        btn_next.config(state="disabled" if done else "normal",
                        text="Fertig ✓" if done else f"Nächster Schritt  ({shown}/{n})")
        # 3D erst zeigen, wenn alles aufgedeckt ist (sonst waere es ja die Loesung)
        if done and state["geo"]:
            draw_geometry(canvas, state["geo"])
        else:
            canvas.delete("all")
            cw = canvas.winfo_width() or 460
            ch = canvas.winfo_height() or 460
            canvas.create_text(cw / 2, ch / 2, width=cw - 40, justify="center",
                               fill="#999", font=("Segoe UI", 11),
                               text="3D-Ansicht erscheint,\nsobald alle Schritte "
                                    "aufgedeckt sind.")

    def on_solve():
        try:
            P = read_vec("P"); a = read_vec("a"); b = read_vec("b")
            Q = read_vec("Q"); c = read_vec("c"); d = read_vec("d")
        except Exception:
            messagebox.showerror("Eingabefehler",
                                 "Bitte alle 18 Felder ausfüllen (z.B. 1, -2, 1/2).")
            return
        steps, _, geo = solve_with_steps(P, a, b, Q, c, d)
        state.update(steps=steps, geo=geo,
                     shown=0 if hilfe.get() else len(steps))
        render()

    def next_step():
        if state["shown"] < len(state["steps"]):
            state["shown"] += 1
            render()

    def show_all():
        state["shown"] = len(state["steps"])
        render()

    def on_example():
        ex = {"P": (1, 1, -1), "a": (1, 0, 2), "b": (0, 2, 0),
              "Q": (0, -1, 1), "c": (-1, 2, -1), "d": (-1, 4, 2)}
        for k, vals in ex.items():
            for e, val in zip(entries[k], vals):
                e.delete(0, "end"); e.insert(0, str(val))

    btns = tk.Frame(left, bg="#f4f4f4")
    btns.grid(row=9, column=0, columnspan=4, sticky="w", pady=(10, 0))
    tk.Button(btns, text="Lösen", command=on_solve, width=12,
              bg="#4a90d9", fg="white", relief="flat").pack(side="left", padx=2)
    tk.Button(btns, text="Beispiel laden", command=on_example, width=14,
              relief="flat").pack(side="left", padx=2)

    tk.Checkbutton(left, text="Hilfe-Modus: Schritte einzeln aufdecken",
                   variable=hilfe, command=on_solve, bg="#f4f4f4"
                   ).grid(row=10, column=0, columnspan=4, sticky="w", pady=(10, 2))

    hbtns = tk.Frame(left, bg="#f4f4f4")
    hbtns.grid(row=11, column=0, columnspan=4, sticky="w")
    btn_next = tk.Button(hbtns, text="Nächster Schritt", command=next_step,
                         width=20, bg="#1a7d33", fg="white", relief="flat")
    btn_next.pack(side="left", padx=2)
    tk.Button(hbtns, text="Alles zeigen", command=show_all, width=12,
              relief="flat").pack(side="left", padx=2)

    canvas.bind("<Configure>", lambda e: render())

    on_example()
    on_solve()
    root.mainloop()


def _demo():
    P = [F(1), F(1), F(-1)]; a = [F(1), F(0), F(2)]; b = [F(0), F(2), F(0)]
    Q = [F(0), F(-1), F(1)]; c = [F(-1), F(2), F(-1)]; d = [F(-1), F(4), F(2)]
    steps, res, geo = solve_with_steps(P, a, b, Q, c, d)
    for kind, text in steps:
        print(("# " if kind == "head" else "") + text)
        print()
    print(">>> Kurzergebnis:", res)
    assert "(3; -4; 6)" in res, res
    assert geo["type"] == "line"
    print("Selbsttest ok.")


if __name__ == "__main__":
    import sys
    if "--demo" in sys.argv:
        _demo()
    else:
        launch_gui()

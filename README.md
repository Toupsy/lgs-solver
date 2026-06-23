# Schnitt zweier Ebenen (Parameterform)

Webtool, das den Schnitt zweier in Parameterform gegebener Ebenen berechnet –
mit vollständigem Rechenweg (Additionsverfahren, exakte Bruchrechnung) und
drehbarer 3D-Ansicht. Gedacht für den Mathematikunterricht.

**E1:** x = P + s·a + t·b  **E2:** x = Q + u·c + v·d

## Funktionen
- Rechenweg in echter Mathematik-Schrift (LaTeX/MathJax): Vektoren als
  Spaltenvektoren, Brüche als Bruch, das LGS als augmentierte Matrix.
- Exakte Rechnung mit Brüchen (kein Rundungsfehler), bleibt möglichst ganzzahlig.
- Lösung als Additionsverfahren – ganze Gleichungen kombinieren, keine Pivotsuche.
- **Hilfe-Modus:** Rechenschritte einzeln aufdecken zum Selber-Lösen.
- **3D-Ansicht:** beide Ebenen + Schnittgerade/-punkt, mit Maus oder Finger drehbar, Zoom per Scrollen/Pinch.
- Fälle: Schnittgerade, einzelner Schnittpunkt, identische Ebenen, echt parallel.

## Nutzung
Einfach `index.html` im Browser öffnen – keine Installation, kein Server nötig.
Die ganze App steckt in dieser einen Datei. Für die Formelschrift wird MathJax
per CDN nachgeladen, dafür ist beim Öffnen eine Internetverbindung nötig.

## Deploy (GitHub Pages)
Settings → Pages → Branch `main`, Ordner `/ (root)`. Die Seite ist dann unter
`https://<user>.github.io/<repo>/` erreichbar und kann auf der Homepage verlinkt
oder per `<iframe>` eingebettet werden.

## Deploy via Portainer (Docker, z.B. auf NAS)
Die App läuft als winziger nginx-Container.

**Portainer → Stacks → Add stack → Repository:**
- Repository URL: dieses Git-Repo
- Compose path: `docker-compose.yml`
- Deploy

Danach erreichbar unter `http://<nas-ip>:1913/`. Den Host-Port in
`docker-compose.yml` anpassen, falls 1913 belegt ist.

Alternativ ohne Git (Web editor): den Inhalt von `docker-compose.yml` einfügen –
Portainer baut das Image dann aus dem `Dockerfile`.

Manuell auf der Kommandozeile:

    docker compose up -d        # baut und startet, Port 1913

## Desktop-Variante (optional)
`ebenen_schnitt_gui.py` ist eine eigenständige tkinter-App (gleiche Funktionen).
Eine `.exe` lässt sich damit bauen:

    python -m PyInstaller --onefile --windowed --name EbenenSchnitt ebenen_schnitt_gui.py

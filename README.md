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
Die App läuft mit dem fertigen Standard-Image `nginx:alpine`. Portainer muss
keinen `Dockerfile` bauen. Beim Container-Start lädt nginx die aktuelle
`index.html` aus GitHub.

**Portainer → Stacks → Add stack → Web editor:**

```yaml
services:
  lgs-solver:
    image: nginx:alpine
    container_name: lgs-solver
    command: >
      /bin/sh -c "wget -O /usr/share/nginx/html/index.html
      https://raw.githubusercontent.com/Toupsy/lgs-solver/main/index.html
      && nginx -g 'daemon off;'"
    ports:
      - "1913:80"
    restart: unless-stopped
```

Danach erreichbar unter `http://<nas-ip>:1913/`. Den Host-Port anpassen, falls
1913 belegt ist.

Wenn Portainer meldet `failed to read dockerfile: open Dockerfile: no such file
or directory`, ist noch eine alte Compose-Version mit `build:` im Stack. In dem
Fall den Stack-Editor öffnen, alles Alte entfernen und die image-only Compose-
Version oben einfügen.

Manuell auf der Kommandozeile:

    docker compose up -d        # zieht nginx:alpine und lädt index.html beim Start

## Desktop-Variante (optional)
`ebenen_schnitt_gui.py` ist eine eigenständige tkinter-App (gleiche Funktionen).
Eine `.exe` lässt sich damit bauen:

    python -m PyInstaller --onefile --windowed --name EbenenSchnitt ebenen_schnitt_gui.py

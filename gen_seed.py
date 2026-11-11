#!/usr/bin/env python3
"""Erzeugt seed.json: Beispielübungen samt Strichmännchen (SVG als Data-URL).
Aufruf: python3 gen_seed.py   -> schreibt seed.json (+ contact.svg zur Kontrolle)"""
import base64, json, math

INK, HI, G = "#1c2733", "#1f7a5c", 135  # Farbe, Akzentfarbe (bewegter Körperteil), Bodenhöhe


def fig(label, neck, hip, arms, legs, head=None, bend=None, extra=""):
    """Ein Bild 200x150. arms/legs: Listen aus (Gelenk, Ende[, hervorheben])."""
    if head is None:  # Kopf in Verlängerung der Wirbelsäule
        dx, dy = neck[0] - hip[0], neck[1] - hip[1]
        n = math.hypot(dx, dy)
        head = (neck[0] + dx / n * 12, neck[1] + dy / n * 12)
    spine = f"M{neck[0]} {neck[1]} " + (f"Q{bend[0]} {bend[1]} " if bend else "L") + f"{hip[0]} {hip[1]}"
    out = [f'<path d="{spine}" stroke="{INK}"/>']
    for root, limbs in ((neck, arms), (hip, legs)):
        for mid, end, *hi in limbs:
            pts = " ".join(f"{x},{y}" for x, y in (root, mid, end))
            out.append(f'<polyline points="{pts}" stroke="{HI if hi and hi[0] else INK}"/>')
    out.append(f'<circle cx="{head[0]:.0f}" cy="{head[1]:.0f}" r="9" fill="#fff" stroke="{INK}"/>')
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 150">'
        '<defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">'
        f'<path d="M0 0L10 5L0 10z" fill="{HI}"/></marker></defs>'
        '<rect width="200" height="150" rx="8" fill="#f4f7f9"/>'
        f'<line x1="8" y1="{G + 3}" x2="192" y2="{G + 3}" stroke="#b8c2cc" stroke-width="2"/>'
        f'<text x="10" y="18" font-family="Segoe UI,Arial,sans-serif" font-size="12" fill="#6b7785">{label}</text>'
        f'{extra}<g fill="none" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">{"".join(out)}</g></svg>'
    )


def arrow(x1, y1, x2, y2, cx=None, cy=None):
    d = f"M{x1} {y1} Q{cx} {cy} {x2} {y2}" if cx is not None else f"M{x1} {y1} L{x2} {y2}"
    return f'<path d="{d}" fill="none" stroke="{HI}" stroke-width="2.5" stroke-dasharray="5 4" marker-end="url(#a)"/>'


def wall(x):
    return f'<line x1="{x}" y1="26" x2="{x}" y2="{G + 3}" stroke="#b8c2cc" stroke-width="4"/>'


def band(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#d9822b" stroke-width="3"/>'


# Wiederkehrende Haltungen
ARMS_DOWN = [((88, 64), (86, 86)), ((112, 64), (114, 86))]
LEGS_STAND = [((94, 112), (91, G)), ((106, 112), (109, G))]
Q_ARMS = [((61, 112), (60, G)), ((67, 112), (68, G))]          # Vierfüßler: Arme
Q_LEGS = [((125, G), (160, 133)), ((131, G), (166, 133))]      # Vierfüßler: Beine
Q = dict(neck=(62, 90), hip=(125, 90), head=(48, 84))

U = []  # (Name, Kategorie, Text, [Bild, Bild])

U.append(("Hüftstrecker im Vierfüßlerstand", "Hüfte",
    "Vierfüßlerstand, Rücken gerade\nEin Bein gestreckt nach hinten abheben\nBein gerade lassen, Richtung 17 Uhr führen\n3 × 12 Wiederholungen pro Seite", [
    fig("Start", **Q, arms=Q_ARMS, legs=Q_LEGS),
    fig("Ende", **Q, arms=Q_ARMS, legs=[Q_LEGS[0], ((156, 90), (187, 88), True)], extra=arrow(170, 125, 185, 100, 185, 115)),
]))

side = dict(neck=(52, 122), hip=(115, 124), head=(38, 119), arms=[((45, 133), (36, 128)), ((75, 128), (86, 134))])
U.append(("Seitliches Beinheben", "Hüfte",
    "Seitlage, unteres Bein leicht gebeugt\nOberes Bein gestreckt anheben\nFußspitze zeigt nach vorne, nicht nach oben\n3 × 15 Wiederholungen pro Seite", [
    fig("Start", **side, legs=[((145, 130), (172, 134)), ((148, 122), (180, 122))]),
    fig("Ende", **side, legs=[((145, 130), (172, 134)), ((144, 106), (171, 88), True)], extra=arrow(183, 116, 178, 92, 186, 104)),
]))

lunge_arms = [((86, 76), (96, 92)), ((104, 76), (98, 92))]
U.append(("Hüftbeuger-Dehnung im Kniestand", "Hüfte",
    "Ausfallschritt, hinteres Knie auf dem Boden\nOberkörper aufrecht, Hände an die Hüfte\nBecken langsam nach vorne unten schieben\n3 × 30 Sekunden pro Seite halten", [
    fig("Start", neck=(92, 50), hip=(92, 96), arms=lunge_arms, legs=[((124, 99), (124, G)), ((80, G), (46, 133))]),
    fig("Ende", neck=(102, 58), hip=(102, 104), arms=[((96, 84), (106, 100)), ((114, 84), (108, 100))],
        legs=[((134, 108), (124, G)), ((80, G), (46, 133), True)], extra=arrow(70, 100, 88, 112)),
]))

sup_arms = [((75, 131), (100, 134))]
U.append(("Brücke (Bridging)", "Rücken",
    "Rückenlage, Füße hüftbreit aufstellen\nBecken anheben, bis Oberschenkel und Rumpf eine Linie bilden\nOben 3 Sekunden halten, Po anspannen\n3 × 10 Wiederholungen", [
    fig("Start", neck=(47, 128), hip=(105, 129), head=(34, 126), arms=sup_arms, legs=[((135, 100), (150, G))]),
    fig("Ende", neck=(47, 128), hip=(105, 106), head=(34, 126), arms=sup_arms, legs=[((140, 98), (150, G))], extra=arrow(105, 132, 105, 116)),
]))

U.append(("Katze – Kuh", "Rücken",
    "Vierfüßlerstand, Hände unter den Schultern\nRücken langsam rund machen, Kinn zur Brust\nDann ins leichte Hohlkreuz, Blick nach vorne\n2 × 10 langsame Wiederholungen", [
    fig("Katze", neck=(62, 90), hip=(125, 90), head=(50, 104), bend=(93, 58), arms=Q_ARMS, legs=Q_LEGS, extra=arrow(93, 60, 93, 44)),
    fig("Kuh", neck=(62, 90), hip=(125, 90), head=(47, 78), bend=(93, 108), arms=Q_ARMS, legs=Q_LEGS, extra=arrow(93, 80, 93, 94)),
]))

U.append(("Vogel-Hund (Bird Dog)", "Rücken",
    "Vierfüßlerstand, Bauch leicht anspannen\nRechten Arm und linkes Bein gleichzeitig strecken\nBecken bleibt ruhig, kein Hohlkreuz\n3 × 8 Wiederholungen pro Seite, je 3 Sekunden halten", [
    fig("Start", **Q, arms=Q_ARMS, legs=Q_LEGS),
    fig("Ende", **Q, arms=[Q_ARMS[1], ((40, 88), (18, 86), True)], legs=[Q_LEGS[0], ((156, 90), (187, 88), True)]),
]))

plank = dict(neck=(62, 104), hip=(120, 110), head=(49, 99), arms=[((60, G), (82, G))])
U.append(("Unterarmstütz (Plank)", "Rücken",
    "Ellenbogen unter den Schultern aufstützen\nKörper bildet eine gerade Linie\nBauch und Po fest anspannen, nicht durchhängen\n3 × 20–30 Sekunden halten", [
    fig("Leichter: auf den Knien", **plank, legs=[((152, G), (176, 122))]),
    fig("Voll: auf den Füßen", **plank, legs=[((150, 120), (182, 133))]),
]))

U.append(("Außenrotation mit Band", "Schulter",
    "Ellenbogen 90° gebeugt, fest am Körper\nBand mit dem Unterarm nach außen ziehen\nSchulter bleibt tief, kein Hochziehen\n3 × 15 Wiederholungen pro Seite", [
    fig("Start", neck=(100, 42), hip=(100, 88), arms=[ARMS_DOWN[0], ((112, 66), (96, 68))], legs=LEGS_STAND,
        extra=wall(22) + band(22, 68, 96, 68)),
    fig("Ende", neck=(100, 42), hip=(100, 88), arms=[ARMS_DOWN[0], ((112, 66), (134, 64), True)], legs=LEGS_STAND,
        extra=wall(22) + band(22, 68, 134, 64) + arrow(118, 80, 140, 76, 130, 84)),
]))

U.append(("Seitheben", "Schulter",
    "Aufrecht stehen, Arme hängen locker\nBeide Arme seitlich bis auf Schulterhöhe heben\nSchultern nicht zu den Ohren ziehen\n3 × 12 Wiederholungen, langsam absenken", [
    fig("Start", neck=(100, 42), hip=(100, 88), arms=ARMS_DOWN, legs=LEGS_STAND),
    fig("Ende", neck=(100, 42), hip=(100, 88), arms=[((76, 46), (52, 46), True), ((124, 46), (148, 46), True)], legs=LEGS_STAND,
        extra=arrow(62, 80, 46, 56, 48, 70) + arrow(138, 80, 154, 56, 152, 70)),
]))

U.append(("Wandsitz", "Knie",
    "Rücken an die Wand, Füße hüftbreit\nIn die Hocke rutschen bis ca. 90° Kniewinkel\nKnie bleiben über den Sprunggelenken\n3 × 30 Sekunden halten", [
    fig("Start", neck=(140, 45), hip=(140, 90), arms=[((136, 68), (134, 88))], legs=[((137, 112), (133, G))], extra=wall(154)),
    fig("Ende", neck=(142, 60), hip=(142, 105), arms=[((134, 84), (118, 98))], legs=[((106, 105), (106, G), True)],
        extra=wall(154) + arrow(165, 55, 165, 85)),
]))

U.append(("Kniebeuge", "Knie",
    "Füße schulterbreit, Fußspitzen leicht nach außen\nPo nach hinten unten schieben wie beim Hinsetzen\nKnie zeigen in Richtung der Fußspitzen\n3 × 12 Wiederholungen", [
    fig("Start", neck=(95, 42), hip=(95, 88), arms=[((92, 64), (94, 86))], legs=[((97, 112), (95, G))]),
    fig("Ende", neck=(100, 62), hip=(78, 100), arms=[((120, 66), (140, 64))], legs=[((114, 104), (100, G), True)],
        extra=arrow(62, 70, 62, 98)),
]))

U.append(("Einbeinstand", "Knie",
    "Auf einem Bein stehen, Knie leicht gebeugt\nBecken gerade halten\nKnie zeigt über die zweite Zehe\n3 × 30 Sekunden pro Seite", [
    fig("Start", neck=(100, 42), hip=(100, 88), arms=ARMS_DOWN, legs=LEGS_STAND),
    fig("Ende", neck=(100, 42), hip=(100, 88), arms=[((80, 56), (60, 62)), ((120, 56), (140, 62))],
        legs=[((99, 112), (100, G)), ((120, 96), (116, 118), True)]),
]))

uri = lambda svg: "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()
data = {"praxis": "Praxis Mustermann", "logo": "", "uebungen": [
    {"id": str(i + 1), "name": n, "kategorie": k, "text": t, "bilder": [uri(s) for s in pics]}
    for i, (n, k, t, pics) in enumerate(U)]}
json.dump(data, open("seed.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# Kontrollbogen: alle Bilder nebeneinander
cells = "".join(
    f'<g transform="translate({(j % 2) * 210 + (i % 3) * 430},{(i // 3) * 160})">{s.replace("<svg ", "<svg width=\'200\' height=\'150\' ")}</g>'
    for i, (*_, pics) in enumerate(U) for j, s in enumerate(pics))
open("contact.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="1290" height="{(len(U) + 2) // 3 * 160}">{cells}</svg>')
print(len(U), "Übungen geschrieben")

#Rodolfo Milhomem
#https://github.com/rodolfo-space-force/
"""
Leitor e interpretador de TLE (Two-Line Element Set)
Agora inclui o nome do satélite (se presente como cabeçalho)
"""

import json

# Definições de campos conforme documentação NORAD
line1_fields = {
    (1, 1): "Line Number",
    (3, 7): "Satellite Catalog Number",
    (8, 8): "Classification",
    (10, 17): "International Designator",
    (19, 32): "Epoch",
    (34, 43): "1st Derivative of Mean Motion",
    (45, 52): "2nd Derivative of Mean Motion",
    (54, 61): "BSTAR Drag Term",
    (63, 63): "Ephemeris/Element Set Type",
    (65, 68): "Element Set Number",
    (69, 69): "Checksum"
}

line2_fields = {
    (1, 1): "Line Number",
    (3, 7): "Satellite Catalog Number",
    (9, 16): "Inclination (deg)",
    (18, 25): "Right Ascension of Asc. Node (deg)",
    (27, 33): "Eccentricity (decimal point assumed)",
    (35, 42): "Argument of Perigee (deg)",
    (44, 51): "Mean Anomaly (deg)",
    (53, 63): "Mean Motion (rev/day)",
    (64, 68): "Revolution Number at Epoch",
    (69, 69): "Checksum"
}

def parse_tle(line, fields):
    """Extrai valores de uma linha TLE com base nos campos"""
    parsed = {}
    for (start, end), description in fields.items():
        value = line[start - 1:end].strip()
        parsed[description] = value
    return parsed

# === Leitura do arquivo ===
with open("STARLINK-34935.txt", "r") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

# Detectar se a primeira linha é nome ou já começa com TLE
name = None
if not (lines[0].startswith("1 ") or lines[0].startswith("2 ")):
    name = lines[0]
    tle_lines = [l for l in lines[1:] if l.startswith("1 ") or l.startswith("2 ")]
else:
    tle_lines = [l for l in lines if l.startswith("1 ") or l.startswith("2 ")]

# Separar linhas 1 e 2
tle_line1 = tle_lines[0]
tle_line2 = tle_lines[1]

# Processar
parsed_line1 = parse_tle(tle_line1, line1_fields)
parsed_line2 = parse_tle(tle_line2, line2_fields)

# ---- Saída em texto corrido ----
if name:
    print(f"=== Satélite: {name} ===\n")

print("=== Linha 1 ===")
for desc, val in parsed_line1.items():
    print(f"{desc}: {val}")

print("\n=== Linha 2 ===")
for desc, val in parsed_line2.items():
    print(f"{desc}: {val}")

# ---- JSON ----
tle_json = {
    "Line1": parsed_line1,
    "Line2": parsed_line2
}
if name:
    tle_json["Name"] = name

with open("output.json", "w", encoding="utf-8") as outfile:
    json.dump(tle_json, outfile, indent=4, ensure_ascii=False)

print("\nJSON salvo em 'output.json'")

# Licença
#Este projeto está licenciado sob a **Licença MIT**.  
#Você pode usar, modificar e redistribuir este código livremente, **desde que mencione o autor original**.

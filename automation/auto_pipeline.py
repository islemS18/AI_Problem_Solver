import subprocess
import sys
import re

# ======================================================
# CONFIG PROBLÈMES
# ======================================================

BASE_PATH = r"C:\Users\HP\OneDrive\Desktop\AIprojet"

PROBLEMS = {
    "1": {
        "name": "Loup Chevre Salade",
        "xml":  BASE_PATH + r"\Les Problemes\Loup_Chevre_Salade\LoupChevreSalade.xml",
        "n":    "9",
        "extra": []
    },
    "2": {
        "name": "Seaux (Die Hard)",
        "xml":  BASE_PATH + r"\Les Problemes\Probleme_des_seaux\seaux.xml",
        "n":    "10",
        "extra": []
    },
    "3": {
        "name": "Missionnaires Cannibales",
        "xml":  BASE_PATH + r"\Les Problemes\Probleme3\probleme3.xml",
        "n":    "10",
        "extra": []
    }
}

TALOS_JAR  = BASE_PATH + r"\talosExamples-0.4.1-SNAPSHOT-jar-with-dependencies.jar"
OUTPUT_DOT = BASE_PATH + r"\automation\solution.dot"


# ======================================================
# EXTRACTION : PREMIÈRE SOLUTION SEULEMENT
# ======================================================

def extract_first_solution(output):
    for line in output.split('\n'):
        line = line.strip()
        if line.startswith('(') and '|' in line:
            states = re.findall(r'\([^)]*\)', line)
            valid = [s for s in states if re.search(r'[A-Za-z]', s)]
            if valid:
                return valid
    return []


# ======================================================
# DOT GENERATOR : nœuds numérotés pour éviter les doublons
# ======================================================

def generate_dot(solution, problem_name):
    dot = []
    dot.append("digraph G {")
    dot.append(f'    label="{problem_name}";')
    dot.append('    node [shape=circle];')
    dot.append('')

    if not solution:
        dot.append("    // Aucune solution trouvee")
        dot.append("}")
        return "\n".join(dot)

    # Chaque nœud = "étape_N\nLABEL" pour être unique même si label répété
    def node_id(i, label):
        return f"step{i}"

    def node_label(i, label):
        return f"Etape {i}\\n{label}"

    # Déclaration des nœuds avec leur label lisible
    for i, s in enumerate(solution):
        nid   = node_id(i, s)
        nlbl  = node_label(i, s)
        if i == 0:
            dot.append(f'    {nid} [label="{nlbl}", color=green, style=filled, fillcolor=lightgreen];')
        elif i == len(solution) - 1:
            dot.append(f'    {nid} [label="{nlbl}", color=blue, style=filled, fillcolor=lightblue];')
        else:
            dot.append(f'    {nid} [label="{nlbl}"];')

    dot.append('')

    # Transitions en rouge gras
    for i in range(len(solution) - 1):
        a = node_id(i, solution[i])
        b = node_id(i+1, solution[i+1])
        dot.append(f'    {a} -> {b} [color=red, penwidth=3];')

    dot.append("}")
    return "\n".join(dot)


# ======================================================
# MAIN
# ======================================================

print("=== AI GRAPH SOLVER FINAL ===\n")
print("Choose problem:")
print("1 - Loup Chevre Salade")
print("2 - Seaux (Die Hard)")
print("3 - Missionnaires Cannibales")

choice = input("\nYour choice: ").strip()

if choice not in PROBLEMS:
    print("Invalid choice")
    sys.exit()

prob     = PROBLEMS[choice]
xml_file = prob["xml"]
n        = prob["n"]

print(f"\nSelected : {prob['name']}")
print(f"XML      : {xml_file}")
print(f"n max    : {n} etapes")

# ======================================================
# RUN TALOS
# ======================================================

cmd = [
    "java", "-cp", TALOS_JAR,
    "StateGraph",
    "-n",     n,
    "-print", "1",
    "-file",  xml_file
] + prob.get("extra", [])

print("\nRunning Talos...")
result = subprocess.run(cmd, capture_output=True, text=True)
output = result.stdout

print("\n================ TALOS OUTPUT ================")
print(output)

# ======================================================
# EXTRACT + AFFICHE PREMIERE SOLUTION
# ======================================================

solution = extract_first_solution(output)

print("\n================ PREMIERE SOLUTION ================")
if solution:
    for i, s in enumerate(solution):
        print(f"  Etape {i}: {s}")
else:
    print("  Aucune solution trouvee !")
    print(f"  Verifiez le fichier XML : {xml_file}")

# ======================================================
# GENERATE DOT
# ======================================================

dot_content = generate_dot(solution, prob["name"])

with open(OUTPUT_DOT, "w", encoding="utf-8") as f:
    f.write(dot_content)

print(f"\nDOT GENERATED : {OUTPUT_DOT}")
if solution:
    print("\nContenu DOT :")
    print(dot_content)

print("\nDONE")
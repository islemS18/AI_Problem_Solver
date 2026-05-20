import re
import subprocess
import sys

# ============================================================
# CONFIGURATION
# ============================================================

BASE_PATH   = r"C:\Users\HP\OneDrive\Desktop\AIprojet"
TALOS_JAR   = BASE_PATH + r"\talosExamples-0.4.1-SNAPSHOT-jar-with-dependencies.jar"
PROMPT_FILE = BASE_PATH + r"\automation\prompt.txt"
OUTPUT_XML  = BASE_PATH + r"\automation\generated.xml"
OUTPUT_DOT  = BASE_PATH + r"\automation\generated_solution.dot"

# ============================================================
# AFFICHER LE PROMPT À COPIER DANS CLAUDE.AI
# ============================================================

def get_prompt(problem_description):
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        base_prompt = f.read()
    return base_prompt + "\n" + problem_description

# ============================================================
# PARSE TRANSITIONS (lignes de chiffres)
# ============================================================

def parse_transitions(text):
    transitions = []
    for line in text.strip().split('\n'):
        line = line.strip()
        # Supprimer commentaires et lignes vides
        if not line or line.startswith('#') or line.startswith('//'):
            continue
        # Garder seulement les lignes de chiffres
        if re.match(r'^[\d\s]+$', line):
            values = line.split()
            if len(values) >= 2 and len(values) % 2 == 0:
                transitions.append(values)
    return transitions

# ============================================================
# GÉNÉRER XML TALOS
# ============================================================

def generate_xml(transitions, variables, initial, final):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<instance format="Talos">')
    lines.append('')
    lines.append('<values>')
    lines.append('    <valmatrix id="transitions">')
    for t in transitions:
        lines.append(f"        <data>{' '.join(t)}</data>")
    lines.append('    </valmatrix>')
    lines.append('</values>')
    lines.append('')
    lines.append('<variables>')
    for name, domain in variables:
        lines.append(f'    <var id="{name}" type="int extensional">{" ".join(domain)}</var>')
    var_names = ' '.join(v[0] for v in variables)
    lines.append(f'    <vararray id="state">{var_names}</vararray>')
    lines.append('')
    for i, (name, _) in enumerate(variables):
        lines.append(f'    <var id="i{name}">{initial[i]}</var>')
    init_names = ' '.join(f'i{v[0]}' for v in variables)
    lines.append(f'    <vararray id="initial">{init_names}</vararray>')
    lines.append('')
    for i, (name, _) in enumerate(variables):
        lines.append(f'    <var id="f{name}">{final[i]}</var>')
    final_names = ' '.join(f'f{v[0]}' for v in variables)
    lines.append(f'    <vararray id="final">{final_names}</vararray>')
    lines.append('')
    lines.append('</variables>')
    lines.append('')
    lines.append('</instance>')
    return '\n'.join(lines)

# ============================================================
# EXTRAIRE SOLUTION + DOT
# ============================================================

def extract_first_solution(output):
    for line in output.split('\n'):
        line = line.strip()
        if line.startswith('(') and '|' in line:
            states = re.findall(r'\([^)]*\)', line)
            valid = [s for s in states if re.search(r'[A-Za-z]', s)]
            if valid:
                return valid
    return []

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
    dot.append(f'    step0 [label="Etape 0\\n{solution[0]}", color=green, style=filled, fillcolor=lightgreen];')
    for i in range(1, len(solution)-1):
        dot.append(f'    step{i} [label="Etape {i}\\n{solution[i]}"];')
    last = len(solution)-1
    dot.append(f'    step{last} [label="Etape {last}\\n{solution[last]}", color=blue, style=filled, fillcolor=lightblue];')
    dot.append('')
    for i in range(len(solution)-1):
        dot.append(f'    step{i} -> step{i+1} [color=red, penwidth=3];')
    dot.append("}")
    return "\n".join(dot)

# ============================================================
# MAIN
# ============================================================

print("=" * 60)
print("   LLM PROBLEM SOLVER (via Claude.ai)")
print("=" * 60)

# 1. Description du problème
print("\nEtape 1: Decrivez votre probleme en une ligne:")
problem = input("> ").strip()

# 2. Afficher le prompt à copier dans Claude.ai
prompt = get_prompt(problem)
print("\n" + "=" * 60)
print("Etape 2: COPIEZ ce prompt dans Claude.ai (claude.ai)")
print("=" * 60)
print(prompt)
print("=" * 60)

# 3. Coller la réponse de Claude
print("\nEtape 3: Collez ici la reponse de Claude.ai")
print("(Collez les lignes de transitions, puis tapez FIN sur une ligne seule)")
print()

llm_lines = []
while True:
    line = input()
    if line.strip().upper() == "FIN":
        break
    llm_lines.append(line)

llm_response = '\n'.join(llm_lines)

# 4. Parser les transitions
transitions = parse_transitions(llm_response)
print(f"\n{len(transitions)} transitions extraites.")

if not transitions:
    print("Aucune transition trouvee. Verifiez la reponse de Claude.")
    sys.exit(1)

# 5. Infos variables
print("\nEtape 4: Definissez les variables")
print("Format: NOM val1 val2 ... | NOM val1 val2 ...")
print("Exemple: L 0 1 | C 0 1 | S 0 1 | B 0 1")
var_input = input("> ").strip()

variables = []
for part in var_input.split('|'):
    part = part.strip().split()
    if part:
        variables.append((part[0], part[1:]))

print("\nEtat initial (valeurs separees par espaces):")
initial = input("> ").strip().split()

print("Etat final:")
final = input("> ").strip().split()

print("Nombre max d etapes:")
n_steps = input("> ").strip()

print("Nom du probleme (pour le DOT):")
prob_name = input("> ").strip()

# 6. Générer XML
xml_content = generate_xml(transitions, variables, initial, final)
with open(OUTPUT_XML, "w", encoding="utf-8") as f:
    f.write(xml_content)
print(f"\nXML genere : {OUTPUT_XML}")
print("\nContenu XML:")
print(xml_content)

# 7. Lancer Talos
cmd = [
    "java", "-cp", TALOS_JAR,
    "StateGraph",
    "-n",     n_steps,
    "-print", "1",
    "-file",  OUTPUT_XML
]
print("\nRunning Talos...")
result = subprocess.run(cmd, capture_output=True, text=True)
output = result.stdout
print(output)

# 8. Solution → DOT
solution = extract_first_solution(output)
dot_content = generate_dot(solution, prob_name)
with open(OUTPUT_DOT, "w", encoding="utf-8") as f:
    f.write(dot_content)

print(f"DOT genere : {OUTPUT_DOT}")
if solution:
    print("\nSolution trouvee !")
    for i, s in enumerate(solution):
        print(f"  Etape {i}: {s}")
    print("\nContenu DOT:")
    print(dot_content)
else:
    print("Aucune solution. Augmentez n ou verifiez les transitions.")

print("\nDONE")
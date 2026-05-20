import re
import sys


def parse_dot(file_path):

    transitions = []
    states = set()

    initial_state = None
    final_state = None

    with open(file_path, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            match = re.match(r'"([^"]+)"\s*->\s*"([^"]+)"', line)

            if match:

                s1 = match.group(1).strip()
                s2 = match.group(2).strip()

                transitions.append((s1, s2))

                states.add(s1)
                states.add(s2)

            init_match = re.match(r'"([^"]+)"\s*\[.*color=green.*\]', line)

            if init_match:
                initial_state = init_match.group(1).strip()

            final_match = re.match(r'"([^"]+)"\s*\[.*color=blue.*\]', line)

            if final_match:
                final_state = final_match.group(1).strip()

    states = sorted(list(states))

    state_id = {s: i for i, s in enumerate(states)}

    return transitions, state_id, initial_state, final_state


def dot_to_xml(dot_file, xml_file):

    transitions, state_id, initial_state, final_state = parse_dot(dot_file)

    init_id = state_id[initial_state]
    final_id = state_id[final_state]

    num_states = len(state_id)

    domain = ' '.join(str(i) for i in range(num_states))

    with open(xml_file, "w", encoding="utf-8") as f:

        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<instance format="Talos">\n\n')

        f.write('<values>\n')
        f.write('    <valmatrix id="transitions">\n')

        for s1, s2 in transitions:
            f.write(f'        <data>{state_id[s1]} {state_id[s2]}</data>\n')

        f.write('    </valmatrix>\n')
        f.write('</values>\n\n')

        f.write('<variables>\n')

        f.write(f'    <var id="S" type="int extensional">{domain}</var>\n')

        f.write('    <vararray id="state">S</vararray>\n\n')

        f.write(f'    <var id="iS">{init_id}</var>\n')
        f.write('    <vararray id="initial">iS</vararray>\n\n')

        f.write(f'    <var id="fS">{final_id}</var>\n')
        f.write('    <vararray id="final">fS</vararray>\n')

        f.write('</variables>\n\n')

        f.write('</instance>\n')

    print(f"\n Conversion DONE")
    print(f" DOT  : {dot_file}")
    print(f" XML  : {xml_file}")
    print(f" States      : {num_states}")
    print(f" Transitions : {len(transitions)}")



# MAIN

if len(sys.argv) != 3:

    print("Usage:")
    print("python converter.py input.dot output.xml")

else:

    dot_file = sys.argv[1]
    xml_file = sys.argv[2]

    dot_to_xml(dot_file, xml_file)
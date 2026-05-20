import re
import sys
import os


# =========================================================
# PARSE DOT FILE
# Compatible avec :
# - Loup / Chèvre / Salade
# - Seaux
# - Missionnaires / Cannibales
# =========================================================

def parse_dot(dot_file):

    transitions = []

    states = set()

    initial_state = None
    final_state = None

    with open(dot_file, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            # =================================================
            # TRANSITIONS
            # =================================================

            match = re.match(
                r'"([^"]+)"\s*->\s*"([^"]+)"(?:\s*\[(.*?)\])?',
                line
            )

            if match:

                s1 = match.group(1).strip()
                s2 = match.group(2).strip()

                attrs = match.group(3)

                action = ""

                if attrs:

                    label_match = re.search(
                        r'label\s*=\s*"([^"]+)"',
                        attrs
                    )

                    if label_match:
                        action = label_match.group(1)

                transitions.append((s1, s2, action))

                states.add(s1)
                states.add(s2)

            # =================================================
            # INITIAL STATE
            # =================================================

            init_match = re.match(
                r'"([^"]+)"\s*\[.*color\s*=\s*green.*\]',
                line
            )

            if init_match:
                initial_state = init_match.group(1).strip()

            # =================================================
            # FINAL STATE
            # =================================================

            final_match = re.match(
                r'"([^"]+)"\s*\[.*color\s*=\s*blue.*\]',
                line
            )

            if final_match:
                final_state = final_match.group(1).strip()

    return transitions, states, initial_state, final_state


# =========================================================
# DOT → XML
# =========================================================

def dot_to_xml(dot_file, xml_file):

    transitions, states, initial_state, final_state = parse_dot(dot_file)

    # =====================================================
    # CREATE STATE IDS
    # =====================================================

    states = sorted(list(states))

    state_id = {s: i for i, s in enumerate(states)}

    num_states = len(states)

    domain = ' '.join(str(i) for i in range(num_states))

    # =====================================================
    # CREATE XML
    # =====================================================

    with open(xml_file, "w", encoding="utf-8") as f:

        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')

        f.write('<instance format="Talos">\n\n')

        # =================================================
        # VALUES
        # =================================================

        f.write('<values>\n')

        f.write('    <valmatrix id="transitions">\n')

        for s1, s2, action in transitions:

            f.write(
                f'        <data>{state_id[s1]} {state_id[s2]}</data>\n'
            )

        f.write('    </valmatrix>\n')

        f.write('</values>\n\n')

        # =================================================
        # VARIABLES
        # =================================================

        f.write('<variables>\n')

        # DOMAIN

        f.write(
            f'    <var id="S" type="int extensional">{domain}</var>\n'
        )

        # STATE ARRAY

        f.write(
            '    <vararray id="state">S</vararray>\n\n'
        )

        # INITIAL

        if initial_state:

            init_id = state_id[initial_state]

            f.write(
                f'    <var id="iS">{init_id}</var>\n'
            )

            f.write(
                '    <vararray id="initial">iS</vararray>\n\n'
            )

        # FINAL

        if final_state:

            final_id = state_id[final_state]

            f.write(
                f'    <var id="fS">{final_id}</var>\n'
            )

            f.write(
                '    <vararray id="final">fS</vararray>\n\n'
            )

        f.write('</variables>\n\n')

        f.write('</instance>\n')

    # =====================================================
    # CREATE MAPPING FILE
    # =====================================================

    mapping_file = xml_file.replace(".xml", "_mapping.txt")

    with open(mapping_file, "w", encoding="utf-8") as m:

        m.write("========== STATES MAPPING ==========\n\n")

        for state, idx in state_id.items():

            m.write(f"{idx} = {state}\n")

    # =====================================================
    # PRINT RESULT
    # =====================================================

    print("\n Conversion DONE")
    print(f" DOT FILE      : {dot_file}")
    print(f" XML FILE      : {xml_file}")
    print(f" MAPPING FILE  : {mapping_file}")

    print(f"\n States        : {num_states}")
    print(f" Transitions   : {len(transitions)}")

    if initial_state:
        print(f" Initial State : {initial_state}")

    if final_state:
        print(f" Final State   : {final_state}")


# MAIN


if len(sys.argv) != 3:

    print("\nUsage :")
    print("python converter.py input.dot output.xml")

else:

    dot_file = sys.argv[1]

    xml_file = sys.argv[2]

    if not os.path.exists(dot_file):

        print(f"\n ERROR : File not found -> {dot_file}")

    else:

        dot_to_xml(dot_file, xml_file)
def read_solution(path_file):

    with open(path_file, "r") as f:

        return [line.strip() for line in f if line.strip()]


def highlight_dot(dot_file, solution_file, output_file):

    path = read_solution(solution_file)

    edges = []

    for i in range(len(path)-1):

        edges.append((path[i], path[i+1]))

    with open(dot_file, "r", encoding="utf-8") as f:

        lines = f.readlines()

    new_lines = []

    for line in lines:

        # highlight nodes
        for node in path:

            if f'{node} [' in line:

                if "color=" not in line:

                    line = line.replace(
                        "]",
                        ", color=red, style=filled, fillcolor=yellow]"
                    )

        # highlight edges
        for a, b in edges:

            if f'{a} -> {b}' in line:

                if "[" in line:

                    line = line.replace(
                        "]",
                        ", color=red, penwidth=4]"
                    )

                else:

                    line = line.replace(
                        ";",
                        ' [color=red, penwidth=4];'
                    )

        new_lines.append(line)

    with open(output_file, "w", encoding="utf-8") as f:

        f.writelines(new_lines)

    print("DONE")


highlight_dot(
    "seaux.dot",
    "solution_path.txt",
    "solution_highlighted.dot"
)
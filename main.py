from parser import ReactiveParser
from svelte_compiler import SvelteCompiler


def parse_file(path):
    with open(path, "r", encoding="utf-8") as file:
        source_code = file.read()

    return ReactiveParser(source_code)


if __name__ == "__main__":
    program = parse_file("examples/04_svelte_example.rlang")

    compiler = SvelteCompiler()
    svelte_code = compiler.compile(program)

    with open("GeneratedComponent.svelte", "w", encoding="utf-8") as file:
        file.write(svelte_code)

    print("Svelte komponenta je generirana u GeneratedComponent.svelte")
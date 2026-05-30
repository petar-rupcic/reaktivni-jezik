from pathlib import Path

from parser import ReactiveParser
from svelte_compiler import SvelteCompiler


def compile_file(input_path, output_path):
    """
    Ucitava program napisan u reaktivnom jeziku,
    parsira ga u AST i zatim generira Svelte komponentu.
    """

    # ucitaj izvorni .rlang program
    source_code = Path(input_path).read_text(encoding="utf-8")

    # parsiraj program u AST
    program = ReactiveParser(source_code)

    # prevedi AST u Svelte kod
    compiler = SvelteCompiler()
    svelte_code = compiler.compile(program)

    # spremi generiranu komponentu na disk
    Path(output_path).write_text(svelte_code, encoding="utf-8")

    print(f"Svelte komponenta je generirana: {output_path}")


if __name__ == "__main__":
    # primjer koristenja svelte kompajlera
    compile_file(
        "examples/11_svelte_demo.rlang",
        "GeneratedComponent.svelte"
    )
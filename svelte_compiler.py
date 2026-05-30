from ast_nodes import (
    Program,
    LetStatement,
    ReactiveStatement,
    SetStatement,
    PrintStatement,
    SourceStatement,
    EmitStatement,
    DependenciesStatement,
    TraceStatement,
    NumberLiteral,
    StringLiteral,
    BooleanLiteral,
    VariableExpression,
    BinaryExpression,
)


class SvelteCompiler:
    """
    Prevoditelj iz ReactiveLang AST-a u Svelte komponentu.
    Svaka naredba jezika prevodi se u odgovarajuci Svelte izraz ili HTML element
    """
    def compile(self, program: Program) -> str:
        
        # generirani Svelte <script> dio
        script_lines = []

        # generirani HTML dio
        html_lines = []

        script_lines.append("<script>")

        # obradi svaku AST naredbu i generiraj odgovarajuci Svelte kod
        for statement in program.statements:
            # let - standardna Svelte varijabla
            if isinstance(statement, LetStatement):
                expression = self.compile_expression(statement.expression)
                script_lines.append(f"  let {statement.name} = {expression};")

            # reactive - Svelte reaktivna deklaracija ($:)
            elif isinstance(statement, ReactiveStatement):
                expression = self.compile_expression(statement.expression)
                script_lines.append(f"  $: {statement.name} = {expression};")

            # set - generira funkciju i gumb za promjenu vrijednosti
            elif isinstance(statement, SetStatement):
                expression = self.compile_expression(statement.expression)
                script_lines.append("")
                script_lines.append(f"  function set_{statement.name}() {{")
                script_lines.append(f"    {statement.name} = {expression};")
                script_lines.append("  }")
                html_lines.append(
                    f"<button on:click={{set_{statement.name}}}>Set {statement.name}</button>"
                )

            # print - prikaz vrijednosti u HTML-u
            elif isinstance(statement, PrintStatement):
                expression = self.compile_expression(statement.expression)
                html_lines.append(f"<p>{{{expression}}}</p>")

            # source - simulacija vanjske vrijednosti
            elif isinstance(statement, SourceStatement):
                script_lines.append(f"  let {statement.name} = undefined;")

            # emit - funkcija koja mijenja vrijednost source varijable
            elif isinstance(statement, EmitStatement):
                expression = self.compile_expression(statement.expression)
                script_lines.append("")
                script_lines.append(f"  function emit_{statement.name}() {{")
                script_lines.append(f"    {statement.name} = {expression};")
                script_lines.append("  }")
                html_lines.append(
                    f"<button on:click={{emit_{statement.name}}}>Emit {statement.name}</button>"
                )

            elif isinstance(statement, DependenciesStatement):
                html_lines.append(
                    f"<p>Dependencies for {statement.name} are shown by ReactiveLang runtime.</p>"
                )

            elif isinstance(statement, TraceStatement):
                html_lines.append(
                    f"<p>Trace for {statement.name} is shown by ReactiveLang runtime.</p>"
                )

        script_lines.append("</script>")

        return "\n".join(script_lines) + "\n\n" + "\n".join(html_lines)

    def compile_expression(self, expression) -> str:
        # rekurzivno prevodi AST u Svelte izraz
        if isinstance(expression, NumberLiteral):
            return str(expression.value)

        if isinstance(expression, StringLiteral):
            return f'"{expression.value}"'

        if isinstance(expression, BooleanLiteral):
            return "true" if expression.value else "false"

        if isinstance(expression, VariableExpression):
            return expression.name

        if isinstance(expression, BinaryExpression):
            left = self.compile_expression(expression.left)
            right = self.compile_expression(expression.right)
            return f"({left} {expression.operator} {right})"

        raise TypeError(f"Unknown expression type: {type(expression)}")
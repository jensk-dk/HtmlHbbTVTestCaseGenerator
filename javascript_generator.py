from pathlib import Path
import esprima

class JavaScriptGenerator:
    _function_declaration = 'FunctionDeclaration'
    _arrow_function_expression = 'ArrowFunctionExpression'
    _function_expression = 'FunctionExpression'
    _variable_declaration = 'VariableDeclaration'

    _function_body = 'body'
    _function_type = 'type'

    __required_function_main = 'main'
    __required_function_main = 'tearDown'
    __required_function_main = 'testEnded'



    def load_base(self, testCasePath: Path) -> bool:

        if not (testCasePath / 'base.js').exists():
            return False

        base_javascript = ''

        with open((testCasePath / 'base.js'), 'r') as java_script_file:
            base_javascript = java_script_file.read()

        variables, functions = self.__extract_all_functions_and_variables(base_javascript)
        print(variables)
        print(functions)

        self.__validate_functions(functions, True)



    def __extract_all_functions_and_variables(self, java_script: str) -> (dict[str, str], dict[str, dict[str, str]]):

        parsed = esprima.parseScript(java_script, {'range': True})

        variables: dict[str, str] = {}
        functions: dict[str, dict[str, str]] = {}

        for node in parsed.body:

            if node.type == self._function_declaration:
                func_start, func_end = node.range
                functions[node.id.name] = {self._function_body: java_script[func_start:func_end], self._function_type: self._function_declaration}
            elif node.type == self._variable_declaration:

                start, end = node.range
                is_variable = True
                for declaration in node.declarations:
                    if declaration.init and declaration.init.type in (self._function_expression, self._arrow_function_expression):
                        functions[declaration.id.name] = {self._function_body: java_script[start:end], self._function_type: declaration.init.type}
                        is_variable = False
                        break
                # If we make it to here it is a global variable
                if is_variable:
                    variables[f'{declaration.type} {declaration.id.name}'] = java_script[start:end]
        return variables, functions

    def __validate_functions(self, functions: dict[str, dict[str, str]], is_base: bool=False) -> bool:

        result = True
        if self.__required_function_main in functions:
            self.__validation_succes('Main Function Found')
        else:
            msg = 'Main Function not Found'
            if is_base:
                self.__validation_warning(msg)
            else:
                self.__validation_error(msg)
            result = False
        return result


    def __validation_succes(self, msg: str) -> None:
        print(u' \u2705: ' + msg)

    def __validation_error(self, msg: str) -> None:
        print(u' \u274C: ' + msg)

    def __validation_warning(self, msg: str) -> None:
        print(u' \u26A0: ' + msg)

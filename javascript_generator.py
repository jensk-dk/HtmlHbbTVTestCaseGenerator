from pathlib import Path
import esprima

class JavaScriptGenerator:

    __default_file_name = 'main.js'

    __function_declaration = 'FunctionDeclaration'
    __arrow_function_expression = 'ArrowFunctionExpression'
    __function_expression = 'FunctionExpression'
    __variable_declaration = 'VariableDeclaration'

    __function_body = 'body'
    __function_type = 'type'

    __required_function_main = 'main'
    __required_function_tear_down_name = 'tearDown'
    __required_function_main_name = 'testEnded'


    def generate_main_js_file(self, files: list[Path], output_path: Path) -> bool:

        variables, functions = self.combine_files(files)

        if not self.__validate_functions(functions):
            # TODO: Logging
            print('[Error] Validation failed output file not written')
            return False

        if (not output_path.is_dir() and not output_path.parent.exists()) or (output_path.is_dir() and not output_path.exists()):
            output_path.mkdir()

        if output_path.is_dir():
            output_path = output_path / self.__default_file_name

        with open(output_path, 'w') as main_js_file:
            print(f'[Info] writing to file: {output_path}')
            print('[Info] writing variables')
            for key, variable in variables.items():
                main_js_file.write(f'{variable}\n\n')

            if variables:
                main_js_file.write('\n')

            print('[Info] writing functions')
            for key, function_info in functions.items():
                main_js_file.write(f'{function_info[self.__function_body]}\n\n')
            print(f'[Info] finished writing file: {output_path}')
        return True

    def combine_files(self, files: list[Path]) -> (dict[str, str], dict[str, dict[str, str]]):

        variables: dict[str, str] = {}
        functions: dict[str, dict[str, str]] = {} # The second dict contais code first then function type
        for path in files:
            # TODO: Logging
            print(f'[Info] Processing file: {path}')
            file_variables, file_functions = self.__load_js_file(path)

            print(file_variables)
            for key, value in file_variables.items():
                # We do not allowing for overriding keys of other types
                if key in functions:
                    # TODO: Logging
                    print(f"Key Error: {key} for variable definition {value} exists as a funtion name already")
                elif key in variables:
                    # TODO: use logging
                    print(f'Variable: {key} with definition {variables[key]}\nWill be overriden with defintion {value}')
                    variables[key] = value
                else:
                    variables[key] = value

            for key, value in file_functions.items():

                if key in variables:
                    # TODO: use Logging
                    print(f'Key Error {key} is already defintion as a variable')
                elif key in functions and functions[key][self.__function_type] != value[self.__function_type]:
                    print(f'Key Error: {key} already defines a function but has type {functions[key][self.__function_type]} instead of the expected {file_functions[key][self.__function_type]}')
                else:
                    functions[key] = value
        return variables, functions


    def __load_js_file(self, path: Path) -> (dict[str, str], dict[str, dict[str, str]]):

        if path.exists():
            with open(path, 'r')  as js_file:
                js_code: str = js_file.read()
                return self.__extract_all_functions_and_variables(js_code)
        else:
            print(f'ERROR could not load file: {path}')
            return None, None


    def __extract_all_functions_and_variables(self, java_script: str) -> (dict[str, str], dict[str, dict[str, str]]):

        parsed = esprima.parseScript(java_script, {'range': True})

        variables: dict[str, str] = {}
        functions: dict[str, dict[str, str]] = {}

        for node in parsed.body:
            if node.type == self.__function_declaration:
                func_start, func_end = node.range
                functions[node.id.name] = {self.__function_body: java_script[func_start:func_end], self.__function_type: self.__function_declaration}
            elif node.type == self.__variable_declaration:
                start, end = node.range
                is_variable = True
                for declaration in node.declarations:
                    if declaration.init and declaration.init.type in (self.__function_expression, self.__arrow_function_expression):
                        functions[declaration.id.name] = {self.__function_body: java_script[start:end], self.__function_type: declaration.init.type}
                        is_variable = False
                        break
                # If we make it to here it is a global variable
                if is_variable:
                    variables[f'{declaration.id.name}'] = java_script[start:end]

        return variables, functions

    def __validate_functions(self, functions: dict[str, dict[str, str]]) -> bool:

        print(functions)
        print(self.__required_function_main)
        result = True
        if self.__required_function_main in functions:
            self.__validation_succes('Main Function Found')
        else:
            self.__validation_error('Main Function not Found')
            result = False
        return result


    # TODO: Move to a logging framework
    def __validation_succes(self, msg: str) -> None:
        print(u' \u2705: ' + msg)

    def __validation_error(self, msg: str) -> None:
        print(u' \u274C: ' + msg)

    def __validation_warning(self, msg: str) -> None:
        print(u' \u26A0: ' + msg)

import sys

from source.dsl.InstructionParser import InstructionParser
from source.dsl.OutputParser import OutputParser
from source.dsl.definition_parsers.DefinitionParser import DefinitionParser
from source.environment.EnvironmentSettings import EnvironmentSettings


def generate_docs(docs_path: str):
    DefinitionParser.generate_docs(docs_path)
    InstructionParser.generate_docs(docs_path)
    OutputParser.generate_docs(docs_path)
    print(f"Specification documentation is generated at {docs_path}.")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        path = EnvironmentSettings.specs_docs_path
    generate_docs(path)

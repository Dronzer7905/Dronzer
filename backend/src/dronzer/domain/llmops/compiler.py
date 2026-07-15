from typing import Any

import structlog
from jinja2 import Environment, StrictUndefined, meta
from jinja2.exceptions import TemplateSyntaxError, UndefinedError

logger = structlog.get_logger("dronzer.llmops.compiler")

class PromptCompiler:
    """
    Renders dynamic Prompt Templates using Jinja2 semantics.
    Enforces that all required variables defined in the prompt schema are provided at runtime.
    """

    def __init__(self):
        # StrictUndefined ensures an error is thrown if a variable is missing
        self.env = Environment(undefined=StrictUndefined, autoescape=False)

    def extract_variables(self, template_text: str) -> set:
        """
        Parses the template string and returns a set of all required variable names.
        (e.g., {{ user_name }} -> 'user_name')
        """
        try:
            ast = self.env.parse(template_text)
            return meta.find_undeclared_variables(ast)
        except TemplateSyntaxError as e:
            logger.error("Failed to parse prompt template syntax", error=str(e))
            raise ValueError(f"Invalid Prompt Template Syntax: {str(e)}")

    def render(self, template_text: str, variables: dict[str, Any]) -> str:
        """
        Injects the provided variables into the template and returns the final string to send to the LLM.
        """
        logger.debug("Rendering Prompt Template")
        try:
            template = self.env.from_string(template_text)
            return template.render(**variables)

        except UndefinedError as e:
            logger.error("Missing required prompt variable", error=str(e))
            raise ValueError(f"Prompt Execution Failed: Missing required variable - {str(e)}")

        except Exception as e:
            logger.exception("Unexpected error rendering prompt template", error=str(e))
            raise

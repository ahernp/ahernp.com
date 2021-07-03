from subprocess import Popen, PIPE

from django.db import models
from django.contrib.postgres.search import Value, Func


def run_shell_command(command, cwd):
    p = Popen(command, shell=True, cwd=cwd, stdout=PIPE)
    stdout = p.communicate()[0]
    if stdout:
        stdout = str(stdout.strip(), "utf-8")
    return stdout


class Headline(Func):
    """Show postgresql text search matches in context"""

    function = "ts_headline"

    def __init__(self, field, query, config=None, options=None, **extra):
        expressions = [field, query]
        if config:
            expressions.insert(0, Value(config))
        if options:
            expressions.append(Value(options))
        extra.setdefault("output_field", models.TextField())
        super().__init__(*expressions, **extra)

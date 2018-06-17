from subprocess import Popen, PIPE

from django.conf import settings
from django.views.generic.base import TemplateView

from core.models import Log

# Shell commands: Name and command
SHELL_COMMANDS = [
    ("hostname", "hostname"),
    ("commit", "git log -n 1"),
    ("packages", "pip freeze"),
]

# Flags in settings: Their expected values.
SETTINGS_FLAGS = [("DEBUG", False)]


def run_shell_command(command, cwd):
    p = Popen(command, shell=True, cwd=cwd, stdout=PIPE)
    stdout = p.communicate()[0]
    if stdout:
        stdout = str(stdout.strip(), "utf-8")
    return stdout


def project_state_at_startup():
    data = {}

    cwd = settings.BASE_DIR
    for name, shell_command in SHELL_COMMANDS:
        data[name] = run_shell_command(shell_command, cwd)

    data["settings_flags"] = []
    for name, expected in SETTINGS_FLAGS:
        actual_setting = getattr(settings, name, None)
        data["settings_flags"].append(
            {"name": name, "expected": expected, "actual": actual_setting}
        )
    return data


PROJECT_STATE = project_state_at_startup()


class DashboardView(TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project_state"] = PROJECT_STATE
        entries = Log.objects.all().order_by("-datetime")[
            : settings.LOG_ENTRIES_TO_SHOW
        ]
        context["log_entries"] = entries
        return context

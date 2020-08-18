import os
from invoke import task
from sys import version_info

ROOT_DIR = os.path.dirname(__file__)
PROJ = "src"
TEST_DIR = "tests/"
CHECK_INCLUDES = ("tasks.py", PROJ, TEST_DIR)


@task
def black(context):
    """Run black style checker."""
    if version_info >= (3, 6, 0):
        context.run("black %s" % (" ".join(CHECK_INCLUDES)))


@task
def flake8(context):
    """Run flake8 style checker."""
    context.run("flake8 %s" % (" ".join(CHECK_INCLUDES)))


@task
def pytest(context):
    """Run flake8 style checker."""
    context.run("python -m pytest")

# stdlib
import asyncio  # noqa: F401  # Fixes intermittent error where the import causes a KeyError
import pathlib

pytest_plugins = ("coincidence", "sphinx_toolbox.testing")

repo_root = pathlib.Path(__file__).parent.parent

if not (repo_root / "setup.cfg").is_file():
	(repo_root / "setup.cfg").write_text(
			"""
[mypy]
python_version = 3.8
namespace_packages = True
check_untyped_defs = True
warn_unused_ignores = True
plugins = attr_utils.mypy_plugin
incremental = False
""",
			encoding="UTF-8",
			)

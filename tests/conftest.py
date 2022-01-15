import pathlib

pytest_plugins = ("coincidence", )

repo_root = pathlib.Path(__file__).parent.parent

if not (repo_root / "setup.cfg").is_file():
	(repo_root / "setup.cfg").write_text("""
[mypy]
python_version = 3.6
namespace_packages = True
check_untyped_defs = True
warn_unused_ignores = True
plugins = attr_utils.mypy_plugin
incremental = False
""", encoding="UTF-8")
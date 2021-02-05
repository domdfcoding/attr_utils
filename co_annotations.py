from domdf_python_tools.paths import PathPlus

for file in PathPlus("tests").rglob("**/*.py"):
	print(file)

	content = file.read_lines()
	file.write_lines(["from __future__ import co_annotations", '', *content])

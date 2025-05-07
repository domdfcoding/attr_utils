#  Based on Sphinx
#  Copyright (c) 2007-2020 by the Sphinx team.
#  |  All rights reserved.
#  |
#  |  Redistribution and use in source and binary forms, with or without
#  |  modification, are permitted provided that the following conditions are
#  |  met:
#  |
#  |  * Redistributions of source code must retain the above copyright
#  |    notice, this list of conditions and the following disclaimer.
#  |
#  |  * Redistributions in binary form must reproduce the above copyright
#  |    notice, this list of conditions and the following disclaimer in the
#  |    documentation and/or other materials provided with the distribution.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  |  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  |  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  |  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  |  HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  |  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  |  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  |  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  |  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  |  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  |  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# stdlib
from types import MethodType
from typing import Iterable, Iterator, Optional

# 3rd party
import pytest
from bs4 import BeautifulSoup
from domdf_python_tools.paths import PathPlus
from sphinx.application import Sphinx
from sphinx.testing.path import path
from sphinx.util import logging
from sphinx.util.build_phase import BuildPhase
from sphinx.util.parallel import SerialTasks, parallel_available

try:
	# 3rd party
	from sphinx.util.display import progress_message
except ImportError:
	# 3rd party
	from sphinx.util import progress_message  # type: ignore[no-redef]

pytest_plugins = "sphinx.testing.fixtures"


@pytest.fixture(scope="session")
def rootdir() -> path:
	rdir = PathPlus(__file__).parent.absolute() / "doc-test"
	(rdir / "test-root").maybe_make(parents=True)
	return path(rdir)


# class AppParams(NamedTuple):
# 	args: Sequence[Any]
# 	kwargs: Dict[str, Any]
#
#
# @pytest.fixture()
# def app_params(
# 		request: Any,
# 		test_params: Dict,
# 		sphinx_test_tempdir: path,
# 		rootdir: path,
# 		) -> Tuple[Sequence, Dict]:
# 	"""
# 	parameters that is specified by 'pytest.mark.sphinx' for
# 	sphinx.application.Sphinx initialization
# 	"""
#
# 	# ##### process pytest.mark.sphinx
#
# 	markers = request.node.iter_markers("sphinx")
# 	pargs = {}
# 	kwargs: Dict[str, Any] = {}
#
# 	if markers is not None:
# 		# to avoid stacking positional args
# 		for info in reversed(list(markers)):
# 			for i, a in enumerate(info.args):
# 				pargs[i] = a
# 			kwargs.update(info.kwargs)
#
# 	args = [pargs[i] for i in sorted(pargs.keys())]
#
# 	# ##### prepare Application params
#
# 	testroot = "root"
# 	kwargs["srcdir"] = srcdir = sphinx_test_tempdir / kwargs.get("srcdir", testroot)
#
# 	# special support for sphinx/tests
# 	if rootdir and not srcdir.exists():
# 		testroot_path = rootdir / ("test-" + testroot)
# 		testroot_path.copytree(srcdir)
#
# 	return AppParams(args, kwargs)


@pytest.fixture()
def patched_app(app: Sphinx, monkeypatch) -> Iterable[Sphinx]:

	def build(
			self,
			docnames: Iterable[str],
			summary: Optional[str] = None,
			method: str = "update",
			) -> None:  # NOQA

		# while reading, collect all warnings from docutils
		with logging.pending_warnings():
			updated_docnames = set(self.read())

		for docname in self.env.check_dependents(self.app, updated_docnames):
			updated_docnames.add(docname)

		if updated_docnames:
			# global actions
			self.app.phase = BuildPhase.CONSISTENCY_CHECK
			with progress_message("checking consistency"):
				self.env.check_consistency()
		elif method == "update" and not docnames:
			return

		self.app.phase = BuildPhase.RESOLVING

		# filter "docnames" (list of outdated files) by the updated
		# found_docs of the environment; this will remove docs that
		# have since been removed
		if docnames and docnames != ["__all__"]:
			docnames = set(docnames) & self.env.found_docs

		# determine if we can write in parallel
		if parallel_available and self.app.parallel > 1 and self.allow_parallel:
			self.parallel_ok = self.app.is_parallel_allowed("write")
		else:
			self.parallel_ok = False

		#  create a task executor to use for misc. "finish-up" tasks
		# if self.parallel_ok:
		#     self.finish_tasks = ParallelTasks(self.app.parallel)
		# else:
		# for now, just execute them serially
		self.finish_tasks = SerialTasks()

		# write all "normal" documents (or everything for some builders)
		self.write(docnames, list(updated_docnames), method)

		# finish (write static files etc.)
		self.finish()

		# wait for all tasks
		self.finish_tasks.join()

	monkeypatch.setattr(app.builder, "build", MethodType(build, app.builder))

	yield app


@pytest.fixture()
def page(patched_app: Sphinx, request) -> Iterator[BeautifulSoup]:
	patched_app.build(force_all=True)

	pagename = request.param
	c = (patched_app.outdir / pagename).read_text()

	yield BeautifulSoup(c, "html5lib")

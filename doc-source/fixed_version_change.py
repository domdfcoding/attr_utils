# Based on Sphinx
#
# Copyright (c) 2007-2021 by the Sphinx team.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# stdlib
from typing import Any, Dict, List, Optional, cast

# 3rd party
import sphinx.domains.changeset
from docutils import nodes
from docutils.nodes import Node
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.locale import _

versionlabels = {
		"versionremoved": _("Removed in version %s"),
		**sphinx.domains.changeset.versionlabels,
		}

versionlabel_classes = {
		"versionremoved": "removed",
		**sphinx.domains.changeset.versionlabel_classes,
		}


class VersionChange(sphinx.domains.changeset.VersionChange):
	"""
	Directive to describe a addition/change/deprecation/removal in a specific version.
	"""

	def run(self) -> List[Node]:
		node = addnodes.versionmodified()
		node.document = self.state.document
		self.set_source_info(node)

		node["type"] = self.name
		node["version"] = self.arguments[0]

		text = versionlabels[self.name] % self.arguments[0]

		if len(self.arguments) == 2:
			inodes, messages = self.state.inline_text(self.arguments[1], self.lineno + 1)
			para = nodes.paragraph(self.arguments[1], '', *inodes, translatable=False)
			self.set_source_info(para)
			node.append(para)
		else:
			messages = []

		if self.content:
			self.state.nested_parse(self.content, self.content_offset, node)

		classes = ["versionmodified", versionlabel_classes[self.name]]

		if len(node):
			to_add: Optional[nodes.Node] = None

			if isinstance(node[0], nodes.paragraph) and node[0].rawsource:
				content = nodes.inline(node[0].rawsource, translatable=True)
				content.source = node[0].source
				content.line = node[0].line
				content += node[0].children
				node[0].replace_self(nodes.paragraph('', '', content, translatable=False))

			elif isinstance(node[0], (nodes.bullet_list, nodes.enumerated_list)):
				# Fix for incorrect ordering with bullet lists
				node.insert(0, nodes.compound(''))
				to_add = nodes.paragraph('', '')

			para = cast(nodes.paragraph, node[0])
			para.insert(0, nodes.inline('', f'{text}: ', classes=classes))

			if to_add is not None:
				node.insert(0, to_add)

		else:
			para = nodes.paragraph(
					'',
					'',
					nodes.inline('', f'{text}.', classes=classes),
					translatable=False,
					)
			node.append(para)

		domain = cast(
				sphinx.domains.changeset.ChangeSetDomain,
				self.env.get_domain("changeset"),
				)
		domain.note_changeset(node)

		ret = [node]  # type: List[Node]
		ret += messages
		return ret


def setup(app: "Sphinx") -> Dict[str, Any]:
	app.add_directive("deprecated", VersionChange, override=True)
	app.add_directive("versionadded", VersionChange, override=True)
	app.add_directive("versionchanged", VersionChange, override=True)
	app.add_directive("versionremoved", VersionChange, override=True)

	return {
			"parallel_read_safe": True,
			"parallel_write_safe": True,
			}

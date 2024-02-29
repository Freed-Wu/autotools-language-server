# autotools-language-server

[![readthedocs](https://shields.io/readthedocs/autotools-language-server)](https://autotools-language-server.readthedocs.io)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Freed-Wu/autotools-language-server/main.svg)](https://results.pre-commit.ci/latest/github/Freed-Wu/autotools-language-server/main)
[![github/workflow](https://github.com/Freed-Wu/autotools-language-server/actions/workflows/main.yml/badge.svg)](https://github.com/Freed-Wu/autotools-language-server/actions)
[![codecov](https://codecov.io/gh/Freed-Wu/autotools-language-server/branch/main/graph/badge.svg)](https://codecov.io/gh/Freed-Wu/autotools-language-server)
[![DeepSource](https://deepsource.io/gh/Freed-Wu/autotools-language-server.svg/?show_trend=true)](https://deepsource.io/gh/Freed-Wu/autotools-language-server)

[![github/downloads](https://shields.io/github/downloads/Freed-Wu/autotools-language-server/total)](https://github.com/Freed-Wu/autotools-language-server/releases)
[![github/downloads/latest](https://shields.io/github/downloads/Freed-Wu/autotools-language-server/latest/total)](https://github.com/Freed-Wu/autotools-language-server/releases/latest)
[![github/issues](https://shields.io/github/issues/Freed-Wu/autotools-language-server)](https://github.com/Freed-Wu/autotools-language-server/issues)
[![github/issues-closed](https://shields.io/github/issues-closed/Freed-Wu/autotools-language-server)](https://github.com/Freed-Wu/autotools-language-server/issues?q=is%3Aissue+is%3Aclosed)
[![github/issues-pr](https://shields.io/github/issues-pr/Freed-Wu/autotools-language-server)](https://github.com/Freed-Wu/autotools-language-server/pulls)
[![github/issues-pr-closed](https://shields.io/github/issues-pr-closed/Freed-Wu/autotools-language-server)](https://github.com/Freed-Wu/autotools-language-server/pulls?q=is%3Apr+is%3Aclosed)
[![github/discussions](https://shields.io/github/discussions/Freed-Wu/autotools-language-server)](https://github.com/Freed-Wu/autotools-language-server/discussions)
[![github/milestones](https://shields.io/github/milestones/all/Freed-Wu/autotools-language-server)](https://github.com/Freed-Wu/autotools-language-server/milestones)
[![github/forks](https://shields.io/github/forks/Freed-Wu/autotools-language-server)](https://github.com/Freed-Wu/autotools-language-server/network/members)
[![github/stars](https://shields.io/github/stars/Freed-Wu/autotools-language-server)](https://github.com/Freed-Wu/autotools-language-server/stargazers)
[![github/watchers](https://shields.io/github/watchers/Freed-Wu/autotools-language-server)](https://github.com/Freed-Wu/autotools-language-server/watchers)
[![github/contributors](https://shields.io/github/contributors/Freed-Wu/autotools-language-server)](https://github.com/Freed-Wu/autotools-language-server/graphs/contributors)
[![github/commit-activity](https://shields.io/github/commit-activity/w/Freed-Wu/autotools-language-server)](https://github.com/Freed-Wu/autotools-language-server/graphs/commit-activity)
[![github/last-commit](https://shields.io/github/last-commit/Freed-Wu/autotools-language-server)](https://github.com/Freed-Wu/autotools-language-server/commits)
[![github/release-date](https://shields.io/github/release-date/Freed-Wu/autotools-language-server)](https://github.com/Freed-Wu/autotools-language-server/releases/latest)

[![github/license](https://shields.io/github/license/Freed-Wu/autotools-language-server)](https://github.com/Freed-Wu/autotools-language-server/blob/main/LICENSE)
[![github/languages](https://shields.io/github/languages/count/Freed-Wu/autotools-language-server)](https://github.com/Freed-Wu/autotools-language-server)
[![github/languages/top](https://shields.io/github/languages/top/Freed-Wu/autotools-language-server)](https://github.com/Freed-Wu/autotools-language-server)
[![github/directory-file-count](https://shields.io/github/directory-file-count/Freed-Wu/autotools-language-server)](https://github.com/Freed-Wu/autotools-language-server)
[![github/code-size](https://shields.io/github/languages/code-size/Freed-Wu/autotools-language-server)](https://github.com/Freed-Wu/autotools-language-server)
[![github/repo-size](https://shields.io/github/repo-size/Freed-Wu/autotools-language-server)](https://github.com/Freed-Wu/autotools-language-server)
[![github/v](https://shields.io/github/v/release/Freed-Wu/autotools-language-server)](https://github.com/Freed-Wu/autotools-language-server)

[![pypi/status](https://shields.io/pypi/status/autotools-language-server)](https://pypi.org/project/autotools-language-server/#description)
[![pypi/v](https://shields.io/pypi/v/autotools-language-server)](https://pypi.org/project/autotools-language-server/#history)
[![pypi/downloads](https://shields.io/pypi/dd/autotools-language-server)](https://pypi.org/project/autotools-language-server/#files)
[![pypi/format](https://shields.io/pypi/format/autotools-language-server)](https://pypi.org/project/autotools-language-server/#files)
[![pypi/implementation](https://shields.io/pypi/implementation/autotools-language-server)](https://pypi.org/project/autotools-language-server/#files)
[![pypi/pyversions](https://shields.io/pypi/pyversions/autotools-language-server)](https://pypi.org/project/autotools-language-server/#files)

Language server for
[autotools](https://www.gnu.org/software/automake/manual/html_node/Autotools-Introduction.html).

Supports:

- `configure.ac`: [autoconf](https://www.gnu.org/software/autoconf)
- `Makefile.am`: [automake](https://www.gnu.org/software/automake)
- `Makefile`: [make](https://www.gnu.org/software/make)

Features:

- [x] [Goto Definition](https://microsoft.github.io/language-server-protocol/specifications/specification-current#textDocument_definition)
  - [x] function
  - [x] variable
  - [x] target
- [x] [Find References](https://microsoft.github.io/language-server-protocol/specifications/specification-current#textDocument_references)
  - [x] function
  - [x] variable
  - [x] target
- [x] [Diagnostic](https://microsoft.github.io/language-server-protocol/specifications/specification-current#diagnostic)
- [ ] [Document Formatting](https://microsoft.github.io/language-server-protocol/specifications/specification-current#textDocument_formatting)
- [x] [Hover](https://microsoft.github.io/language-server-protocol/specifications/specification-current#textDocument_hover)
  - [x] definition
  - [x] document
- [x] [Completion](https://microsoft.github.io/language-server-protocol/specifications/specification-current#textDocument_completion)
  - [ ] definition
  - [x] document

Other features:

- [x] [pre-commit-hooks](https://pre-commit.com/)
  - [x] linter
  - [ ] formatter

## Screenshots

### Diagnostic

![diagnostic](https://github.com/Freed-Wu/autotools-language-server/assets/32936898/a1b35e66-7046-42e0-8db8-b636e711764d)

### Hover

![document hover](https://github.com/Freed-Wu/autotools-language-server/assets/32936898/c39c08fd-3c8e-474d-99f4-e9f919f4da37)

### Completion

![completion](https://github.com/SchemaStore/schemastore/assets/32936898/fa0c523d-cb51-4870-92a4-07d64c624221)

## How Does It Work

See [here](https://github.com/neomutt/lsp-tree-sitter#usage).

Read
[![readthedocs](https://shields.io/readthedocs/autotools-language-server)](https://autotools-language-server.readthedocs.io)
to know more.

## Similar Projects

- [cmake-language-server](https://github.com/regen100/cmake-language-server)

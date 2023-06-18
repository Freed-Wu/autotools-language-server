# autoconf-language-server

[![readthedocs](https://shields.io/readthedocs/autoconf-language-server)](https://autoconf-language-server.readthedocs.io)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Freed-Wu/autoconf-language-server/main.svg)](https://results.pre-commit.ci/latest/github/Freed-Wu/autoconf-language-server/main)
[![github/workflow](https://github.com/Freed-Wu/autoconf-language-server/actions/workflows/main.yml/badge.svg)](https://github.com/Freed-Wu/autoconf-language-server/actions)
[![codecov](https://codecov.io/gh/Freed-Wu/autoconf-language-server/branch/main/graph/badge.svg)](https://codecov.io/gh/Freed-Wu/autoconf-language-server)
[![DeepSource](https://deepsource.io/gh/Freed-Wu/autoconf-language-server.svg/?show_trend=true)](https://deepsource.io/gh/Freed-Wu/autoconf-language-server)

[![github/downloads](https://shields.io/github/downloads/Freed-Wu/autoconf-language-server/total)](https://github.com/Freed-Wu/autoconf-language-server/releases)
[![github/downloads/latest](https://shields.io/github/downloads/Freed-Wu/autoconf-language-server/latest/total)](https://github.com/Freed-Wu/autoconf-language-server/releases/latest)
[![github/issues](https://shields.io/github/issues/Freed-Wu/autoconf-language-server)](https://github.com/Freed-Wu/autoconf-language-server/issues)
[![github/issues-closed](https://shields.io/github/issues-closed/Freed-Wu/autoconf-language-server)](https://github.com/Freed-Wu/autoconf-language-server/issues?q=is%3Aissue+is%3Aclosed)
[![github/issues-pr](https://shields.io/github/issues-pr/Freed-Wu/autoconf-language-server)](https://github.com/Freed-Wu/autoconf-language-server/pulls)
[![github/issues-pr-closed](https://shields.io/github/issues-pr-closed/Freed-Wu/autoconf-language-server)](https://github.com/Freed-Wu/autoconf-language-server/pulls?q=is%3Apr+is%3Aclosed)
[![github/discussions](https://shields.io/github/discussions/Freed-Wu/autoconf-language-server)](https://github.com/Freed-Wu/autoconf-language-server/discussions)
[![github/milestones](https://shields.io/github/milestones/all/Freed-Wu/autoconf-language-server)](https://github.com/Freed-Wu/autoconf-language-server/milestones)
[![github/forks](https://shields.io/github/forks/Freed-Wu/autoconf-language-server)](https://github.com/Freed-Wu/autoconf-language-server/network/members)
[![github/stars](https://shields.io/github/stars/Freed-Wu/autoconf-language-server)](https://github.com/Freed-Wu/autoconf-language-server/stargazers)
[![github/watchers](https://shields.io/github/watchers/Freed-Wu/autoconf-language-server)](https://github.com/Freed-Wu/autoconf-language-server/watchers)
[![github/contributors](https://shields.io/github/contributors/Freed-Wu/autoconf-language-server)](https://github.com/Freed-Wu/autoconf-language-server/graphs/contributors)
[![github/commit-activity](https://shields.io/github/commit-activity/w/Freed-Wu/autoconf-language-server)](https://github.com/Freed-Wu/autoconf-language-server/graphs/commit-activity)
[![github/last-commit](https://shields.io/github/last-commit/Freed-Wu/autoconf-language-server)](https://github.com/Freed-Wu/autoconf-language-server/commits)
[![github/release-date](https://shields.io/github/release-date/Freed-Wu/autoconf-language-server)](https://github.com/Freed-Wu/autoconf-language-server/releases/latest)

[![github/license](https://shields.io/github/license/Freed-Wu/autoconf-language-server)](https://github.com/Freed-Wu/autoconf-language-server/blob/main/LICENSE)
[![github/languages](https://shields.io/github/languages/count/Freed-Wu/autoconf-language-server)](https://github.com/Freed-Wu/autoconf-language-server)
[![github/languages/top](https://shields.io/github/languages/top/Freed-Wu/autoconf-language-server)](https://github.com/Freed-Wu/autoconf-language-server)
[![github/directory-file-count](https://shields.io/github/directory-file-count/Freed-Wu/autoconf-language-server)](https://github.com/Freed-Wu/autoconf-language-server)
[![github/code-size](https://shields.io/github/languages/code-size/Freed-Wu/autoconf-language-server)](https://github.com/Freed-Wu/autoconf-language-server)
[![github/repo-size](https://shields.io/github/repo-size/Freed-Wu/autoconf-language-server)](https://github.com/Freed-Wu/autoconf-language-server)
[![github/v](https://shields.io/github/v/release/Freed-Wu/autoconf-language-server)](https://github.com/Freed-Wu/autoconf-language-server)

[![pypi/status](https://shields.io/pypi/status/autoconf-language-server)](https://pypi.org/project/autoconf-language-server/#description)
[![pypi/v](https://shields.io/pypi/v/autoconf-language-server)](https://pypi.org/project/autoconf-language-server/#history)
[![pypi/downloads](https://shields.io/pypi/dd/autoconf-language-server)](https://pypi.org/project/autoconf-language-server/#files)
[![pypi/format](https://shields.io/pypi/format/autoconf-language-server)](https://pypi.org/project/autoconf-language-server/#files)
[![pypi/implementation](https://shields.io/pypi/implementation/autoconf-language-server)](https://pypi.org/project/autoconf-language-server/#files)
[![pypi/pyversions](https://shields.io/pypi/pyversions/autoconf-language-server)](https://pypi.org/project/autoconf-language-server/#files)

Language server for [autoconf](https://www.gnu.org/software/autoconf).

- [x] document hover
- [x] completion

![document hover](https://github.com/SchemaStore/schemastore/assets/32936898/d8a2cdf1-d62b-46f4-87a9-12701ab660a6)

![completion](https://github.com/SchemaStore/schemastore/assets/32936898/fa0c523d-cb51-4870-92a4-07d64c624221)

## Usage

### vim

Install [coc.nvim](https://github.com/neoclide/coc.nvim):

```json
{
  "languageserver": {
    "autoconf": {
      "command": "autoconf-language-server",
      "filetypes": [
        "config"
      ],
      "initializationOptions": {
        "method": "builtin"
      }
    }
  }
}
```

### neovim

Install [nvim-lspconfig](https://github.com/neovim/nvim-lspconfig):

```vim
if executable('autoconf-language-server')
  augroup lsp
    autocmd!
    autocmd User lsp_setup call lsp#register_server({
          \ 'name': 'autoconf',
          \ 'cmd': {server_info->['autoconf-language-server']},
          \ 'whitelist': ['config'],
          \ 'initialization_options': {
          \   'method': 'builtin',
          \ },
          \ })
  augroup END
endif
```

## Customization

See
<https://autoconf-language-server.readthedocs.io/en/latest/api/autoconf-language-server.html#autoconf_language_server.server.get_document>.

## Similar Projects

- [cmake-language-server](https://github.com/regen100/cmake-language-server)

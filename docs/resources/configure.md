# Configure

See customization in
<https://autotools-language-server.readthedocs.io/en/latest/api/autotools-language-server.html#autotools_language_server.server.get_document>.

## (Neo)[Vim](https://www.vim.org)

### [coc.nvim](https://github.com/neoclide/coc.nvim)

```json
{
  "languageserver": {
    "autotools": {
      "command": "autotools-language-server",
      "filetypes": [
        "config",
        "make",
        "automake"
      ],
      "initializationOptions": {
        "method": "builtin"
      }
    }
  }
}
```

### [vim-lsp](https://github.com/prabirshrestha/vim-lsp)

```vim
if executable('autotools-language-server')
  augroup lsp
    autocmd!
    autocmd User lsp_setup call lsp#register_server({
          \ 'name': 'autotools',
          \ 'cmd': {server_info->['autotools-language-server']},
          \ 'whitelist': ['config', 'make', 'automake'],
          \ 'initialization_options': {
          \   'method': 'builtin',
          \ },
          \ })
  augroup END
endif
```

## [Neovim](https://neovim.io)

```lua
vim.api.nvim_create_autocmd({ "BufEnter" }, {
  pattern = { "configure.ac", "Makefile*", "*.mk" },
  callback = function()
    vim.lsp.start({
      name = "autotools",
      cmd = { "autotools-language-server" }
    })
  end,
})
```

## [Emacs](https://www.gnu.org/software/emacs)

```elisp
(make-lsp-client :new-connection
(lsp-stdio-connection
  `(,(executable-find "autotools-language-server")))
  :activation-fn (lsp-activate-on "configure.ac" "Makefile*" "*.mk")
  :server-id "autotools")))
```

## [Sublime](https://www.sublimetext.com)

```json
{
  "clients": {
    "autotools": {
      "command": [
        "autotools-language-server"
      ],
      "enabled": true,
      "selector": "source.autotools"
    }
  }
}
```

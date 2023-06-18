# Configure

See customization in
<https://autoconf-language-server.readthedocs.io/en/latest/api/autoconf-language-server.html#autoconf_language_server.server.get_document>.

## (Neo)[Vim](https://www.vim.org)

### [coc.nvim](https://github.com/neoclide/coc.nvim)

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

### [vim-lsp](https://github.com/prabirshrestha/vim-lsp)

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

## [Neovim](https://neovim.io)

```lua
vim.api.nvim_create_autocmd({ "BufEnter" }, {
  pattern = { "configure.ac" },
  callback = function()
    vim.lsp.start({
      name = "autoconf",
      cmd = { "autoconf-language-server" }
    })
  end,
})
```

## [Emacs](https://www.gnu.org/software/emacs)

```elisp
(make-lsp-client :new-connection
(lsp-stdio-connection
  `(,(executable-find "autoconf-language-server")))
  :activation-fn (lsp-activate-on "configure.ac")
  :server-id "autoconf")))
```

## [Sublime](https://www.sublimetext.com)

```json
{
  "clients": {
    "autoconf": {
      "command": [
        "autoconf-language-server"
      ],
      "enabled": true,
      "selector": "source.autoconf"
    }
  }
}
```

# Configure

- For windows, change `~/.config` to `~/AppData/Local`
- For macOS, change `~/.config` to `~/Library`

## (Neo)[Vim](https://www.vim.org)

For vim:

- Change `~/.config/nvim` to `~/.vim`
- Change `init.vim` to `vimrc`

### [coc.nvim](https://github.com/neoclide/coc.nvim)

`~/.config/nvim/coc-settings.json`:

```json
{
  "languageserver": {
    "config": {
      "command": "autoconf-language-server",
      "filetypes": [
        "config"
      ]
    },
    "make": {
      "command": "make-language-server",
      "filetypes": [
        "make"
      ]
    }
  }
}
```

### [vim-lsp](https://github.com/prabirshrestha/vim-lsp)

`~/.config/nvim/init.vim`:

```vim
if executable('autoconf-language-server')
  augroup lsp
    autocmd!
    autocmd User lsp_setup call lsp#register_server({
          \ 'name': 'config',
          \ 'cmd': {server_info->['autoconf-language-server']},
          \ 'whitelist': ['config'],
          \ })
  augroup END
endif
if executable('make-language-server')
  augroup lsp
    autocmd!
    autocmd User lsp_setup call lsp#register_server({
          \ 'name': 'make',
          \ 'cmd': {server_info->['make-language-server']},
          \ 'whitelist': ['make'],
          \ })
  augroup END
endif
```

## [Neovim](https://neovim.io)

`~/.config/nvim/init.lua`:

```lua
vim.api.nvim_create_autocmd({ "BufEnter" }, {
  pattern = { "configure.ac" },
  callback = function()
    vim.lsp.start({
      name = "config",
      cmd = { "config-language-server" }
    })
  end,
})
vim.api.nvim_create_autocmd({ "BufEnter" }, {
  pattern = { "Makefile.am", "Makefile" },
  callback = function()
    vim.lsp.start({
      name = "make",
      cmd = { "make-language-server" }
    })
  end,
})
```

## [Emacs](https://www.gnu.org/software/emacs)

`~/.emacs.d/init.el`:

```lisp
(make-lsp-client :new-connection
(lsp-stdio-connection
  `(,(executable-find "autoconf-language-server")))
  :activation-fn (lsp-activate-on "configure.ac")
  :server-id "config")))
(make-lsp-client :new-connection
(lsp-stdio-connection
  `(,(executable-find "make-language-server")))
  :activation-fn (lsp-activate-on "Makefile.am" "Makefile")
  :server-id "make")))
```

## [Helix](https://helix-editor.com/)

`~/.config/helix/languages.toml`:

```toml
[[language]]
name = "autoconf"
language-servers = [ "autoconf-language-server",]

[[language]]
name = "make"
language-servers = [ "make-language-server",]

[language_server.autoconf-language-server]
command = "autoconf-language-server"

[language_server.make-language-server]
command = "make-language-server"
```

## [KaKoune](https://kakoune.org/)

### [kak-lsp](https://github.com/kak-lsp/kak-lsp)

`~/.config/kak-lsp/kak-lsp.toml`:

```toml
[language_server.autoconf-language-server]
filetypes = [ "autoconf",]
command = "autoconf-language-server"

[language_server.make-language-server]
filetypes = [ "make",]
command = "make-language-server"
```

## [Sublime](https://www.sublimetext.com)

`~/.config/sublime-text-3/Packages/Preferences.sublime-settings`:

```json
{
  "clients": {
    "autoconf": {
      "command": [
        "autoconf-language-server"
      ],
      "enabled": true,
      "selector": "source.autoconf"
    },
    "make": {
      "command": [
        "make-language-server"
      ],
      "enabled": true,
      "selector": "source.make"
    }
  }
}
```

## [Visual Studio Code](https://code.visualstudio.com/)

[An official support of generic LSP client is pending](https://github.com/microsoft/vscode/issues/137885).

### [vscode-glspc](https://gitlab.com/ruilvo/vscode-glspc)

`~/.config/Code/User/settings.json`:

```json
{
  "glspc.serverPath": "make-language-server",
  "glspc.languageId": "make"
}
```

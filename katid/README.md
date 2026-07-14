# katid

A language server for Makefile.

## Features

- [ ] cache: once a Makefile is changed, clear
  `MakefileCacheManager._cache.find(filename)`
- [ ] builtin Makefile: provide the definition for `MAKE`, `CC`, ...

## Build

```sh
xmake -y
```

## Related Projects

- [make-lsp-server](https://github.com/alexclewontin/make-lsp-vscode/blob/master/server/package.json):
  the earliest language server for Makefile. Use regular expression. Written in
  javascript.
- [autotools-language-server](https://github.com/Freed-Wu/autotools-language-server)
  Use tree-sitter. Written in python. Also support autoconf.

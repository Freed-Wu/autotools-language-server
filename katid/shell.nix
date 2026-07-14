{ pkgs ? import <nixpkgs> { } }:

with pkgs;
mkShell {
  name = "katid";
  buildInputs = [
    xmake
    pkg-config

    # kati
    git

    # lsp-framework
    cmake
    ninja
    curl
    gnutar
    gzip
  ];
}

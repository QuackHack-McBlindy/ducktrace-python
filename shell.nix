{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python312
    python312Packages.setuptools
    python312Packages.wheel
    python312Packages.build
    python312Packages.twine
    
  ];}

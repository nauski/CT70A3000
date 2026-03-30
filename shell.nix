{ pkgs ? import <nixpkgs> {} }:

let
  python = pkgs.python312.withPackages (ps: [
    ps.pillow
    ps.tkinter
  ]);
in
pkgs.mkShell {
  packages = [ python ];

  shellHook = ''
    echo "Inventory Management System dev shell"
    echo "Run: python dashboard.py"
  '';
}

{
  description = "ducktrace-python – duck‑themed logging for Python";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python312;
      in {
        packages.default = python.pkgs.buildPythonPackage {
          pname = "ducktrace";
          version = "0.1.0";
          src = ./.;
          format = "pyproject";

          nativeBuildInputs = with python.pkgs; [ setuptools wheel ];

          propagatedBuildInputs = [ ];

          meta = with pkgs.lib; {
            description = "A duck‑themed logging system for Python";
            homepage = "https://github.com/QuackHack-McBlindy/ducktrace-python";
            license = licenses.mit;
            maintainers = with maintainers; [ QuackHack-McBlindy ];
          };
        };

        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python312
            python312Packages.setuptools
            python312Packages.wheel
          ];
        };
        
      });}

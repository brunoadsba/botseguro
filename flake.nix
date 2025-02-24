{
  description = "Ambiente de desenvolvimento para um chatbot Flask";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          python311
          python311Packages.pip
          python311Packages.flask
          python311Packages.fuzzywuzzy
          python311Packages.python-levenshtein
        ];
        shellHook = ''
          export PYTHONNOUSERSITE=1
          export PIP_DISABLE_PIP_VERSION_CHECK=1
          export PYTHONPATH=$PWD/.venv/lib/python3.11/site-packages:$PYTHONPATH
          mkdir -p .venv/lib/python3.11/site-packages
          pip install -r requirements.txt --target=.venv/lib/python3.11/site-packages
        '';
      };
    };
}
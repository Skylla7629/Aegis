{
  description = "development shell for aegis prototype";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = {nixpkgs, ...}: let
    system = "x86_64-linux";

    pkgs = import nixpkgs {
      inherit system;
      config.allowUnfree = true;
    };
  in {
    devShells.${system} = {
      default = pkgs.mkShell {
        buildInputs = [
          pkgs.python313
          pkgs.uv
        ];

        name = "devShell for Aegis-py";

        shellHook = ''
          echo "the blazingly fast private mesenger (in deveopment!)"
        '';
      };
    };
  };
}

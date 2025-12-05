{
  descprition = "development shell for aegis prototype";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = {nixpkgs}: let
    system = "x86_64-linux";

    pkgs = import nixpkgs {
      inherit system;
      config.allowUnfree = true;
    };
  in {
    devShells.${system} = {
      aegis = pkgs.mkShell {
        name = "devShell for Aegis-py";

        packages = with pkgs; [
          python313
          uv
        ];

        shellHook = ''
          echo "the blazingly fast private mesenger (in deveopment!)"
        '';
      };
    };
  };
}

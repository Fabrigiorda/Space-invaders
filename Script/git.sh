git config --global --unset user.name
git config --global --unset user.email
git config --global --unset user.password
git config --global --unset credential.helper
cmdkey /delete:LegacyGeneric:target=git:https://github.com

git config --global --replace-all user.name "Fabrigiorda"
git config --global --replace-all user.email "fgiordanelli@alumno.huergo.edu.ar"

#!/usr/bin/env bash
set -e

current_version=$(grep '^version =' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
echo "Current version: $current_version"

IFS='.' read -r major minor patch <<< "$current_version"
new_patch=$((patch + 1))
new_version="$major.$minor.$new_patch"
echo "New version: $new_version"

sed -i.bak "s/^version = \".*\"/version = \"$new_version\"/" pyproject.toml
rm pyproject.toml.bak
echo "Updated pyproject.toml"

if [ -f "flake.nix" ]; then
    sed -i.bak "s/version = \".*\";/version = \"$new_version\";/" flake.nix
    rm flake.nix.bak
    echo "Updated flake.nix"
fi

git add pyproject.toml
[ -f "flake.nix" ] && git add flake.nix

git commit -m "Bump version to $new_version"
git tag "v$new_version"

git push origin main --tags

echo "Released version $new_version"

set shell := ["zsh", "-uc"]
set positional-arguments

# List all available recipes
help:
  @just --list

# +-------------------+
# | SETUP AND CI/CD   |
# +-------------------+

# Install dependencies and pre-commit hooks
install: ensure-repo
  #! /usr/bin/env zsh
  {{just_executable()}} needs pdm grep gh

  pdm install --dev --group=:all
  pdm run pre-commit install --install-hooks
  pdm run nbstripout --install

  if ! gh secret list | grep --quiet PERSONAL_ACCESS_TOKEN; then
    print "\nTo run CI/CD workflows, you need to set the PERSONAL_ACCESS_TOKEN with:"
    print "just config-ci <token>"
    print "or manually with:"
    print "gh secret set PERSONAL_ACCESS_TOKEN --body=<token> --app=actions"
    print "⚠️ Do not pass the token as plain text, or it will persist in your shell history!"
  fi

# Set the secret token to run CI/CD workflows
@config-ci password:
  {{just_executable()}} needs gh

  gh secret set PERSONAL_ACCESS_TOKEN --body={{password}} --app=actions

# Configure PyPI credentials to release the package (works in CI/CD too)
@config-pypi password:
  {{just_executable()}} needs pdm

  pdm config --local repository.pypi.url https://upload.pypi.org/legacy/
  pdm config --local repository.pypi.username __token__
  pdm config --local repository.pypi.password {{password}}

  gh secret set PDM_PUBLISH_REPO --body="https://upload.pypi.org/legacy/" --app=actions
  gh secret set PDM_PUBLISH_USERNAME --body="__token__" --app=actions
  gh secret set PDM_PUBLISH_PASSWORD --body="$(pdm config --local repository.pypi.password)" --app=actions

# Configure TestPyPI to test the release process (locally only)
@config-testpypi password:
  {{just_executable()}} needs pdm

  pdm config --local repository.testpypi.url https://test.pypi.org/legacy/
  pdm config --local repository.testpypi.username __token__
  pdm config --local repository.testpypi.password {{password}}

# Lock dependencies
@lock:
  {{just_executable()}} needs pdm

  pdm lock --dev --group=:all

# Update dependencies and update pre-commit hooks
update: lock
  pdm update
  pdm run pre-commit install-hooks
  pdm run pre-commit autoupdate

# +-------------------+
# | DEVELOPMENT TOOLS |
# +-------------------+

# Format code with black and isort
@fmt:
  pdm run black -- src tests
  pdm run blacken-docs -- src/**/*.py tests/*.py
  pdm run ruff --select=I001 --fix -- src tests

# Lint the project with Ruff
@lint:
  pdm run ruff -- src tests

# Perform static type checking with mypy
@typecheck:
  pdm run mypy -- src tests

# Audit dependencies with pip-audit
@audit:
  pdm run pip-audit
  pdm run deptry -- src

# Format, lint and typecheck the project
@sanitise: fmt lint typecheck

alias sanitize := sanitise

# Check the version can be bumped without errors
@test-bump: check-commits
  pdm run cz bump --dry-run

# Bump the version
@bump: test-bump
  pdm run cz bump

# Test the release workflow
test-release: sanitise audit test-bump

# Release a new version
release: sanitise audit bump
  git push
  git push --tag

# Publish the package to GemFury
@test-publish:
  {{just_executable()}} check-repository testpypi
  pdm publish --repository=testpypi

# Publish the package to GemFury
@publish:
  {{just_executable()}} check-repository pypi
  pdm publish --repository=pypi

# Run all tests
test:
  pdm run pytest --cov=src/makemore --cov-report=term-missing --cov-report=html

# Live preview the documentation
preview-docs:
  pdm run mike serve --config-file=docs/mkdocs.yml

# +-------------------+
# | UTILITIES         |
# +-------------------+

# Launch a jupyter instance
@lab:
  pdm run jupyter lab

# Commit with conventional commits
@commit: check-commits
  pdm run cz commit

alias c := commit

# Export production dependencies to requirements.txt
@export:
  pdm export --prod -f=requirements > requirements.txt
  pdm export --no-default --dev -f=requirements > requirements-dev.txt

# +-------------------+
# | INTERNALS         |
# +-------------------+

# Assert a command is available
[private]
needs *commands:
  #!/usr/bin/env zsh
  set -euo pipefail
  for cmd in "$@"; do
    if ! command -v $cmd &> /dev/null; then
      print "$cmd binary not found. Did you forget to install it?"
      exit 1
    fi
  done

# Check whether the commit messages follow the conventional commit format
[private]
check-commits:
  #! /usr/bin/env zsh
  set -euo pipefail

  local revs
  revs=($(git rev-list origin/main..HEAD))

  if [[ $#revs -eq 0 ]]; then
    print "No commits to check."
    exit 0
  else
    pdm run cz check --rev-range origin/main..HEAD
  fi

# Check a publishing repo is configured
[private]
check-repository *repos:
  #!/usr/bin/env zsh
  for repo in "$@"; do
    local configs
    configs=($(pdm config repository.$repo)) 2>/dev/null
    if [[ $#configs -eq 0 ]]; then
      print "\nNo repository $repo found."
      print "pdm config repository.$repo.url <url>"
      print "pdm config repository.$repo.username <username>"
      print "pdm config repository.$repo.password <password>"
      exit 1
    fi
  done

# Ensure that the remote repo exists
[private]
ensure-repo:
  #! /usr/bin/env zsh
  if ! [[ -d .git ]]; then
    git init
  fi

  if ! gh repo list baggiponte | grep --quiet makemore ; then
    while true; do
      print -n "No remote repository found. Do you want to create a new repository? (y/n): "
      read -r REPLY

      case $REPLY in
        [Yy])
          print -n "Do you want to create a private repository? (y/n): "
          read -r PRIVATE
          case $PRIVATE in
            [Yy])
              gh repo create baggiponte/makemore --private --source=.
              ;;
            [Nn])
              gh repo create baggiponte/makemore --public --source=.
              ;;
            *)
              print "Invalid input. Please enter 'y' or 'n'."
              ;;
          esac
          break
          ;;
        [Nn])
          exit 0
          ;;
        *)
          print "Invalid input. Please enter 'y' or 'n'."
          ;;
      esac
    done
  elif ! git remote get-url origin 1>/dev/null; then
    while true; do
      read -r "A repo with this name already exists. Do you want to add it as a remote? (y/n): " REPLY

      case $REPLY in
        [Yy])
          git remote add origin git@github.com:baggiponte/makemore
          break
          ;;
        [Nn])
          exit 0
          ;;
        *)
          print "Invalid input. Please enter 'y' or 'n'."
          ;;
      esac
    done
  fi

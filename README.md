# Migrate env secrets between CI providers

Created mostly to import from Travis to GitHub Actions due to
<https://www.jeffgeerling.com/blog/2020/travis-cis-new-pricing-plan-threw-wrench-my-open-source-works>

For example, add an API token with `repo` scope to Travis settings
under the env var `GH_SECRETS_TOKEN`, then replace `.travis.yml` with:

```yaml
language: python
jobs:
  include:
  - name: migrate
    python: 3.7
install:
- git clone https://github.com/casperdcl/ci-env-migrate
- pip install -r ci-env-migrate/requirements.txt
script:
- python ci-env-migrate/gh.py $TRAVIS_REPO_SLUG "SOMEVAR=$SOMEVAR"
```

## Install

```sh
git clone https://github.com/casperdcl/ci-env-migrate
pip3 install -r ci-env-migrate/requirements.txt
```

## Usage

```sh
# to Github Actions
python3 ci-env-migrate/gh.py owner/repo SOMEVAR=secret
```

`$GH_SECRETS_TOKEN` must be present and have `repo` scope.

```
Usage:
  gh.py [options] <repo> [<secrets>...]

Arguments:
  <repo>  : Repo slug (e.g. casperdcl/test)
  <secrets>  : Secrets (e.g. SOMEVAR=private)

Options:
  -t TOKEN, --token TOKEN  : If unspecified, use `$GH_SECRETS_TOKEN`
  -f FILE, --env-file FILE  : file containing <secrets> (one per line)
  -v, --verbose  : Debug logging
```

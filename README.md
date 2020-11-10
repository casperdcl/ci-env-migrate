# Migrate env secrets between CI providers

Created mostly to import from Travis to GitHub Actions due to
<https://www.jeffgeerling.com/blog/2020/travis-cis-new-pricing-plan-threw-wrench-my-open-source-works>

## Install

```sh
git clone https://github.com/casperdcl/ci-env-migrate
pip3 install -r ci-env-migrate/requirements.txt
```

## Usage

```sh
# to Github Actions
python3 ci-env-migrate/gh.py --token $GH_SECRETS_TOKEN owner/repo SOMEVAR=secret
```

Note that `--token` is optional if `$GH_SECRETS_TOKEN` is present in the current env.
The token must have `repo` scope.

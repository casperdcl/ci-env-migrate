#!/usr/bin/env python3
"""
Usage:
  gh [options] <repo> [<secrets>...]

Arguments:
  <repo>  : Repo slug (e.g. casperdcl/test)
  <secrets>  : Secrets (e.g. SOMEVAR=private)

Options:
  -t TOKEN, --token TOKEN  : If unspecified, use `$GH_SECRETS_TOKEN`
  -f FILE, --env-file FILE  : file containing <secrets> (one per line)
  -v, --verbose  : Debug logging
"""
from argopt import argopt
from base64 import b64encode
from nacl import encoding, public
import logging
import os
import requests

API = "https://api.github.com"
SUCCESS = {201: "Created", 204: "Updated"}
log = logging.getLogger("gh")


def encrypt(public_key: str, secret_value: str) -> str:
    """
    Encrypt a Unicode string using the public key
    https://developer.github.com/v3/actions/secrets/#example-encrypting-a-secret-using-python
    """
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")


def get_public_key(owner, repo, token):
    res = requests.get(
        f"{API}/repos/{owner}/{repo}/actions/secrets/public-key",
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        },
    )
    res = res.json()
    return res["key_id"], res["key"]


def put_secrets(owner, repo, token, **secrets):
    key_id, key = get_public_key(owner, repo, token)
    for k, v in secrets.items():
        log.info("variable %s", k)
        log.debug("setting '%s' to '%s'", k, v)
        data = {"encrypted_value": encrypt(key, v), "key_id": key_id}
        log.debug(data)
        res = requests.put(
            f"{API}/repos/{owner}/{repo}/actions/secrets/{k}",
            json=data,
            headers={
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json",
            },
        )
        if res.status_code not in SUCCESS:
            log.warn("%s: %s", res, res.json())
        else:
            log.info(SUCCESS[res.status_code])


if __name__ == "__main__":
    args = argopt(__doc__).parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    token = args.token or os.getenv("GH_SECRETS_TOKEN")
    owner, repo = args.repo.split("/")
    if args.env_file:
        with open(args.env_file) as fd:
            secrets = dict(i.split("=", 1) for i in fd.readlines())
    else:
        secrets = {}
    secrets.update(i.split("=", 1) for i in args.secrets)
    put_secrets(owner, repo, token, **secrets)

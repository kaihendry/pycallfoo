Exercise https://github.com/kaihendry/pyunderstand

## pyunderstand ref resolution

The workflow determines which ref to checkout from pyunderstand in this order:

1. Manual override via `workflow_dispatch` input
2. Matching branch name (if current branch exists in pyunderstand)
3. `version` field from `config.yaml`
4. Default branch

https://discord.com/channels/1039017663004942429/1388197295387840552/1392105578649878611

    so ... (learned this the hard way) ...

    you need to have the deps in pyproject.toml with version specifiers, like `"boto3>=1.39.3"`
    only then dependabot tries to update them

    in short, dependabot
    - reads pyproject.toml
    - updates uv.lock

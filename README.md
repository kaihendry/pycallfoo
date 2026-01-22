Exercise https://github.com/kaihendry/pyunderstand

## Dependency ref resolution

The `checkout-dependency` composite action (`.github/actions/checkout-dependency`) resolves refs in this order:

1. Manual override via `ref` input
2. Matching branch name (if current branch exists in target repo, skipped for main/master)
3. Value from `config.yaml` (configurable key, defaults to `version`)
4. Default branch

### Usage

```yaml
- uses: ./.github/actions/checkout-dependency
  with:
    repository: owner/repo
    ref: ${{ inputs.some_ref }}      # optional override
    path: local-path
    config-key: version              # optional, defaults to 'version'
    token: ${{ github.token }}
```

### Scaling to multiple dependencies

```yaml
- uses: ./.github/actions/checkout-dependency
  with:
    repository: kaihendry/pyunderstand
    path: pyunderstand
    config-key: pyunderstand_version
    token: ${{ github.token }}

- uses: ./.github/actions/checkout-dependency
  with:
    repository: kaihendry/another-dep
    path: another-dep
    config-key: another_dep_version
    token: ${{ github.token }}
```

With `config.yaml`:
```yaml
pyunderstand_version: main
another_dep_version: v1.2.3
```

## Local development

When GitHub Actions is unavailable, use the Python script:

```bash
# Normal usage - resolves ref automatically
./setup_deps.py
uv run main.py

# Override with specific ref
PYUNDERSTAND_REF=feature-branch ./setup_deps.py

# Test the resolution logic
./test_ref_resolution.py
```

The script follows the same resolution order as the GitHub Action.

## Why this pattern?

This solves the problem of **coordinated development across repositories**:

| Scenario | What happens |
|----------|--------------|
| Working on `feature-x` branch in both repos | Automatically uses `feature-x` from pyunderstand |
| Push to `main` | Uses pinned version from `config.yaml` (stable) |
| CI/CD override needed | Set `PYUNDERSTAND_REF` or use workflow_dispatch |

This avoids:
- Hardcoding refs in pyproject.toml that break other branches
- Forgetting to update refs when switching contexts
- CI failures due to mismatched branches during feature development

https://discord.com/channels/1039017663004942429/1388197295387840552/1392105578649878611

    so ... (learned this the hard way) ...

    you need to have the deps in pyproject.toml with version specifiers, like `"boto3>=1.39.3"`
    only then dependabot tries to update them

    in short, dependabot
    - reads pyproject.toml
    - updates uv.lock

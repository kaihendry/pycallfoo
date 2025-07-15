Exercise https://github.com/kaihendry/pyunderstand

https://discord.com/channels/1039017663004942429/1388197295387840552/1392105578649878611

    so ... (learned this the hard way) ...

    you need to have the deps in pyproject.toml with version specifiers, like `"boto3>=1.39.3"`
    only then dependabot tries to update them

    in short, dependabot
    - reads pyproject.toml
    - updates uv.lock

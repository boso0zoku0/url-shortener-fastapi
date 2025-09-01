# FastAPI URL Shortener
[![Python checks](https://img.shields.io/github/actions/workflow/status/OWNER/REPO/python-checks.yaml?branch=main&style=for-the-badge&label=Python%20checks&logo=github)](https://github.com/boso0zoku0/url-shortener-fastapi/actions/workflows/python-checks.yaml)
                                                                                                                                                                            
## Develop

Check GitHub Actions after any push

### Setup

Right click `url-shortener` -> Mark Directory as -> Sources Root


### Install depencies

Install all packages:
```shell
uv sync
```

### Configure pre-commit

Install pre-commit hook:
```shell
pre-commit install
```

### Run

Go to workdir:
```shell
cd url-shortener
```

Run dev server:
```shell
fastapi dev
```

## Snippets

```shell
python -c 'import secrets;print(secrets.token_urlsafe(16))'
```

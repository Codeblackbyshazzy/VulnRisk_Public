# Backend packaging migration (Poetry → uv)

## Summary

The backend now uses a single PEP 621 manifest and lockfile:

- **Manifest:** `backend/pyproject.toml`
- **Lockfile:** `backend/uv.lock`
- **Tool:** [uv](https://docs.astral.sh/uv/)

Docker installs dependencies with `uv sync --frozen --no-dev` (see `backend/Dockerfile`). The virtualenv lives at `/opt/venv` so `docker-compose` volume mounts of `./backend:/app` do not overwrite installed packages.

## Contributor commands

```bash
cd backend
uv sync --all-groups   # runtime + dev dependencies
make dev               # start API
make test
make lint
make lock-check        # verify lockfile is current
```

Optional feature extras:

```bash
uv sync --extra aws    # boto3 for Lambda/DynamoDB
uv sync --extra nlp    # spaCy / transformers
```

## GitHub issue response (template)

> Thanks for flagging the mixed Poetry / `requirements.txt` setup — you were right that it was not intentional.
>
> We consolidated on **PEP 621 `pyproject.toml` + `uv.lock`**. Docker and local dev now install from the same lockfile (`uv sync --frozen --no-dev` in the image). Hand-maintained `requirements.txt` and Poetry config were removed. Unused packages (e.g. sqlalchemy, celery from the old split manifests) were dropped unless imported by the app.
>
> **Breaking change for local backend dev:** use Python 3.13+, install [uv](https://docs.astral.sh/uv/), then `cd backend && uv sync --all-groups`. Docker users only need `docker compose build --no-cache backend` after pulling.
>
> See `docs/PACKAGING_MIGRATION.md` for details.

## PR test plan

- [ ] `cd backend && uv lock --check`
- [ ] `uv sync --all-groups && make test && make lint`
- [ ] `docker compose build backend && docker compose up -d` — `curl http://localhost:8000/health`
- [ ] No remaining references to `poetry` or `backend/requirements.txt`

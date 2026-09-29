# Suggested Project Commands

Codex may implement these using Make, Taskfile, npm scripts, or equivalent.

```bash
# Python environment
uv sync

# Generate dataset
uv run python -m ml.data.generate

# Validate data
uv run python -m ml.data.validate

# Train all models
uv run python -m ml.models.train

# Tune
uv run python -m ml.models.tune

# Evaluate champion
uv run python -m ml.models.evaluate

# Generate reports
uv run python -m ml.evaluation.build_reports

# Run API
uv run uvicorn apps.api.main:app --reload

# Run ML tests
uv run pytest

# Frontend
cd apps/web
pnpm install
pnpm dev

# Frontend checks
pnpm lint
pnpm typecheck
pnpm test

# E2E
pnpm playwright test
```

Prefer a root-level convenience interface:

```bash
make setup
make data
make train
make reports
make api
make web
make test
```

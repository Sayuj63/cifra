.PHONY: setup data eda train api web test
setup:
	python -m pip install -e ".[dev,ops]"
	cd apps/web && npm install
data:
	python -m ml.data.generate
eda:
	python -m ml.evaluation.eda
train:
	python -m ml.models.train
api:
	python -m uvicorn apps.api.main:app --reload
web:
	cd apps/web && npm run dev
test:
	python -m pytest -q
	cd apps/web && npm run typecheck && npm run lint && npm run build

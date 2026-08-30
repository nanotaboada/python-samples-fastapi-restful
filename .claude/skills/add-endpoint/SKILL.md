---
name: add-endpoint
description: Step-by-step recipes for adding an endpoint or modifying the schema in this repo
---

# Endpoint and schema recipes

**Add an endpoint**: Add Pydantic model in `models/` if the request/response
shape is new → add async service method in `services/` with error handling and
rollback → add route in `routes/` with `Depends(generate_async_session)` →
add tests following the naming pattern → run pre-commit checks.

**Modify schema**: Update `schemas/player_schema.py` → run
`uv run alembic revision --autogenerate -m "description"` to generate a
migration → review and adjust the generated file in `alembic/versions/` →
run `uv run alembic upgrade head` → update `models/player_model.py` if the
API shape changes → update services and tests → run `pytest`.

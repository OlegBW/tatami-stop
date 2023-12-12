default:
    just --list

lint flag="" path=".":
    @ruff check {{flag}} {{path}}

test:
    @pytest

start:
    @uvicorn src.main:app --reload
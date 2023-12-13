default:
    just --list

lint flag="" path=".":
    @ruff check {{flag}} {{path}}

format flag="" path=".":
    @ruff format {{flag}} {{path}}

test:
    @pytest

start:
    @uvicorn src.main:app --reload
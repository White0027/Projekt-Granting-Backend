# GQL_Granting

__Tomáš Urban,__ 
__Sabina Kubešová__
________________________________________________________________________

## Deníček

7.10.2024 publikován repositář
________________________________________________________________________

## Aktuální úkoly

- [x] Fork hrbolek/gql_granting jako template
________________________________________________________________________

## Harmonogram skupinové práce

__7.10.2024__ vybraná témata, publikované repositories

__7.11.2024__ 1. projektový den, doložení kompletních descriptions (gql modely)

__9.12.2024__ 2. projektový den, doložení funkcionality (crud)

__29.1.2025__ 3. projektový den, doložení testů
________________________________________________________________________

## Poznámky

```bash
uvicorn main:app --env-file environment.txt --port 8001
```
```bash
pytest --cov-report term-missing --cov=src --log-cli-level=INFO -x
```
```bash
pytest -k "test_FillDataViaGQL" --cov-report term-missing --cov=src --log-cli-level=INFO -x
```

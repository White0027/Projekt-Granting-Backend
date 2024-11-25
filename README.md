# GQL_Granting

__Tomáš Urban,__ 
__Sabina Kubešová__
________________________________________________________________________

## Deníček

7.10.2024 publikován repositář

30.10.2024 dokončení komentářů u DBDefinitons

5.11.2024 dokončení descriptions v GraphTypeDefinitions

7.11.2024 uspěšné prezentování projektu na 1. projektovém dni

14.11.2024 úprava Dataloaderů

25.11.2024 přidání Voyager pro zobrazení dat
________________________________________________________________________

## Aktuální úkoly

- [x] Fork hrbolek/gql_granting jako template
- [x] Okomentovat DBDefinitons
- [x] Přidat description v GraphTypeDefinitions
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

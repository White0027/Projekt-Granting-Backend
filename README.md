# GQL_Granting

__Tomáš Urban,__ 
__Sabina Kubešová__
________________________________________________________________________

## Deníček

7.10.2024 Publikován repositář

30.10.2024 Dokončení komentářů u DBDefinitons

5.11.2024 Dokončení descriptions v GraphTypeDefinitions

7.11.2024 Úspěšné prezentování projektu na 1. projektovém dni

14.11.2024 Úprava Dataloaderů

25.11.2024 Přidání Voyager pro zobrazení dat

28.11.2024 Přidání schémat a _data do QGL modelů

9.12.2024 Úspěšné prezenetování projektu na 2. projektovém dni

6.1.2025 Kompletní dokončení CRUD operací

21.1.2025 Částečná oprava testů (předělání portů, přidaní POST k FastAPI pro /oauth/login3)
          Splněno ze 72% (Test má GET, server má POST)

22.1.2025 Splněno 72%, oprava předchozích chyb, potřeba doplnit "tables"

27.1.2025 Splněno 74%, aktualizace starých testů, potřeba doplnit CUD operace

28.1.2025 Splněno 79%, update testů

29.1.2025 Splněno 84%, přidání CUD operací u classificationlevels, předělání GraphTypeDefinitions.py
          Úspěšné prezentování projektu na 3. projektovém dni

8.2.2025 Splněno 89%, dokončení testů na CRUD operace

10.2.2025 Splněno 90%
________________________________________________________________________

## Aktuální úkoly

- [x] Fork hrbolek/gql_granting jako template
- [x] Okomentovat DBDefinitons
- [x] Přidat description v GraphTypeDefinitions
- [x] Všechny GQL typy mají private attribut _data, což je odpovídající db řádek (neplatí pro extended types)
- [x] Všechny GQL typy a odpovídající DB modely mají atributy:
    - lastchange
    - created
    - changedby_id
    - createby_id
    - rbacobject_id
- [x] Přidání CRUD operací
- [x] Vektorové atributy mají volitelné parametry where, limit a skip a mají alternativu podle standardu relay connection
- [ ] Součástí filtrů (where) bude primární klíč i cizí klíče
- [x] Počáteční import dat je realizován jako asynchronní task: 
    ```python
    task = asyncio.create_task(initDB(asyncSessionMaker))
    ```
- [x] Mutace upravit tak, aby používaly:
    ```python
    from uoishelpers.resolvers import encapsulateInsert, encapsulateUpdate, encapsulateDelete
    ```
- [x] Všechny atributy mají anotace, např.:
    ```python
    Annotated[Optional[str], strawberry.argument(description="")]="0"
    ```
- [x] U všech fields jsou permission classes a v komentáři uvedeno, kdo má k atributu či funkcionalitě přístup
- [x] Testy s alespoň 90% pokrytím pomocí dotazů, ty jsou uloženy v systému souborů (read.gql, create.gql, …)

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
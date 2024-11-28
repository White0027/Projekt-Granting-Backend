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

28.11.2024 Přidání schémat a _data do QGL modelů
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

- [ ] Vektorové atributy mají volitelné parametry where, limit a skip a mají alternativu podle standardu relay connection
- [ ] Vektorové resolvery globální úrovně (query) mají také alternativu podle standardu relay connection
- [ ] Součástí filtrů (where) bude primární klíč i cizí klíče
- [ ] Počáteční import dat je realizován jako asynchronní task: 
    ```python
    task = asyncio.create_task(initDB(asyncSessionMaker))
    ```
- [ ] Mutace upravit tak, aby používaly:
    ```python
    from uoishelpers.resolvers import encapsulateInsert, encapsulateUpdate, encapsulateDelete
    ```
- [ ] Všechny atributy mají anotace, např.:
    ```python
    Annotated[Optional[str], strawberry.argument(description="")]="0"
    ```
- [ ] U všech fields jsou permission classes a v komentáři uvedeno, kdo má k atributu či funkcionalitě přístup
- [ ] Testy s alespoň 90% pokrytím pomocí dotazů, ty jsou uloženy v systému souborů (read.gql, create.gql, …)

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


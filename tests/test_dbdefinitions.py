import pytest 
from .shared import prepare_demodata, prepare_in_memory_sqllite

@pytest.mark.asyncio
async def test_table_users_feed():
    # Test, zda je tabulka 'users_feed' inicializována a naplněna testovacími daty
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    # data = get_demodata()

def test_connection_string():
    # Ověření, že vrácený connection string obsahuje nezbytné části
    from src.DBDefinitions import ComposeConnectionString
    connectionString = ComposeConnectionString()

    assert "://" in connectionString
    assert "@" in connectionString


@pytest.mark.asyncio
async def test_table_start_engine():
    # Kontroluje, zda je možné nastartovat engine a vytvořit asynchronní session
    from src.DBDefinitions import startEngine
    connectionString = "sqlite+aiosqlite:///:memory:"
    async_session_maker = await startEngine(
        connectionString, makeDrop=True, makeUp=True
    )

    assert async_session_maker is not None
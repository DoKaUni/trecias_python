import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from code.III_praktinis_darbas import Base, Shop, Item, Component

# Sukuriamas SQLite engine testavimui
@pytest.fixture(scope="module")
def engine():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)  # Create tables here
    yield engine
    Base.metadata.drop_all(engine)

# Sesijos sukurimas testavimui
@pytest.fixture(scope="function")
def session(engine):
    """Creates a new database session for a test with a rollback at the end."""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    yield session
    session.close()
    transaction.rollback()
    connection.close()

# Pirmos užduoties testavimas
class Test_1uzd:
    def test_tables_created(self, engine): # Tikrinama ar egzistuoja lentelės duomenų bazėse
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        assert 'shops' in tables
        assert 'items' in tables
        assert 'components' in tables

# Antros užduoties testavimas
class Test_2uzd:
    def test_add_shop(self, session): # Tikrinama ar buvo pridėtas shops įrašas
        shop = Shop(name='IKI', address='Kaunas, Iki gatvė 1')

        session.add(shop)
        session.commit()

        assert shop in session

    def test_add_item(self, session): # Tikrinama ar buvo pridėtas items įrašas
        shop = Shop(name='IKI', address='Kaunas, Iki gatvė 1')
        item = Item(barcode='112233112233', name='Žemaičių duona', unit_price=1.55, shop=shop)

        session.add(item)
        session.commit()

        assert item in session

    def test_add_component(self, session): # Tikrinama ar buvo pridėtas component įrašas
        shop = Shop(name='IKI', address='Kaunas, Iki gatvė 1')
        item = Item(barcode='112233112233', name='Žemaičių duona', unit_price=1.55, shop=shop)
        component = Component(name='Miltai', quantity=1.50, item=item)

        session.add(component)
        session.commit()

        assert component in session

# Trečios užduoties testavimas
class Test_3uzd:
    def test_query_update_component(self, session): # Testuojama ar galima pakeisti component įrašo quantity reikšme
        item = Item(barcode='112233112233', name='Žemaičių duona', unit_price=1.55)
        component = Component(name='Vanduo', quantity=1.00)

        session.add(component)
        session.commit()
        
        query = session.query(Component).filter(Component.name == 'Vanduo' and Component.item == item).first()
        
        assert query.quantity == 1.00
        
        query.quantity = 1.50
        session.commit()
        
        updated_query = session.query(Component).filter(Component.name == 'Vanduo' and Component.item == item).first()

        assert updated_query.quantity == 1.50

    def test_delete_component(self, session): # Testuojama ar galima ištrinti įrašą
        item = Item(barcode='99919191991', description='Pienas iš Aukštaitijos', name='Aukštaičių pienas', unit_price=2.99)
        component = Component(name='Pienas', quantity=1.10, item=item)

        session.add(component)
        session.commit()
        
        session.delete(component)
        session.commit()
        
        deleted_component = session.query(Component).filter(Component.name == 'Pienas', Component.item == item).first()

        assert deleted_component is None
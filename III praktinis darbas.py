"""
    Užduotis #1
    Programa turi 3 klases, kurios nurodo duomenų bazės lentelės ir jų saugomus duomenis.

    Parametrai:
        Shop(Base) - klase nurodanti shops lentelės duomenis
        Item(Base) - klase nurodanti items lentelės duomenis
        Component(Base) - klase nurodanti components lentelės duomenis
        
    Rezultatas:
        Programa sukuria duomenų bazės lenteles, kurias galima naudoti velesniams veiksmams.

"""

from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from datetime import datetime
Base = declarative_base()

class Shop(Base):
    __tablename__ = "shops"

    id = Column(Integer, primary_key = True) # Sveikas skaičius, kuris yra pirminis raktas ( auto inkrementavimas yra numatytas, jeigu naudojamas primary_key = True)
    name = Column(String(40), nullable = False) # Pavadinimas, kuris yra 40 simbolių ilgio ir yra privalomas (negali būti tusčias)
    address = Column(String(100)) # Adresas, kuris yra 100 simbolių ilgio
    items = relationship("Item", back_populates = "shop") # Ryšys su Item klase (back_populates - nurodo dvi pusi ryšį)

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key = True) # Sveikas skaičius, kuris yra pirminis raktas
    barcode = Column(String(32), unique = True) # Barkodas, kuris yra 32 simbolių ilgio ir turi būti unikalus
    name = Column(String(40), nullable = False) # Pavadinimas, kuris yra 40 simbolių ilgio ir yra privalomas (negali būti tusčias)
    description = Column(String(200), default = '') # Aprašymas, kuris yra 200 simbolių ilgio ir numatyta vertė tusčia
    unit_price = Column(Numeric(10, 2), nullable = False, default = 1.00) #
    created_at = Column(DateTime, default = datetime.now) # Data ir laikas, numatyta vertė yra kada sukuriamas įrašas
    shop_id = Column(ForeignKey("shops.id")) # Svetimas raktas iš shops
    shop = relationship("Shop", back_populates = "items") # Ryšys su Shop klase
    components = relationship("Component", back_populates = "item") # Ryšys su Component klase

class Component(Base):
    __tablename__ = "components"

    id = Column(Integer, primary_key = True) # Sveikas skaičius, kuris yra pirminis raktas
    name = Column(String(20)) # Pavadinimas, kuris yra 20 simbolių ilgio
    quantity = Column(Numeric(10, 2), default = 1.00) # Kiekis, 
    item_id = Column(ForeignKey("items.id")) # Svetimas raktas iš items
    item = relationship("Item", back_populates = "components") # Ryšys su Item klase

Shop.__table__
Item.__table__
Component.__table__

"""
    Užduotis #2
    Sukuriami įrašai duomenų bazės lentelėse iš pirmos užduoties tryjų klasių

    Parametrai:
        Shop įrašai 
        Item įrašai
        Component įrašai

    Rezultatas:
    Programa užpildo duomenų bazės lenteles su konkrečiais parduotuvių, prekių ir komponentų įrašais
"""

from sqlalchemy.orm import sessionmaker

# Sukuriamas engine
engine = create_engine('sqlite:///:memory:', echo=True)

# Sukuriama duomenu bazes schema
Base.metadata.create_all(engine)

# Sukuriama sesija
Session = sessionmaker(bind=engine)
session = Session()

# Sukuriami Shop irašai
shop_iki = Shop(name='IKI', address='Kaunas, Iki gatvė 1')
shop_maxima = Shop(name='MAXIMA', address='Kaunas, Maksima gatvė 2')

# Sukuriami Item irašai
item_iki_duona = Item(barcode='112233112233', name='Žemaičių duona', unit_price=1.55, shop=shop_iki)
item_iki_pienas = Item(barcode='33333222111', description='Pienas iš Žemaitijos', name='Žemaičių pienas', unit_price=2.69, shop=shop_iki)
item_maxima_duona = Item(barcode='99898989898', name='Aukštaičių duona', unit_price=1.65, shop=shop_maxima)
item_maxima_pienas = Item(barcode='99919191991', description='Pienas iš Aukštaitijos', name='Aukštaičių pienas', unit_price=2.99, shop=shop_maxima)

# Sukuriami Component irašai
component_iki_miltai = Component(name='Miltai', quantity=1.50, item=item_iki_duona)
component_iki_vanduo = Component(name='Vanduo', quantity=1.00, item=item_iki_duona)
component_iki_pienas = Component(name='Pienas', quantity=1.00, item=item_iki_pienas)
component_maxima_miltai = Component(name='Miltai', quantity=1.60, item=item_maxima_duona)
component_maxima_vanduo = Component(name='Vanduo', quantity=1.10, item=item_maxima_duona)
component_maxima_pienas = Component(name='Pienas', quantity=1.10, item=item_maxima_pienas)

# Pridedami irašai sesijai
session.add_all([shop_iki, shop_maxima, item_iki_duona, item_iki_pienas, item_maxima_duona, item_maxima_pienas,
                 component_iki_miltai, component_iki_vanduo, component_iki_pienas,
                 component_maxima_miltai, component_maxima_vanduo, component_maxima_pienas])

# Commitinami pokyčiai duombazeje
session.commit()

"""
    Užduotis #3
    Pakeičia IKI vandens quantity iš 1.00 į 1.45
    Ištrina MAXIMA Aukštaičių pieno komponentą 'Pienas'.

    Parametrai:
        query_iki_vanduo - paieškos kintamasis, naudojamas rasti vandens komponentą.
        component_to_delete - paieškos kintamasis, naudojamas ištrinti pieno komponentą.
    
    Rezultatas:
    Vandens kiekis pakeistas iš 1.00 į 1.45, Maximos pieno komponentas ištrintas.

"""
# Randamas komponentas, t.y. iki vanduo
query_iki_vanduo = session.query(Component).filter(Component.name == 'Vanduo' and Component.item == item_iki_duona)
if query_iki_vanduo: # Jei vanduo randamas
    query_iki_vanduo.quantity = 1.45 # Pakeiciamas vandens kiekis i 1.45 is 1.00
    print("IKI vandens kiekis pakeistas į: " + str(query_iki_vanduo.quantity))
else: # Jei vanduo nerandamas
    print("IKI vandens komponentas(component_iki_vanduo) nerastas.")

#Randamas komponentas, t.y. MAXIMA pienas
component_to_delete = session.query(Component).filter(Component.name == 'Pienas' and Component.item == item_maxima_pienas).first()

if component_to_delete: # Jei pienas randamas
    session.delete(component_to_delete) # Istrinamas komponentas
    session.commit() # Pokyciai issaugomi duomenu bazeje
    print("MAXIMA pieno komponentas(component_maxima_pienas) ištrintas.")
else: # Jei pienas nerandamas
    print("MAXIMA pieno komponentas(component_maxima_pienas) nerastas.")




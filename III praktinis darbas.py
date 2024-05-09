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

engine = create_engine("sqlite:///:memory:", echo=True)

Shop.__table__
Item.__table__
Component.__table__

Base.metadata.create_all(engine)

"""
    Užduotis #2
    ...
"""
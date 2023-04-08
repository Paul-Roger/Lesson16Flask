from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, ForeignKey, Numeric, Date, delete
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///AutoDB.sqlite', echo=True)

Base = declarative_base()

class AutoBrand(Base):
    __tablename__ = 'AutoBrand'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    BrandName = Column(String(100), nullable=False)
    NoOfSearches = Column(Integer)

    def __init__(self, brandname, noofsearches = 0):
        self.BrandName = brandname
        self.NoOfSearches = noofsearches

    def __str__(self):
        return f'{self.ID}) {self.NoOfSearches} {self.NoOfSearches}'


class SearchResult(Base):
    __tablename__ = 'SearchResult'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    BrandID = Column(Integer, ForeignKey('AutoBrand.ID'), nullable=False)
    Title = Column(String(256), nullable=False)
    PubDate = Column(Date, nullable=True)
    Link = Column(String(256), nullable=False)
    ShortText = Column(String(256), nullable=True)
    #autobrand = relationship('AutoBrand', backref='results')

    def __init__(self, brandid, title, pubdate, link, shorttext):
        self.BrandID = brandid
        self.Title = title
        self.PubDate = pubdate
        self.Link = link
        self.ShortText = shorttext
    def __str__(self):
        return f'{self.ID}) {self.Brand.BrandName} {self.Title} {self.PubDate} {self.Link} {self.ShortText}'

# Создание таблицы
Base.metadata.create_all(engine)

# Создание сессии
Session = sessionmaker(bind=engine)
# create a Session
session = Session()

#Проверим смисок автобрендов
record_no = session.query(AutoBrand).count()
if record_no <= 0:
    # первоначальное заполнение
    session.add_all([AutoBrand('Toyota', 0), AutoBrand('Tesla', 0), AutoBrand('Vokswagen', 0), AutoBrand('Mercedes', 0), AutoBrand('BMW', 0), AutoBrand('Renault', 0)])
    session.commit()
session.close()

from SQLAlchemyDB import *

# Создание сессии
def session_init():
    engine = create_engine('sqlite:///AutoDB.sqlite', echo=True)
    Session = sessionmaker(bind=engine)
    # create a Session
    return (Session())

#Проверим смисок автобрендов и заполним список
def autolist_init(session:Session):
    record_no = session.query(AutoBrand).count()
    if record_no <= 0:
        # первоначальное заполнение
        session.add_all([AutoBrand('Toyota', 0), AutoBrand('Tesla', 0), AutoBrand('Vokswagen', 0), AutoBrand('Mercedes', 0), AutoBrand('BMW', 0), AutoBrand('Renault', 0)])
        session.commit()

def check_add(session:Session, brandname) -> int:
        brandrec = session.query(AutoBrand).filter(AutoBrand.BrandName.like(f'%{brandname}%')).first()
        if brandrec == None:
            session.add(AutoBrand(brandname, 1))
            brandrec = session.query(AutoBrand).filter(AutoBrand.BrandName.like(f'%{brandname}%')).first()
        else:
            brandrec.NoOfSearches += 1
        session.commit()
        return brandrec.ID

def add_article(session:Session, brand_id, title, pubdate:Date, link, short_text):
    print("*** add_article ***", brand_id, title, pubdate, link, short_text)
    print(type(brand_id), type(title), type(pubdate), type(link), type(short_text))

    session.add(SearchResult(brand_id, title, pubdate, link, short_text))
    session.commit()
    return

def brandlist(session:Session):
    brands = session.query(AutoBrand.BrandName).order_by(AutoBrand.BrandName.desc()).limit(15).all()
    brand_list = []
    for brand in brands:
        brand_list.append(brand[0])
    print(brand_list)
    return (brand_list)

def articlelist(session:Session, brand_template):
    print("brand_template",brand_template)
    articles = session.query(SearchResult.Title, SearchResult.PubDate, SearchResult.Link, SearchResult.ShortText).where(SearchResult.BrandID == AutoBrand.ID).where(AutoBrand.BrandName.like(f'%{brand_template}%')).all()
    return (articles)

def cleararticles(session:Session, brand_template):
    print("brand_template",brand_template)
#find brand
    brand = session.query(AutoBrand.ID).filter(AutoBrand.BrandName.like(f'%{brand_template}%')).first()
    if brand:
        del_records = delete(SearchResult).where(SearchResult.BrandID == brand[0])
        session.execute(del_records)
        session.commit()



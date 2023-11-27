from sqlalchemy.orm import Session

from .import keygen, models, schemas 

def create_db_url(url: schemas.URLBase, db: Session):
    key = keygen.create_unique_random_key(db)
    secret_key = f"{key}_{keygen.create_random_key(length=8)}"
    db_url = models.URL(target_url=url.target_url, key=key, secret_key=secret_key)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key

    return db_url

def get_db_url_by_key(db: Session, key: str, secret: bool):
    if secret is True:
        return (db.query(models.URL).filter(models.URL.secret_key == key, models.URL.is_active).first())
    else:
        return (db.query(models.URL).filter(models.URL.key == key, models.URL.is_active).first())


def update_db_clicks(db: Session, db_url: schemas.URL):
    db_url.clicks += 1 
    db.commit()
    db.refresh(db_url)
    return(db_url)

def deactivate_db_url_by_secret_key(db: Session, secret_key: str):
    db_url = get_db_url_by_key(db=db, key=secret_key, secret=True)
    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)
    return db_url
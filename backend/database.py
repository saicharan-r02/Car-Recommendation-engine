import os
import re
import sys
from datetime import datetime
from typing import Dict,Any,List,Optional
import pandas as pd
from sqlalchemy import create_engine,Column,Integer,Float,String,DateTime,ForeignKey,func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, scoped_session

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
DB_PATH=os.path.join(BASE_DIR,"car_inventory.db")
DATABASE_URI=f"sqlite:///{DB_PATH}"

engine=create_engine(DATABASE_URI,connect_args={"check_same_thread":False})
SessionLocal=scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base=declarative_base()


class Car(Base):
    """Dynamic car inventory specifications."""
    __tablename__="cars"

    id=Column(Integer,primary_key=True,autoincrement=True)
    brand=Column(String(100),nullable=False,index=True)
    model=Column(String(100),nullable=False,index=True)
    year=Column(Integer,default=2023)
    engine_size=Column(String(50),nullable=True)
    horsepower=Column(Integer,default=400)
    torque=Column(Integer,default=400)
    zero_to_sixty=Column(Float,nullable=False,index=True)
    price_usd=Column(Float,nullable=False,index=True)
    created_at=Column(DateTime,default=datetime.utcnow)

    # Relationships
    favorites=relationship("UserFavorite",back_populates="car",cascade="all,delete-orphan")


class UserSearchLog(Base):
    """Logs user criteria and search timestamps."""
    __tablename__="user_search_logs"

    id=Column(Integer,primary_key=True,autoincrement=True)
    target_time=Column(Float,nullable=False)
    target_budget=Column(Float,nullable=False)
    results_count=Column(Integer,default=0)
    searched_at=Column(DateTime,default=datetime.utcnow)


class UserFavorite(Base):
    """User wishlist / garage saved bookmarks."""
    __tablename__="user_favorites"

    id = Column(Integer, primary_key=True, autoincrement=True)
    car_id=Column(Integer,ForeignKey("cars.id"),nullable=False)
    user_note=Column(String(255),default="Saved to Garage")
    saved_at=Column(DateTime,default=datetime.utcnow)

    # Relationships
    car = relationship("Car",back_populates="favorites")


def init_db():
    """Initializes tables and automatically seeds from CSV if empty."""
    Base.metadata.create_all(bind=engine)
    session=SessionLocal()
    try:
        count=session.query(func.count(Car.id)).scalar()or 0
        if count==0:
            csv_path=os.path.join(BASE_DIR,"Sport car price.csv")
            if os.path.exists(csv_path):
                seed_from_csv(csv_path)
    finally:
        session.close()
    print(f"[OK] Car Recommendation database initialized at: {DB_PATH}",file=sys.stderr)


def seed_from_csv(csv_path: str):
    """Parses and seeds the initial CSV car records into SQLite."""
    print(f"[SEED] Importing cars from {csv_path}...")
    df=pd.read_csv(csv_path)

    # Clean price column
    df["Price (in USD)"]=df["Price (in USD)"].astype(str).str.replace(r'[\$,"]','',regex=True)
    df["Price (in USD)"]=pd.to_numeric(df["Price (in USD)"],errors="coerce")

    # Clean 0-60 column
    df["0-60 MPH Time (seconds)"]=pd.to_numeric(df["0-60 MPH Time (seconds)"],errors="coerce")
    
    make_col="Car Name" if "Car Name" in df.columns else "Car Make"
    df.dropna(subset=["Price (in USD)","0-60 MPH Time (seconds)",make_col,"Car Model"],inplace=True)

    # Deduplicate
    df=df.drop_duplicates(subset=[make_col,"Car Model"])

    session=SessionLocal()
    try:
        cars_to_add=[]
        for _,row in df.iterrows():
            hp_raw=re.sub(r"[^\d]","",str(row.get("Horsepower","400")))
            hp_val=int(hp_raw) if hp_raw else 400

            torque_raw=re.sub(r"[^\d]","",str(row.get("Torque (lb-ft)","400")))
            torque_val=int(torque_raw) if torque_raw else 400

            year_raw=re.sub(r"[^\d]","",str(row.get("Year","2023")))
            year_val=int(year_raw) if year_raw else 2023

            car = Car(
                brand=str(row[make_col]).strip(),
                model=str(row["Car Model"]).strip(),
                year=year_val,
                engine_size=str(row.get("Engine Size (L)", "3.0L")).strip(),
                horsepower=hp_val,
                torque=torque_val,
                zero_to_sixty=float(row["0-60 MPH Time (seconds)"]),
                price_usd=float(row["Price (in USD)"])
            )
            cars_to_add.append(car)

        session.bulk_save_objects(cars_to_add)
        session.commit()
        print(f"[SEED] Successfully seeded {len(cars_to_add)} cars into car_inventory.db.")
    except Exception as e:
        session.rollback()
        print(f"[ERROR] Seeding failed: {e}")
    finally:
        session.close()


def get_recommendations(u_time:float,u_price:float,top_n:int=5) -> List[Dict[str,Any]]:
    """Calculates similarity against dynamic database inventory."""
    session=SessionLocal()
    try:
        cars=session.query(Car).filter(Car.price_usd<=u_price).all()
        if not cars:
            # Fallback if no cars under strict budget: find closest affordable
            cars=session.query(Car).all()
            if not cars:
                return[]

        # Find max metrics for normalization
        p_max=session.query(func.max(Car.price_usd)).scalar()or 1.0
        t_max=session.query(func.max(Car.zero_to_sixty)).scalar()or 1.0

        scored=[]
        for c in cars:
            score=(abs(c.price_usd-u_price)/p_max*0.8)+(abs(c.zero_to_sixty-u_time)/t_max*0.2)
            scored.append((score,c))

        scored.sort(key=lambda x:x[0])

        results=[]
        for _,c in scored[:top_n]:
            results.append({
                "id":c.id,
                "Car_Name":c.brand,
                "Car_Model":c.model,
                "Year":c.year,
                "Horsepower":c.horsepower,
                "Time":c.zero_to_sixty,
                "Price":c.price_usd
            })

        # Log search query
        log=UserSearchLog(
            target_time=u_time,
            target_budget=u_price,
            results_count=len(results)
        )
        session.add(log)
        session.commit()

        return results
    finally:
        session.close()

def add_new_car(brand: str,model: str,year: int,horsepower: int,zero_to_sixty: float,price_usd: float) -> int:
    """Adds a new car to the dynamic inventory."""
    session=SessionLocal()
    try:
        car=Car(
            brand=brand,
            model=model,
            year=year,
            horsepower=horsepower,
            zero_to_sixty=zero_to_sixty,
            price_usd=price_usd
        )
        session.add(car)
        session.commit()
        return car.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def save_favorite_car(car_id:int,note:str="Saved Car") -> bool:
    """Adds a car to favorites."""
    session=SessionLocal()
    try:
        fav=UserFavorite(car_id=car_id,user_note=note)
        session.add(fav)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False
    finally:
        session.close()

def get_favorites() -> List[Dict[str,Any]]:
    """Retrieves all saved favorites."""
    session=SessionLocal()
    try:
        favs=session.query(UserFavorite).join(Car).order_by(UserFavorite.saved_at.desc()).all()
        return [
            {
                "favorite_id":f.id,
                "car_id":f.car.id,
                "brand":f.car.brand,
                "model":f.car.model,
                "year":f.car.year,
                "zero_to_sixty":f.car.zero_to_sixty,
                "price_usd":f.car.price_usd,
                "note":f.user_note,
                "saved_at":f.saved_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            for f in favs
        ]
    finally:
        session.close()

if __name__=="__main__":
    init_db()

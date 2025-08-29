from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///weather.db')
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    default_city = Column(String)
    temperature_unit = Column(String, default='C')
    weather_searches = relationship("WeatherSearch", back_populates="user", cascade="all, delete-orphan")
    favorites = relationship("FavoriteCity", back_populates="user", cascade="all, delete-orphan")
    
    @hybrid_property
    def display_name(self): return self.name.title()
    
    @classmethod
    def create(cls, name, default_city=None, temperature_unit='C'):
        session = Session()
        try: user = cls(name=name, default_city=default_city, temperature_unit=temperature_unit); session.add(user); session.commit(); session.refresh(user); return user
        finally: session.close()
    
    @classmethod
    def get_all_for_cli(cls):
        session = Session()
        try: return [(u.id, u.display_name, len(u.weather_searches)) for u in session.query(cls).all()]
        finally: session.close()
    
    @classmethod
    def find_by_id(cls, user_id):
        session = Session()
        try: return session.query(cls).filter(cls.id == user_id).first()
        finally: session.close()

class WeatherSearch(Base):
    __tablename__ = 'weather_searches'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    city = Column(String, nullable=False)
    temperature = Column(Float)
    condition = Column(String)
    search_date = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="weather_searches")
    
    @hybrid_property
    def temp_display(self): return f"{self.temperature:.1f}°" if self.temperature else "N/A"
    
    @classmethod
    def create(cls, user_id, city, temperature=None, condition=None):
        session = Session()
        try: search = cls(user_id=user_id, city=city, temperature=temperature, condition=condition); session.add(search); session.commit(); session.refresh(search); return search
        finally: session.close()
    
    @classmethod
    def get_all_for_cli(cls):
        session = Session()
        try: return [(s.id, s.city, s.temp_display, s.search_date.strftime("%m-%d")) for s in session.query(cls).all()]
        finally: session.close()
    
    @classmethod
    def find_by_id(cls, search_id):
        session = Session()
        try: return session.query(cls).filter(cls.id == search_id).first()
        finally: session.close()
    
    def delete(self):
        session = Session()
        try: session.delete(self); session.commit()
        finally: session.close()

class FavoriteCity(Base):
    __tablename__ = 'favorite_cities'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    city_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    user = relationship("User", back_populates="favorites")
    
    @hybrid_property
    def display_city(self): return self.city_name.title()
    
    @classmethod
    def create(cls, user_id, city_name):
        session = Session()
        try: favorite = cls(user_id=user_id, city_name=city_name); session.add(favorite); session.commit(); session.refresh(favorite); return favorite
        finally: session.close()
    
    @classmethod
    def get_user_favorites_for_cli(cls, user_id):
        session = Session()
        try: return [(f.id, f.display_city) for f in session.query(cls).filter(cls.user_id == user_id, cls.is_active == True).all()]
        finally: session.close()

Base.metadata.create_all(engine)
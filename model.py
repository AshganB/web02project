

from flask_login import UserMixin
from datetime import datetime
import hashlib

#model for User class:

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False) # i.e Hanna Barbera
    display_name = db.Column(db.String(20), unique=True, nullable=False) # i.e hanna_25
    email = db.Column(db.String(120), unique=True, nullable=False) # i.e hanna@hanna-barbera.com
    password = db.Column(db.String(32), nullable=False) 
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    #created_locations = db.relationship('SampleLocation', back_populates='user', order_by="SampleLocation.description", lazy=True) # <<<
    

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()
        
    def __repr__(self):
        return f"User({self.id}, '{self.display_name}', '{self.email}')"      

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()   

#model for new location:
# class SampleLocation(db.Model):
#     __tablename__ = 'sample_locations'

#     id = Column(Integer, primary_key=True)
#     description = Column(String(80))
#     geom = Column(Geometry(geometry_type='POINT', srid=SpatialConstants.SRID))  
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # <<<

    # many to one side of the relationship of SampleLocation with User <<<
    #user = db.relationship("User", back_populates="created_locations") # <<<

 
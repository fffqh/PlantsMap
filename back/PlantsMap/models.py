import datetime
from email.policy import default
from PlantsMap.extensions import db 
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable = False, unique=True)
    user_email = db.Column(db.String(120), nullable = False, unique=True)
    user_pwd = db.Column(db.String(120), nullable=False)
    user_status = db.Column(db.Boolean, nullable=False, default=True)
    # 定义关系
    maps = db.relationship('Map', back_populates='user')
    mnts = db.relationship('Mnt', back_populates='user')
    def __repr__(self):
        return '<user %d %s >' % (self.user_id, self.user_name)
    def set_password(self, password):
        self.user_pwd = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.user_pwd, password)


class Plant(db.Model):
    __tablename__ = "plant"
    plant_id = db.Column(db.Integer, primary_key=True)
    plant_name = db.Column(db.String(80), nullable=False, unique=True)
    plant_attr = db.Column(db.Text, nullable=True)
    #定义关系
    maps = db.relationship('Map', back_populates='plant',
                            cascade='all, delete-orphan', passive_deletes=True)
    def __repr__(self):
        return '<plant id:%d name:%s >' % (self.plant_id, self.plant_name)


class Map(db.Model):
    __tablename__ = "map"
    map_id = db.Column(db.Integer, primary_key=True)
    # map_time = db.Column(db.DateTime, nullable=False)
    map_create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    map_update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    map_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    map_plant_id = db.Column(db.Integer, db.ForeignKey('plant.plant_id', ondelete='CASCADE'), nullable=False)
    map_longitude = db.Column(db.Text, nullable=False)
    map_latitude = db.Column(db.Text, nullable=False)
    map_plant_num = db.Column(db.Integer, nullable=False, default=1)
    # 定义关系
    mnts = db.relationship('Mnt', back_populates='map',
                            cascade='all, delete-orphan', passive_deletes=True)
    user = db.relationship('User', back_populates='maps')
    plant = db.relationship('Plant', back_populates='maps')
    def __repr__(self):
        return '<map id:%d uid:%d pid:%d  %s,%s >' % (self.map_id, self.map_user_id, self.map_plant_id, 
                                                                self.map_longitude, self.map_latitude)

class Mnt(db.Model):
    __tablename__ = "mnt"
    mnt_id = db.Column(db.Integer, primary_key=True)
    mnt_time = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    mnt_type = db.Column(db.Integer, nullable=False)
    mnt_text = db.Column(db.Text, nullable=True)
    mnt_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    mnt_map_id = db.Column(db.Integer, db.ForeignKey('map.map_id', ondelete='CASCADE'), nullable=False)
    # 定义关系
    user = db.relationship('User', back_populates='mnts')
    map = db.relationship('Map', back_populates='mnts')
    def __repr__(self):
        return '<mnt id:%d type:%d uid:%d mid:%d >' % (self.mnt_id, self.mnt_type, self.mnt_user_id, self.mnt_map_id)


class Msg(db.Model):
    __tablename__ = "msg"
    msg_id = db.Column(db.Integer, primary_key=True)
    msg_time = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    msg_from = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    msg_to = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    msg_map_id = db.Column(db.Integer, db.ForeignKey('map.map_id'), nullable=False)
    msg_type = db.Column(db.Integer, nullable=False) # {1:'创建', 2:'更新', 3:'确认', 4:'错误'}
    msg_txt = db.Column(db.Text, nullable=False)
    msg_status = db.Column(db.String(10), nullable=False, default="undo") # 'reject' 'accept' 'undo'


class MapImg(db.Model):
    __tablename__ = "mapimg"
    id = db.Column(db.Integer, primary_key=True)
    map_id = db.Column(db.Integer, db.ForeignKey(
        'map.map_id', ondelete='CASCADE'), nullable=False)
    img_url = db.Column(db.Text, nullable=False)

class PlantImg(db.Model):
    __tablename__ = "plantimg"
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey(
        'plant.plant_id', ondelete='CASCADE'), nullable=False)
    img_url = db.Column(db.Text, nullable=False)

class MsgImg(db.Model):
    __tablename__ = "msgimg"
    id = db.Column(db.Integer, primary_key=True)
    msg_id = db.Column(db.Integer, db.ForeignKey('msg.msg_id'), nullable=False)
    img_url = db.Column(db.Text, nullable=False)

class AllPlants(db.Model):
    __tablename__ = "allplants"
    id = db.Column(db.Integer, primary_key=True)
    name_code = db.Column(db.String(100), nullable=True)
    accepted_name_code = db.Column(db.String(100), nullable=True)
    canonical_name = db.Column(db.String(255), nullable=False)
    genus = db.Column(db.String(255), nullable=False)
    genus_c = db.Column(db.String(255), nullable=False)
    species = db.Column(db.String(255), nullable=False)
    species_c = db.Column(db.String(255), nullable=False)


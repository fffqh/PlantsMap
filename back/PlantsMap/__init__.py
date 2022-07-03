import os
import click
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from PlantsMap.views.users import users_bp
from PlantsMap.views.maps import maps_bp
from PlantsMap.views.plants import plants_bp
from PlantsMap.views.images import images_bp
from PlantsMap.views.message import message_bp
from PlantsMap.views.home import home_bp

from PlantsMap.extensions import db , mail_obj, dropzone
from PlantsMap.settings import config
from PlantsMap.models import User, Map, Mnt, Plant, Msg, MapImg, PlantImg, MsgImg, AllPlants

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# 工厂函数：创建app
def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('PlantsMap') # 实例化app
    CORS(app, resources=r'/*',supports_credentials=True)	# 注册CORS, "/*" 允许访问所有api

    app.config.from_object(config[config_name]) # 配置app

    # 注册
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_shell_context_processors(app)
    return app

# 模块注册
def register_extensions(app):
    db.init_app(app)
    mail_obj.init_app(app)
    dropzone.init_app(app)

# 蓝图注册
def register_blueprints(app):
    app.register_blueprint(plants_bp, url_prefix='/api-fqh/plants')
    app.register_blueprint(users_bp, url_prefix='/api-fqh/users')
    app.register_blueprint(maps_bp, url_prefix='/api-fqh/maps')
    app.register_blueprint(images_bp, url_prefix='/api-fqh/images')
    app.register_blueprint(message_bp, url_prefix='/api-fqh/message')
    app.register_blueprint(home_bp, url_prefix='/api-fqh/home')

# 命令注册
def register_commands(app):
    @app.cli.command()
    def initdb():
        db.create_all()
        u = User(
            user_name='admin',
            user_email='admin@qq.com'
        )
        u.set_password('admin123')
        db.session.add(u)
        db.session.commit()
        click.echo("Initialized database.")

    @app.cli.command()
    def dropdb():
        db.drop_all()
        click.echo("Droped database.")

# 注册shell上下文钩子
def register_shell_context_processors(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User, Map=Map, Mnt=Mnt, Plant=Plant, AllPlants=AllPlants,
                    Msg=Msg, MapImg=MapImg, PlantImg=PlantImg, MsgImg=MsgImg)

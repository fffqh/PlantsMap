import re
import random 
import datetime
from flask import request, jsonify, session, make_response, Blueprint
from PlantsMap.extensions import db
from PlantsMap.models import User

from PlantsMap.mail import *

users_bp = Blueprint('users', __name__)

# 存放用户对应的验证码
mails_verified_list = {}

# 检查用户是否登录
@users_bp.route('/islogin', methods={'GET'})
def islogin():
    try:
        user_id = session.get('user_id')
        if user_id is None:
            return jsonify({'msg':'no'}), 200
        else:
            user = User.query.get(int(user_id))
            if user is None:
                return jsonify({'msg':'no'}), 200
            return jsonify({'msg':'yes', 'user_id':user_id, 'user_name':user.user_name}), 200
    except:
        return jsonify({'msg':'no'}), 200
    else:
        return jsonify({'msg':'no'}), 200


# 用户注册
@users_bp.route('/signup', methods={'POST'})
def signup():
    # 数据错误检查
    data = request.get_json()
    if(data.get('user_name') is None):
        return jsonify({'fault':'request data need user_name!'}), 400
    if(data.get('user_email') is None):
        return jsonify({'fault':'request data need user_email'}), 400
    if(data.get('user_verify') is None):
        return jsonify({'fault':'request data need user_verify'}), 400
    if(data.get('user_pwd') is None):
        return jsonify({'fault':'request data need user_pwd'}), 400
    
    # 判断name是否重复
    if User.query.filter_by(user_name=data['user_name']).first():
        return jsonify({'fault': 'user_name is invalid!'}), 401
    # 判断email是否重复
    if User.query.filter_by(user_email=data['user_email']).first():
        return jsonify({'fault': 'user_email is invalid!'}), 401
    # 判断验证码是否正确
    if data['user_email'] not in mails_verified_list.keys() or data['user_verify'] != \
            mails_verified_list[data['user_email']][0]:
        return jsonify({'fault': 'user_verify is invalid!'}), 403
    
    # 判断验证码是否超时，超过十分钟则失效
    min = (datetime.datetime.now() -
            mails_verified_list[data['user_email']][1]).seconds / 60
    if min > 10:
        return jsonify({'fault': 'user_verify is overdue!'}), 403
    
    # 创建新用户
    with db.auto_commit_db():
        u = User(user_name=data['user_name'],
                user_email=data['user_email'],
                user_status=True)
        u.set_password(data['user_pwd'])
        db.session.add(u)

    return jsonify({'msg':'ok'}), 201

# 用户登录
@users_bp.route('/login',  methods={'POST'})
def login():
    # 确定user_info
    email_str = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    data = request.get_json()
    if(data.get('user_info') is None ):
        return jsonify({'fault':'data request need user_info'}), 400
    if(data.get('user_pwd') is None):
        return jsonify({'fault':'data request need user_pwd'}), 400
    
    # 检查用户信息
    u = None
    if re.match(email_str, data['user_info']):
        u = User.query.filter_by(user_email=data['user_info']).first()
    else:
        u = User.query.filter_by(user_name=data['user_info']).first()
    # 用户信息检查
    if (u is None):
        return jsonify({'fault': 'user info error!'}), 401
    if (u.validate_password(data['user_pwd']) == False):
        return jsonify({'fault': 'user info error!'}), 401
    if (u.user_status == False):
        return jsonify({'fault': 'user is invalid!'}), 403

    # 登录成功
    # 登陆成功，在session中储存用户信息
    session['logged_in'] = True
    session['user_id'] = u.user_id
    session['user_name'] = u.user_name
    session['user_email'] = u.user_email
    response = make_response(jsonify({
        'msg':'ok','user_id': u.user_id, 
        'user_name': u.user_name, 'user_email':u.user_email}))
    response.set_cookie('user_id', str(u.user_id))
    response.set_cookie('user_name', u.user_name)
    return response, 200

# 用户登出
@users_bp.route('/logout', methods={'POST'})
def logout():
    if session.get('logged_in') is not None:
        session.pop('logged_in')
    if session.get('user_id') is not None:
        session.pop('user_id')
    if session.get('user_name') is not None:
        session.pop('user_name')
    if session.get('user_email') is not None:
        session.pop('user_email')
    response = jsonify({'info': 'successful logout'})
    response.delete_cookie('user_id')
    response.delete_cookie('user_name')
    return response, 200

# 获取验证码
@users_bp.route('/verify', methods={'POST'})
def verify():
    data = request.get_json() 
    code = ''.join(random.choice(
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        ) for _ in range(6))
    user_email = data['user_email']
    send_mail(user_email, '验证码', '您的验证码为' + code)
    # 记录验证码信息，前一个为验证码，后一个为验证码发出时的时间
    mails_verified_list[user_email] = (code, datetime.datetime.now())
    return jsonify({'msg':'ok'}), 200


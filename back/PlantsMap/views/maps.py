from flask import request, jsonify, session, make_response, Blueprint
from PlantsMap.extensions import db
from PlantsMap.models import User, Map, Plant, Mnt

maps_bp = Blueprint('maps', __name__)


@maps_bp.route('/allpoints', methods={'GET'})
def get_allpoints():
    # 取得数据
    map_lst = []
    map_objs = Map.query.all()
    for map_obj in map_objs:
        map_lst.append({'map_id'         :map_obj.map_id,
                        'map_create_time':map_obj.map_create_time,
                        'map_update_time':map_obj.map_update_time,
                        'map_user_id'    :map_obj.map_user_id,
                        'map_plant_id'   :map_obj.map_plant_id,
                        'map_plant_name' :map_obj.plant.plant_name,
                        'map_longitude'  :map_obj.map_longitude,
                        'map_latitude'   :map_obj.map_latitude,
                        'map_plant_num'  :map_obj.map_plant_num
                        })
    return jsonify({'msg':'ok', 'map':map_lst}), 200

@maps_bp.route('/userpoints', methods={'GET'})
def get_userpoints():
    # 检查用户权限
    try:
        if 'user_id' in session:
            user_id = int(session['user_id'])
        else:    
            print("用户未登录")
            return jsonify({'msg': '用户未登录'}), 403
    except:
        return jsonify({'msg':'用户id数据格式有误'}), 400
    else:
        # 取得数据
        map_lst = []
        map_objs = Map.query.filter_by(map_user_id=user_id).all()
        for map_obj in map_objs:
            map_lst.append({'map_id'        :map_obj.map_id,
                            'map_create_time':map_obj.map_create_time,
                            'map_update_time':map_obj.map_update_time,
                            'map_user_id'   :map_obj.map_user_id,
                            'map_plant_id'  :map_obj.map_plant_id,
                            'map_plant_name':map_obj.plant.plant_name,
                            'map_longitude' :map_obj.map_longitude,
                            'map_latitude'  :map_obj.map_latitude,
                            'map_plant_num' :map_obj.map_plant_num
                            })
        return jsonify({'msg':'ok', 'map':map_lst}), 200

@maps_bp.route('/addpoint', methods={'POST'})
def add_point():
    # 检查用户权限
    try:
        if 'user_id' in session:
            user_id = int(session['user_id'])
        else:    
            print("用户未登录")
            return jsonify({'msg':'用户未登录'}), 403
        data = request.get_json()
        if data.get('map_plant_name') is None:
            return jsonify({'msg': '未提交植物名称'}), 400
        if data.get('map_longitude') is None:
            return jsonify({'msg': '未提交经度'}), 400
        if data.get('map_latitude') is None:
            return jsonify({'msg': '未提交纬度'}), 400
        if data.get('map_plant_num') is None:
            return jsonify({'msg': '未提交植物数量'}), 400
        map_plant_name = str(data['map_plant_name'])
        map_longitude = str(data['map_longitude'])
        map_latitude = str(data['map_latitude'])
        map_plant_num = int(data['map_plant_num'])
    except:
        return jsonify({'msg':'提交数据有误，请检查'}), 400
    else:
        # 查找植物名称是否在数据库中
        p = Plant.query.filter_by(plant_name=map_plant_name).first()
        if p is None:
            return jsonify({'msg':'not_in_hub'}), 200
        # 将地图点加入数据库
        map_obj = Map(  map_user_id=user_id,
                        map_plant_id=p.plant_id,
                        map_longitude=map_longitude,
                        map_latitude=map_latitude,
                        map_plant_num=map_plant_num)
        db.session.add(map_obj)
        db.session.commit()
        # 将维护信息加入数据库
        mnt_obj = Mnt(mnt_type=0, mnt_user_id=user_id, mnt_map_id=map_obj.map_id)
        db.session.add(mnt_obj)
        db.session.commit()
        return jsonify({'msg':'ok', 'map_plant_id':p.plant_id, 'map_id':map_obj.map_id}), 201

@maps_bp.route('/mnts', methods={'POST'})
def get_mnts():
    try:
        map_id = int(request.get_json().get('map_id'))
    except:
        return jsonify({'msg':'数据格式错误'}), 400
    else:
        mnt_objs = Mnt.query.filter_by(mnt_map_id=map_id).order_by(Mnt.mnt_time.desc()).all()
        mnt_list = []
        for mnt in mnt_objs:
            user_name = '未知'
            user = User.query.get(mnt.mnt_user_id)
            if user is not None:
                user_name = user.user_name
            if mnt.mnt_type == 0:
                mnt_list.append({'mnt_time':mnt.mnt_time, 'mnt_type':'创建','mnt_user_name':user_name})
            else:
                mnt_list.append({'mnt_time':mnt.mnt_time, 'mnt_type':'更新','mnt_user_name':user_name})
        return jsonify({'msg':'ok', 'mnts':mnt_list}), 200


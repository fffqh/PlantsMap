import os
from flask import request, jsonify, session, Blueprint, send_from_directory, send_file, make_response
from flask import current_app
from PlantsMap.extensions import db
from PlantsMap.models import User, Map, Plant
from sqlalchemy import extract, and_

home_bp = Blueprint('home', __name__)

@home_bp.route('/points', methods={'POST'})
def get_user_points():
    try:
        user_id = session.get('user_id')
        if user_id is None:
            return jsonify({'msg':'用户未登录'}), 403
        user_id = int(user_id)
        data = request.get_json()
        page_index = int(data['page_index'])
        page_size = int(data['page_size'])
        home_user_id = int(data['user_id'])
    except:
        return jsonify({'msg':'数据格式错误'}), 400
    else:
        u = User.query.get(home_user_id)
        if u is None:
            return jsonify({'msg':'用户不存在'}), 404
        maps_pg = Map.query.filter_by(map_user_id=home_user_id).paginate(page=page_index, per_page=page_size)
        maps_objs = maps_pg.items
        maps_lst = []
        for m in maps_objs:
            map_plant_name = '未知'
            map_plant = Plant.query.get(m.map_plant_id)
            map_plant_name = map_plant.plant_name
            maps_lst.append({'map_id':m.map_id,'map_plant_id':m.map_plant_id,
                            'map_plant_name':map_plant_name, 
                            'map_create_time':m.map_create_time,
                            'map_update_time':m.map_update_time,
                            'map_longitude':m.map_longitude,
                            'map_latitude':m.map_latitude,
                            'map_plant_num':m.map_plant_num})
        return jsonify({'msg':'ok', 'total': maps_pg.total, 'data':maps_lst}), 200

# 取得用户某天的植物数量
@home_bp.route('/day_points_num', methods={'POST'})
def get_day_point_num():
    try:
        user_id = session.get('user_id')
        if user_id is None:
            return jsonify({'msg':'用户未登录'}), 403
        data = request.get_json()
        data_user_id = int(data['user_id'])
        year = int(data['year'])
        month = int(data['month'])
        day = int(data['day'])
    except:
        return jsonify({'msg':'数据格式错误'}), 400
    else:
        # 查询data_user_id是否存在
        data_user = User.query.get(data_user_id)
        if data_user is None:
            return jsonify({'msg':'查询的用户不存在'}), 404
        # 查询植物地图点的数量
        points = Map.query.filter(and_(
            Map.map_user_id == data_user_id,
            extract('year', Map.map_create_time) == year,
            extract('month', Map.map_create_time) == month,
            extract('day', Map.map_create_time) == day
        )).all()
        for p in points:
            print(p)
        try:
            point_num = len(points)
        except:
            return jsonify({'msg':'fail'}), 404
        else:
            return jsonify({'msg':'ok', 'num':point_num}), 200

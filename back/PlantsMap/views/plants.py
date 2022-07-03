import base64
from flask import request, jsonify, session, make_response, Blueprint
from PlantsMap.extensions import db
from PlantsMap.models import Plant, AllPlants

plants_bp = Blueprint('plants', __name__)

# 获取植物信息列表
@plants_bp.route('/get_plants', methods={'GET'})
def get_plants():
    plst = Plant.query.all()
    pjson = []
    for p in plst:
        pjson.append({'plant_id':p.plant_id, 'plant_name':p.plant_name, 'plant_attr':p.plant_attr})
    return jsonify({'msg':'ok','count':len(pjson),'data':pjson}), 200

# 分页获取植物信息列表
@plants_bp.route('/page', methods=['POST'])
def get_plants_page():
    try:
        data = request.get_json()
        page_index = int(data['page_index'])
        page_size = int(data['page_size'])
    except:
        return jsonify({'msg':'数据格式错误'}), 400
    else:
        plants_pg = Plant.query.paginate(page=page_index, per_page=page_size)
        plants_objs = plants_pg.items
        plants_lst = []
        for p in plants_objs:
            plants_lst.append({'plant_id':p.plant_id,'plant_name':p.plant_name, 'plant_attr':p.plant_attr})
        return jsonify({'msg':'ok', 'total':plants_pg.total, 'data':plants_lst}), 200


# 添加植物信息
@plants_bp.route('/add_plant', methods={'POST'})
def add_plant():
    # 检查用户权限
    try:
        if 'user_id' in session:
            user_id = int(session['user_id'])
        else:
            return jsonify({'msg':'用户未登录'}), 403
        data = request.get_json()
        if data.get('plant_name') is None:
            return jsonify({'msg':'未提交植物名称'}), 400
        plant_name = str(data['plant_name'])
        plant_attr = ''
        if data.get('plant_attr') is not None:
            plant_attr = str(data['plant_attr'])
    except:
        return jsonify({'msg':'数据格式有误'}), 400
    else:
        p = Plant(plant_name=plant_name)
        if plant_attr != '':
            p.plant_attr = plant_attr
        db.session.add(p)
        db.session.commit()
        return jsonify({'plant_id':p.plant_id, 'plant_name':p.plant_name}), 201

# 添加植物信息（带有检查）
@plants_bp.route('/check/add_plant', methods={'POST'})
def add_plant_with_check():
    # 检查用户权限
    try:
        if 'user_id' in session:
            user_id = int(session['user_id'])
        else:
            return jsonify({'msg':'用户未登录'}), 403
        data = request.get_json()
        if data.get('plant_name') is None:
            return jsonify({'msg':'未提交植物名称'}), 400
        plant_name = str(data['plant_name'])
        plant_attr = ''
        if data.get('plant_attr') is not None:
            plant_attr = str(data['plant_attr'])
    except:
        return jsonify({'msg': '数据格式有误'}), 400
    else:
        # 检查AllPlants中是否有
        p = AllPlants.query.filter_by(species_c=plant_name).first()
        if p is None:
            return jsonify({'msg':'fail'}), 200
        # 检查Plant中是否有
        oldp = Plant.query.filter_by(plant_name = plant_name).first()
        if oldp is not None:
            return jsonify({'msg': 're_add', 'data': {  'canonical_name': p.canonical_name,
                                                        'genus': p.genus, 'genus_c': p.genus_c,
                                                        'species': p.species,
                                                        'species_c': p.species_c}}), 200
        
        addp = Plant(plant_name=p.species_c, 
                    plant_attr=p.genus_c + '。' + plant_attr)
        db.session.add(addp)
        db.session.commit()
        return jsonify({'msg':'ok', 'data':{'canonical_name':p.canonical_name, 
                                            'genus':p.genus, 'genus_c':p.genus_c,
                                            'species':p.species, 
                                            'species_c':p.species_c}}), 201


@plants_bp.route('/del_plant', methods={'POST'})
def del_plant():
    pass

# 根据植物名称搜索植物
@plants_bp.route('/search_plant',methods={'POST'})
def search_plant():
    try:
        data = request.get_json()
        if(data.get('keyword') is None):
            return jsonify({'msg':'未提交搜索关键字'}), 400
        keyword = data['keyword']
    except:
        return jsonify({'msg':'数据格式有误'}), 400
    else:
        result = []
        if keyword == "":
            return jsonify({'msg':'ok', 'result':result}), 200
        p_objs = Plant.query.filter(
            Plant.plant_name.like('%'+keyword +'%') 
        ).all()
        for p in p_objs:
            result.append({'plant_id':p.plant_id, 'plant_name':p.plant_name})
        return jsonify({'msg':'ok', 'result':result}), 200


# 根据植物名称或属性搜索植物，并分页返回
@plants_bp.route('/search/page', methods={'POST'})
def search_page():
    try:
        data = request.get_json()
        srh_type = int(data['search_type'])
        srh_keyword = str(data['search_keyword'])
        srh_page_index = int(data['search_page_index'])
        srh_page_size = int(data['search_page_size'])
    except:
        return jsonify({'msg':'数据格式有误'}), 400
    else:
        plants_lst = []
        if srh_keyword == "":
            return jsonify({'msg':'ok', 'total':0, 'data':plants_lst}), 200
        # 进行搜索
        if srh_type == 1:
            plants_pg = Plant.query.filter(
                Plant.plant_name.like('%'+srh_keyword+'%')
            ).paginate(page=srh_page_index, per_page=srh_page_size)
        elif srh_type == 2:
            plants_pg = Plant.query.filter(
                Plant.plant_attr.like('%'+srh_keyword+'%')
            ).paginate(page=srh_page_index, per_page=srh_page_size)
        else:
            return jsonify({'msg': '数据格式有误'}), 400
        # 处理搜索结果
        plants_objs = plants_pg.items
        for p in plants_objs:
            plants_lst.append({'plant_id':p.plant_id, 'plant_name':p.plant_name, 'plant_attr':p.plant_attr})
        return jsonify({'msg': 'ok', 'total': plants_pg.total, 'data': plants_lst}), 200

@plants_bp.route('/search', methods={'POST'})
def search():
    try:
        data = request.get_json()
        srh_type = int(data['search_type'])
        srh_keyword = str(data['search_keyword'])
    except:
        return jsonify({'msg': '数据格式有误'}), 400
    else:
        plants_lst = []
        if srh_keyword == "":
            return jsonify({'msg': 'ok', 'total': 0, 'data': plants_lst}), 200
        # 进行搜索
        if srh_type == 1:
            plants_objs = Plant.query.filter(
                Plant.plant_name.like('%'+srh_keyword+'%')
            ).all()
        elif srh_type == 2:
            plants_objs = Plant.query.filter(
                Plant.plant_attr.like('%'+srh_keyword+'%')
            ).all()
        else:
            return jsonify({'msg': '数据格式有误'}), 400
        # 处理搜索结果
        for p in plants_objs:
            plants_lst.append(
                {'plant_id': p.plant_id, 'plant_name': p.plant_name, 'plant_attr': p.plant_attr})
        return jsonify({'msg': 'ok', 'total': len(plants_objs), 'data': plants_lst}), 200

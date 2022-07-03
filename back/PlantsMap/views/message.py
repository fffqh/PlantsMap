from flask import request, jsonify, session, make_response, Blueprint
from PlantsMap.extensions import db
from PlantsMap.models import User, Map, Mnt, Msg

message_bp = Blueprint('message', __name__)

# 发送信息
@message_bp.route('/addmsg', methods={'POST'})
def addmsg():
    try:
        user_id = session.get('user_id')
        if user_id is None:
            return jsonify({'msg':'用户未登录'}), 403
        user_id = int(user_id)
        data = request.get_json()
        map_id = int(data['map_id'])
        msg_type = int(data['mnt_type'])
        msg_txt = str(data['mnt_desc'])
    except:
        return jsonify({'msg':'数据格式错误'}), 400        
    else:
        # 查询 map_id 是否存在
        map_obj = Map.query.get(map_id)
        if map_obj is None:
            return jsonify({'msg':'维护的地图点不存在'}), 404
        # 检查输入是否过长
        if len(msg_txt) > 250:
            return jsonify({'msg':'维护信息过长'}), 400
        # 取得to_user_id，检查用户是否存在
        touser_id = map_obj.map_user_id
        touser_obj = User.query.get(map_obj.map_user_id)
        if touser_obj is None:
            admin_obj = User.query.filter(user_name='admin').first()
            if admin_obj is None:
                return jsonify({'msg':'地图点的创建者不存在，且管理员不存在'}), 404
            touser_id = admin_obj.user_id
        # 更新 msg 数据表
        msg_obj = Msg(msg_from=user_id, msg_to=touser_id, msg_map_id=map_id, msg_type = msg_type, msg_txt=msg_txt)
        db.session.add(msg_obj)
        db.session.commit()
        return jsonify({'msg':'ok', 'msg_id':msg_obj.msg_id}), 201

# 分页获取收件箱列表
@message_bp.route('/recv_page', methods=['POST'])
def get_recv_page():
    # data = request.get_json()
    # print('get_recv:', data)
    try:
        user_id = session.get('user_id')
        if user_id is None:
            return jsonify({'msg':'用户未登录'}), 403
        user_id = int(user_id)
        data = request.get_json()
        page_index = int(data['page_index'])
        page_size = int(data['page_size'])
    except:
        return jsonify({'msg':'数据格式错误'}), 400
    else:
        msg_pg = Msg.query.filter_by(msg_to=user_id)\
                    .order_by(Msg.msg_time.desc()).paginate(page=page_index, per_page=page_size)
        msg_objs = msg_pg.items 
        msg_lst = []
        for msg in msg_objs:
            u = User.query.get(msg.msg_from)
            from_u_name = '已注销'
            if u is not None:
                from_u_name = u.user_name
            msg_type_dict = {1:'创建',2:'更新',3:'确认',4:'删除'}
            msg_lst.append({'msg_id':msg.msg_id, 'msg_time':msg.msg_time, 
                            'msg_from':from_u_name, 'msg_map_id':msg.msg_map_id, 
                            'msg_type':msg_type_dict[msg.msg_type], 
                            'msg_txt':msg.msg_txt, 'msg_status':msg.msg_status})
        return jsonify({'msg':'ok', 'total':msg_pg.total, 'data':msg_lst}), 200


# 分页获取发件箱列表
@message_bp.route('/send_page', methods=['POST'])
def get_send_page():
    try:
        user_id = session.get('user_id')
        if user_id is None:
            return jsonify({'msg':'用户未登录'}), 403
        data = request.get_json()
        user_id = int(user_id)
        page_index = int(data['page_index'])
        page_size = int(data['page_size'])
    except Exception as ex:
        return jsonify({'msg': '数据格式错误'}), 400
    else:
        msg_pg = Msg.query.filter_by(msg_from=user_id)\
                    .order_by(Msg.msg_time.desc()).paginate(page=page_index, per_page=page_size)
        msg_objs = msg_pg.items
        msg_lst = []
        for msg in msg_objs:
            u = User.query.get(msg.msg_to)
            to_u_name = '已注销'
            if u is not None:
                to_u_name = u.user_name
            msg_type_dict = {1: '创建', 2: '更新', 3: '确认', 4: '错误'}
            msg_lst.append({'msg_id': msg.msg_id, 'msg_time': msg.msg_time,
                            'msg_to': to_u_name , 'msg_map_id': msg.msg_map_id,
                            'msg_type': msg_type_dict[msg.msg_type],
                            'msg_txt': msg.msg_txt, 'msg_status':msg.msg_status})
        return jsonify({'msg': 'ok', 'total': msg_pg.total, 'data': msg_lst}), 200


# 接受信息并将维护历史加入mnt表中
@message_bp.route('/accept', methods={'POST'})
def accept_msg():
    try:
        user_id = session.get('user_id')
        if user_id is None:
            return jsonify({'msg':'用户未登录'}), 403
        user_id = int(user_id)
        data = request.get_json()
        msg_id = int(data['msg_id'])
    except:
        return jsonify({'msg':'数据格式错误'}), 400
    else:
        # 用户id与msg_to是否匹配
        msg_obj = Msg.query.get(msg_id)
        if user_id != msg_obj.msg_to:
            return jsonify({'msg':'用户操作权限不足'}), 404
        mnt_obj = Mnt(  mnt_time = msg_obj.msg_time, mnt_type = msg_obj.msg_type,
                        mnt_text = msg_obj.msg_txt, mnt_user_id = msg_obj.msg_from, 
                        mnt_map_id = msg_obj.msg_map_id)
        with db.auto_commit_db():
            db.session.add(mnt_obj)
            msg_obj.msg_status = 'accept'
        return jsonify({'msg':'ok'}), 201

# 拒绝信息
@message_bp.route('/reject', methods={'POST'})
def reject_msg():
    try:
        user_id = session.get('user_id')
        if user_id is None:
            return jsonify({'msg': '用户未登录'}), 403
        user_id = int(user_id)
        data = request.get_json()
        msg_id = int(data['msg_id'])
    except:
        return jsonify({'msg': '数据格式错误'}), 400
    else:
        # 用户id与msg_to是否匹配
        msg_obj = Msg.query.get(msg_id)
        if user_id != msg_obj.msg_to:
            return jsonify({'msg': '用户操作权限不足'}), 404
        msg_obj.msg_status = 'reject'
        db.session.commit()
        return jsonify({'msg':'ok'}), 201


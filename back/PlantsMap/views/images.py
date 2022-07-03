import os
from flask import request, jsonify, session, Blueprint,send_from_directory, send_file, make_response
from flask_dropzone import random_filename
from flask import current_app
from PlantsMap.extensions import db
from PlantsMap.models import Map, Msg, MapImg, PlantImg, MsgImg

images_bp = Blueprint('images', __name__)


@images_bp.route('/msg_upload', methods={'POST'})
def msg_upload():
    # 检查用户权限
    try:
        # print(request.form)
        user_id = session.get('user_id')
        if user_id is None:
            return jsonify({'msg': '用户未登录'}), 403
        msg_id = request.form.get('msg_id')
        if msg_id is None:
            return jsonify({'msg': '需要msg_id字段'}), 400
        msg_id = int(msg_id)
        f = request.files.get("file")
        if f is None:
            return jsonify({'msg': '需要file字段'}), 400
    except:
        return jsonify({'msg': '数据格式有误'}), 400
    else:
        #查询msg_id是否有效且用户拥有权限
        msg_obj = Msg.query.get(msg_id)
        if msg_obj is None:
            return jsonify({'msg': '地图点不存在'}), 404
        if user_id != msg_obj.msg_from:
            return jsonify({'msg': '用户没有该信息的权限'}), 403

        # 获取一个随机的文件名称
        filename = random_filename(f.filename)
        fileurl = os.path.join(
            current_app.config['IMAGE_UPLOAD_PATH'], filename)
        # 保存文件
        f.save(fileurl)

        with db.auto_commit_db():
            # 将文件记录插入数据库钟
            msgimg = MsgImg(msg_id=msg_id, img_url=fileurl)
            db.session.add(msgimg)
        return jsonify({'msg': 'ok'}), 201


@images_bp.route('/map_upload', methods={'POST'})
def map_upload():
    # 检查用户权限
    try:
        print(request.form)
        user_id = session.get('user_id')
        if user_id is None:
            return jsonify({'msg':'用户未登录'}), 403
        map_id = request.form.get('map_id')
        if map_id is None:
            return jsonify({'msg':'需要map_id字段'}),400
        map_id = int(map_id)
        f = request.files.get("file")
        if f is None:
            return jsonify({'msg':'需要file字段'}),400
    except:
        return jsonify({'msg':'数据格式有误'}), 400
    else:
        #查询map_id是否有效且用户拥有权限
        map_obj = Map.query.get(map_id)
        if map_obj is None:
            return jsonify({'msg':'地图点不存在'}), 404
        if user_id != map_obj.map_user_id:
            return jsonify({'msg':'用户没有该地图点的编辑权限'}), 403
        
        # 获取一个随机的文件名称
        filename = random_filename(f.filename)
        fileurl = os.path.join(current_app.config['IMAGE_UPLOAD_PATH'], filename)
        # 保存文件
        f.save(fileurl)

        with db.auto_commit_db():
            # 将文件记录插入数据库钟
            mapimg = MapImg(map_id=map_id, img_url=fileurl)
            db.session.add(mapimg)
        return jsonify({'msg':'ok'}), 201

@images_bp.route('/get_mapimgs', methods={'POST'})
def get_map_imgs():
    try:
        data = request.get_json()
        map_id = int(data['map_id'])
    except:
        return jsonify({'msg':'数据格式错误'}), 400
    else:
        mapimgs = MapImg.query.filter_by(map_id=map_id).all()
        images_id = []
        for mapimg in mapimgs:
            images_id.append(mapimg.id)
        return jsonify({'msg':'ok', 'images_id':images_id}), 200

@images_bp.route('/get_msgimgs', methods={'POST'})
def get_msg_imgs():
    try:
        data = request.get_json()
        msg_id = int(data['msg_id'])
    except:
        return jsonify({'msg':'数据格式错误'}), 400
    else:
        msgimgs = MsgImg.query.filter_by(msg_id=msg_id).all()
        images_id = []
        for msgimg in msgimgs:
            images_id.append(msgimg.id)
        return jsonify({'msg':'ok', 'images_id':images_id}), 200


@images_bp.route('/msgimg/<image_id>', methods={'GET'})
def msg_images(image_id):
    image_id = int(image_id)
    msgimg = MsgImg.query.get(image_id)
    if msgimg is None:
        return jsonify({'msg':'图片不存在'}), 404
    img_path = msgimg.img_url
    return make_response(send_from_directory(os.path.dirname(img_path), os.path.basename(img_path))), 200


@images_bp.route('/<image_id>', methods={'GET'})
def images(image_id):
    mapimg = MapImg.query.get(image_id)
    if mapimg is None:
        return jsonify({'msg':'图片不存在'}), 404
    img_path = mapimg.img_url
    return make_response(send_from_directory(os.path.dirname(img_path), os.path.basename(img_path))), 200

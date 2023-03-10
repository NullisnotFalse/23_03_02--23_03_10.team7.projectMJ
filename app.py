from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.wtgzda4.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

from bson import ObjectId
from datetime import datetime
import pytz


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/popup/<int:i>')
def popup(i):
    return render_template('popup.html',num=i)

@app.route('/edit/<int:i>')
def edit(i):
    return render_template('edit.html',num=i)

@app.route('/map/<string:address>')
def map(address):
    return render_template('map.html',address=address)


@app.route("/comment", methods=["POST"])
def save_comment():
    name_receive = request.form['name_give']
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    menu_receive = request.form['menu_give']
    address_receive = request.form['address_give']
    comment_receive = request.form['comment_give']
    tag_receive = request.form['tag_give']
    password_receive = request.form['password_give']

    time_zone = pytz.timezone('Asia/Seoul')
    current_time = datetime.now(time_zone).strftime("%y-%m-%d %H:%M")

    doc = {
        'name': name_receive,
        'url': url_receive,
        'star': star_receive,
        'menu': menu_receive,
        'address': address_receive,
        'comment': comment_receive,
        'tag': tag_receive,
        'password': password_receive,
        'time': current_time
    }
    db.projectMJ.insert_one(doc)

    return jsonify({'msg': '등록 완료'})


@app.route("/comment", methods=["GET"])
def get_comment_list():
    comment_list = list(db.projectMJ.find({},{'_id':False}))

    return jsonify({'comment_list': comment_list})


@app.route("/comment/<int:i>", methods=["GET"])
def get_comment(i):
    comment = list(db.projectMJ.find({}, {'_id': False}))[i]

    return jsonify({'comment': comment})


@app.route("/comment/<int:i>", methods=["PUT"])
def edit_comment(i):
    name_receive = request.form['name_give']
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    menu_receive = request.form['menu_give']
    address_receive = request.form['address_give']
    comment_receive = request.form['comment_give']
    tag_receive = request.form['tag_give']
    password_receive = request.form['password_give']

    edit_doc = {
        'name': name_receive,
        'url': url_receive,
        'star': star_receive,
        'menu': menu_receive,
        'address': address_receive,
        'comment': comment_receive,
        'tag': tag_receive,
        'password': password_receive
    }

    comment_list = []
    for doc in db.projectMJ.find():
        doc['_id'] = str(doc['_id'])
        comment_list.append(doc)

    if comment_list[i]['password'] == password_receive:
        db.projectMJ.update_one({'_id': ObjectId(comment_list[i]['_id'])}, {'$set': edit_doc})
        return jsonify({'msg': '수정 완료', 'reload':'1'})
    else:
        return jsonify({'msg': '비밀번호가 일치하지 않습니다.', 'reload':'0'})


@app.route("/comment/<int:i>", methods=["DELETE"])
def delete_comment(i):
    password_receive = request.form['password_give']

    comment_list = []
    for doc in db.projectMJ.find():
        doc['_id'] = str(doc['_id'])
        comment_list.append(doc)

    if comment_list[i]['password'] == password_receive:
        db.projectMJ.delete_one({'_id': ObjectId(comment_list[i]['_id'])})
        db.reply.delete_many({'id': comment_list[i]['_id']})
        return jsonify({'msg': '삭제 완료', 'reload':'1'})
    else:
        return jsonify({'msg': '비밀번호가 일치하지 않습니다.', 'reload': '0'})


@app.route("/reply/<int:i>", methods=["POST"])
def save_reply(i):
    reply_receive = request.form['reply_give']
    reply_name_receive = request.form['reply_name_give']
    reply_password_receive = request.form['reply_password_give']

    time_zone = pytz.timezone('Asia/Seoul')
    current_time = datetime.now(time_zone).strftime("%m-%d %H:%M")

    comment_list = []
    for doc in db.projectMJ.find():
        doc['_id'] = str(doc['_id'])
        comment_list.append(doc)

    index_id = comment_list[i]['_id']

    doc = {
        'id': index_id,
        'reply': reply_receive,
        'reply_name': reply_name_receive,
        'reply_password': reply_password_receive,
        'reply_time': current_time
    }
    db.reply.insert_one(doc)

    return jsonify({'msg': '작성 완료'})


@app.route("/reply/<int:i>", methods=["GET"])
def get_reply_list(i):
    comment_list = []
    for doc in db.projectMJ.find():
        doc['_id'] = str(doc['_id'])
        comment_list.append(doc)

    index_id = comment_list[i]['_id']

    temp_reply_list = []
    for doc in db.reply.find():
        doc['_id'] = str(doc['_id'])
        temp_reply_list.append(doc)

    reply_list = [doc for doc in temp_reply_list if doc['id'] == index_id]

    return jsonify({'reply_list': reply_list})


@app.route("/reply/<int:i>", methods=["DELETE"])
def delete_reply(i):
    i_receive = request.form['i_give']
    check_id_receive = request.form['check_id_give']
    relpy_pw_check_receive = request.form['relpy_pw_check_give']

    comment_list = []
    for doc in db.projectMJ.find():
        doc['_id'] = str(doc['_id'])
        comment_list.append(doc)

    index_id = comment_list[i]['_id']

    temp_reply_list = []
    for doc in db.reply.find():
        doc['_id'] = str(doc['_id'])
        temp_reply_list.append(doc)

    reply_list = [doc for doc in temp_reply_list if doc['id'] == index_id]

    if reply_list[int(i_receive)]['reply_password'] == relpy_pw_check_receive:
        db.reply.delete_one({'_id': ObjectId(check_id_receive)})
        return jsonify({'msg': '삭제 완료', 'reload': '1'})
    else:
        return jsonify({'msg': '비밀번호가 일치하지 않습니다.', 'reload': '0'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
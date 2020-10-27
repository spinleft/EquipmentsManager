# -*- coding : utf-8 -*-
# coding: utf-8

from flask import *
from werkzeug.utils import secure_filename
import pymysql
from app import app, db
from config import basedir
import os


@app.route('/')
@app.route('/index')
def index():
    items = [{"zh": "详细信息", "en": "info"}, {"zh": "数量统计", "en": "equipnum"}]
    return render_template("index.html",
                           title='首页',
                           items=items)


@app.route('/info', methods=['GET', 'POST'])
def info():
    cursor = db.cursor()
    filter = {}
    if request.method == 'POST':
        print(request.form)
        op = request.form['提交']
        if op == '筛选':
            columns = ['类型', '名称', '型号', '序列号', '合同号', '到货时间', '经办人', '状态', '存放位置']
            count = 0
            sql = "select * from `详情` where "
            for column in columns:
                filter[column] = request.form[column]
                if request.form[column]:
                    if count > 0:
                        sql = sql + " and "
                    sql = sql + "`" + column + "` like \'%" + \
                        request.form[column] + "%\'"
                    count = count + 1
            if count == 0:
                sql = "select * from `详情`"
            cursor.execute(sql)
            records = cursor.fetchall()
        elif op == '插入':
            new_form = fixform(request.form)
            if request.files['合同文件1']:
                new_form['合同文件'] = ""
                i = 1
                while request.files['合同文件' + str(i)]:
                    f = request.files['合同文件' + str(i)]
                    upload_path = os.path.join(
                        basedir, 'app/static/uploads',
                        new_form['名称']+'-'+new_form['型号']+'-'+new_form['序列号'], secure_filename(f.filename))
                    upload_dir = os.path.dirname(upload_path)
                    if not os.path.exists(upload_dir):
                        os.mkdir(upload_dir)
                    f.save(upload_path)
                    new_form['合同文件'] = new_form['合同文件'] + secure_filename(f.filename) + ";"
                    i = i + 1
            else:
                new_form['合同文件'] = None

            if request.files['照片']:
                f = request.files['照片']
                upload_path = os.path.join(
                    basedir, 'app/static/uploads',
                    new_form['名称']+'-'+new_form['型号']+'-'+new_form['序列号'], secure_filename(f.filename))
                upload_dir = os.path.dirname(upload_path)
                if not os.path.exists(upload_dir):
                    os.mkdir(upload_dir)
                f.save(upload_path)
                new_form['照片'] = os.path.join(
                    'static/uploads',
                    new_form['名称']+'-'+new_form['型号']+'-'+new_form['序列号'], secure_filename(f.filename))
            else:
                new_form['照片'] = None
            
            if request.files['位置照片']:
                f = request.files['位置照片']
                upload_path = os.path.join(
                    basedir, 'app/static/uploads',
                    new_form['名称']+'-'+new_form['型号']+'-'+new_form['序列号'], secure_filename(f.filename))
                upload_dir = os.path.dirname(upload_path)
                if not os.path.exists(upload_dir):
                    os.mkdir(upload_dir)
                f.save(upload_path)
                new_form['位置照片'] = os.path.join(
                    'static/uploads',
                    new_form['名称']+'-'+new_form['型号']+'-'+new_form['序列号'], secure_filename(f.filename))
            else:
                new_form['位置照片'] = None
            cursor.execute("""
                        insert into `详情`(`类型`, `名称`, `型号`, `序列号`, `合同号`, `到货时间`, `经办人`, `状态`, `存放位置`, `合同文件`, `照片`, `位置照片`, `备注`) 
                        values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        [new_form['类型'], new_form['名称'], new_form['型号'],
                            new_form['序列号'], new_form['合同号'], new_form['到货时间'],
                            new_form['经办人'], new_form['状态'], new_form['存放位置'],
                            new_form['合同文件'], new_form['照片'], new_form['位置照片'],
                            new_form['备注']])
            db.commit()
            cursor.execute("select * from `详情`")
            records = cursor.fetchall()
    else:
        cursor.execute("select * from `详情`")
        records = cursor.fetchall()
    for record in records:
        if record[9]:
            record[9] = record[9].split(";")
    return render_template("info.html",
                        title='详细信息',
                        records=records,
                        filter=filter)


@app.route('/operate', methods=['POST'])
def operate():
    cursor = db.cursor()
    op = request.form['op']
    if op == '删除':
        cursor.execute("select * from `详情` where `名称`=%s and `型号`=%s and `序列号`=%s",
                       [request.form['名称'], request.form['型号'], request.form['序列号']])
        records = cursor.fetchall()
        return render_template("operate.html",
                               title='删除',
                               records=records,
                               type='删除')
    elif op == '修改':
        cursor.execute("select * from `详情` where `名称`=%s and `型号`=%s and `序列号`=%s",
                       [request.form['名称'], request.form['型号'], request.form['序列号']])
        records = cursor.fetchall()
        return render_template("operate.html",
                               title='修改',
                               records=records,
                               type='修改')
    else:
        info()


@app.route('/dbop', methods=['POST'])
def dbop():
    cursor = db.cursor()
    op = request.form['op']
    if op == '确认删除':
        cursor.execute("select * from `详情` where `名称`=%s and `型号`=%s and `序列号`=%s",
                       [request.form['名称'], request.form['型号'], request.form['序列号']])
        record = cursor.fetchone()
        file_relative_path = record[8]
        cursor.execute("delete from `详情` where `名称`=%s and `型号`=%s and `序列号`=%s",
                       [request.form['名称'], request.form['型号'], request.form['序列号']])
        db.commit()
        if request.form['del_file'] == 'yes':
            file_path = os.path.join(basedir, 'app', file_relative_path)
            os.remove(file_path)
    elif op == '确认修改':
        if request.form['del_file'] == 'yes':
            cursor.execute("select * from `详情` where `名称`=%s and `型号`=%s and `序列号`=%s",
                           [request.form['名称'], request.form['型号'], request.form['序列号']])
            record = cursor.fetchone()
            file_relative_path = record[8]
        new_form = fixform(request.form)
        if request.files['file']:
            f = request.files['file']
            upload_path = os.path.join(
                basedir, 'app/static/uploads',
                new_form['名称']+'-'+new_form['型号']+'-'+new_form['序列号']+'-'+secure_filename(f.filename))
            f.save(upload_path)
            new_form['合同文件'] = os.path.join(
                'static/uploads',
                new_form['名称']+'-'+new_form['型号']+'-'+new_form['序列号']+'-'+secure_filename(f.filename))
        else:
            new_form['合同文件'] = None
        cursor.execute("""
                       update `详情` set `类型`=%s, `名称`=%s, `型号`=%s, `序列号`=%s,  
                       `合同号`=%s, `到货时间`=%s, `状态`=%s, `存放位置`=%s, `合同文件`=%s 
                       where `名称`=%s and `型号`=%s and `序列号`=%s
                       """,
                       [new_form['类型'], new_form['名称'], new_form['型号'],
                        new_form['序列号'], new_form['合同号'], new_form['到货时间'],
                        new_form['状态'], new_form['存放位置'], new_form['合同文件'],
                        request.form['原名称'], request.form['原型号'], request.form['原序列号']])
        db.commit()
        if request.form['del_file'] == 'yes':
            file_path = os.path.join(basedir, 'app', file_relative_path)
            os.remove(file_path)
    elif op == '插入':
        new_form = fixform(request.form)
        if request.files['file']:
            f = request.files['file']
            upload_path = os.path.join(
                basedir, 'app/static/uploads',
                new_form['名称']+'-'+new_form['型号']+'-'+new_form['序列号']+'-'+secure_filename(f.filename))
            f.save(upload_path)
            new_form['合同文件'] = os.path.join(
                'static/uploads',
                new_form['名称']+'-'+new_form['型号']+'-'+new_form['序列号']+'-'+secure_filename(f.filename))
        else:
            new_form['合同文件'] = None
        cursor.execute("""
                       insert into `详情`(`类型`, `名称`, `型号`, `序列号`, `合同号`, `到货时间`, `状态`, `存放位置`, `合同文件`, `照片`, `位置照片`, `备注`) 
                       values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                       """,
                       [new_form['类型'], new_form['名称'], new_form['型号'],
                        new_form['序列号'], new_form['合同号'], new_form['到货时间'], 
                        new_form['状态'], new_form['存放位置'], new_form['合同文件']])
        db.commit()
    elif op == '筛选':
        columns = ['类型', '名称', '型号', '序列号', '合同号', '到货时间', '状态', '存放位置']
        filter = {}
        count = 0
        sql = "select * from `详情` where "
        for column in columns:
            filter[column] = request.form[column]
            if request.form[column]:
                if count > 0:
                    sql = sql + " and "
                sql = sql + "`" + column + "` like \'%" + \
                    request.form[column] + "%\'"
                count = count + 1
        if count == 0:
            sql = "select * from `详情`"
        cursor.execute(sql)
        records = cursor.fetchall()
        return render_template("info.html",
                               title='详细信息',
                               records=records,
                               filter=filter)
    else:
        pass
    return info()


def fixform(form):
    columns = ['类型', '名称', '型号', '序列号', '合同号', '到货时间', '经办人', '状态', '存放位置', '备注']
    new_form = {}
    for column in columns:
        if form[column] == '' or form[column] == 'None':
            new_form[column] = None
        else:
            new_form[column] = form[column]
    return new_form


@app.route('/equipnum', methods=['GET'])
def equipnum():
    cursor = db.cursor()
    cursor.execute("select * from `数量统计`")
    records = cursor.fetchall()
    return render_template("equipnum.html",
                           title='数量统计',
                           records=records,
                           filter={})

import os
import shutil
import xlrd
import xlwt
import re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_file
)
from werkzeug.exceptions import abort

import manager
from manager.auth import login_required
from manager.db import get_db

bp = Blueprint('info', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    db = get_db()
    cursor = db.cursor()
    if request.method == 'POST':
        form_dict = request.form.to_dict()
        valid_key = []
        for key in form_dict:
            if form_dict[key] != "":
                valid_key.append(key)
        select_condition = []
        for key in valid_key:
            if key == "type" and form_dict[key] != "":
                select_condition.append("`type`=\'" + form_dict[key] + "\'")
            elif key == "name" and form_dict[key] != "":
                select_condition.append("`name` LIKE \'%" + form_dict[key] + "%\'")
            elif key == "model" and form_dict[key] != "":
                select_condition.append("`model` LIKE \'%" + form_dict[key] + "%\'")
            elif key == "serial_number" and form_dict[key] != "":
                select_condition.append("`serial_number` LIKE \'%" + form_dict[key] + "%\'")
            elif key == "contract_number" and form_dict[key] != "":
                select_condition.append("`contract_number` LIKE \'%" + form_dict[key] + "%\'")
            elif key == "arrival_date_start" and form_dict[key] != "":
                select_condition.append("DATE(`arrival_date`) >= DATE('" + form_dict[key] + "')")
            elif key == "arrival_date_end" and form_dict[key] != "":
                select_condition.append("DATE(`arrival_date`) <= DATE('" + form_dict[key] + "')")
            elif key == "transactor" and form_dict[key] != "":
                select_condition.append("`transactor` LIKE \'%" + form_dict[key] + "%\'")
            elif key == "status" and form_dict[key] != "":
                select_condition.append("`status`=\'" + form_dict[key] + "\'")
            elif key == "location" and form_dict[key] != "":
                select_condition.append("`location` LIKE \'%" + form_dict[key] + "%\'")
        if len(select_condition) != 0:
            query = "SELECT `id`, `type`, `name`, `model`, `serial_number`, `contract_number`, `arrival_date`, `transactor`, `status`, `location` FROM `information` WHERE " + " AND ".join(select_condition) + " ORDER BY `id` ASC"
            cursor.execute(query)
            cursor.close()
            records = cursor.fetchall()
            for record in records:
                if record['arrival_date'] is None:
                    record['arrival_date'] = ''
            return render_template('info/index.html', records=records)

    cursor.execute(
        "SELECT `id`, `type`, `name`, `model`, `serial_number`, `contract_number`, `arrival_date`, `transactor`, `status`, `location` FROM `information` ORDER BY `id` ASC"
    )
    cursor.close()
    records = cursor.fetchall()
    for record in records:
        if record['arrival_date'] is None:
            record['arrival_date'] = ''
    return render_template('info/index.html', records=records)

@bp.route('/multi_delete', methods=('POST',))
def multi_delete():
    form_dict = request.form.to_dict()
    all_values = form_dict.values()
    all_id = [value for value in all_values if re.match("^[0-9]", value)]
    db = get_db()
    cursor = db.cursor()
    for id in all_id:
        cursor.execute(
            "DELETE FROM `information` WHERE `id`=%s", [int(id)]
        )
        app = manager.create_app()
        delete_dir = os.path.join(app.config['UPLOAD_FOLDER'], str(id))
        if os.path.exists(delete_dir):
            shutil.rmtree(delete_dir)
    cursor.close()
    db.commit()
    return redirect(url_for('index'))

def set_style(bold=False, format_str=''):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.bold = bold
    style.font = font
    style.num_format_str = format_str
    return style

@bp.route('/export', methods=('POST',))
def export():
    form_dict = request.form.to_dict()
    all_values = form_dict.values()
    all_id = [value for value in all_values if re.match("^[0-9]", value)]
    all_cols = [value for value in all_values if re.match("^[a-z]", value)]
    all_cols.append("comment")
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('Sheet 1')
    col_name_dict = {
        "type": "类型",
        "name": "名称",
        "model": "型号",
        "serial_number": "序列号",
        "contract_number": "合同号",
        "arrival_date": "到货日期",
        "transactor": "经办人",
        "status": "状态",
        "location": "位置",
        "contract_files": "合同文件",
        "photo": "照片",
        "location_photo": "位置照片",
        "manual": "说明书",
        "comment": "备注"
    }
    for i in range(len(all_cols)):
        sheet.write(0, i, col_name_dict[all_cols[i]], set_style(True, '@'))
    db = get_db()
    cursor = db.cursor()
    new_cols = ['`' + col + '`' for col in all_cols]
    query = "SELECT " + ", ".join(new_cols) + " FROM `information` WHERE `id`=%s"
    for i in range(len(all_id)):
        cursor.execute(query, [int(all_id[i])])
        record = cursor.fetchone()
        if "arrival_date" in record:
            record['arrival_date'] = str(record['arrival_date'])
        record_list = [record[key] for key in all_cols]
        for j in range(len(record_list)):
            sheet.write(i + 1, j, record_list[j], set_style(False, '@'))
    app = manager.create_app()
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], "temp.xls")
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
    workbook.save(save_path)
    return send_file(save_path)

def get_record(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * from `information` WHERE `id`=%s",
        [int(id)]
    )
    record = cursor.fetchone()
    cursor.close()
    return record


@bp.route('/<int:id>/details', methods=('GET', 'POST'))
@login_required
def details(id):
    if request.method == 'POST':
        record = get_record(id)
        if record['contract_files'] is not None and record['contract_files'] != '':
            old_filename_list = record['contract_files'].split(';')
        else:
            old_filename_list = []
        if record['photo'] is not None and record['photo'] != '':
            old_photoname_list = record['photo'].split(';')
        else:
            old_photoname_list = []
        if record['location_photo'] is not None and record['location_photo'] != '':
            old_loc_photoname_list = record['location_photo'].split(';')
        else:
            old_loc_photoname_list = []
        if record['manual'] is not None and record['manual'] != '':
            old_manualname_list = record['manual'].split(';')
        else:
            old_manualname_list = []
        form_dict = request.form.to_dict()
        file_dict = request.files.to_dict()

        app = manager.create_app()
        contract_filename_list = []
        contract_file_list = []
        index = 0
        while 'contract_filename_' + str(index) in form_dict:
            contract_filename_list.append(form_dict['contract_filename_' + str(index)])
            if 'contract_file_' + str(index) in file_dict:
                contract_file_list.append(file_dict['contract_file_' + str(index)].filename)
            index += 1
        
        photoname_list = []
        photo_list = []
        index = 0
        while 'photoname_' + str(index) in form_dict:
            photoname_list.append(form_dict['photoname_' + str(index)])
            if 'photo_' + str(index) in file_dict:
                photo_list.append(file_dict['photo_' + str(index)].filename)
            index += 1
        
        loc_photoname_list = []
        loc_photo_list = []
        index = 0
        while 'location_photoname_' + str(index) in form_dict:
            loc_photoname_list.append(form_dict['location_photoname_' + str(index)])
            if 'location_photo_' + str(index) in file_dict:
                loc_photo_list.append(file_dict['location_photo_' + str(index)].filename)
            index += 1
        
        manualname_list = []
        manual_list = []
        index = 0
        while 'manualname_' + str(index) in form_dict:
            manualname_list.append(form_dict['manualname_' + str(index)])
            if 'manual_' + str(index) in file_dict:
                manual_list.append(file_dict['manual_' + str(index)].filename)
            index += 1
        
        new_record = form_dict
        if new_record['arrival_date'] == '':
            new_record['arrival_date'] = None
        new_record['contract_files'] = ';'.join(contract_filename_list)
        new_record['photo'] = ';'.join(photoname_list)
        new_record['location_photo'] = ';'.join(loc_photoname_list)
        new_record['manual'] = ';'.join(manualname_list)
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE `information` SET `type`=%s, `name`=%s, `model`=%s, `serial_number`=%s, `contract_number`=%s, `arrival_date`=%s, `transactor`=%s, `status`=%s, `location`=%s, `contract_files`=%s, `photo`=%s, `location_photo`=%s, `manual`=%s, `comment`=%s WHERE `id`=%s",
            [new_record['type'], new_record['name'], new_record['model'], new_record['serial_number'], new_record['contract_number'], new_record['arrival_date'], new_record['transactor'], new_record['status'], new_record['location'], new_record['contract_files'], new_record['photo'], new_record['location_photo'], new_record['manual'], new_record['comment'], int(id)]
        )
        upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], str(id))
        for filename in old_filename_list:
            if (filename not in contract_filename_list) or (filename in contract_file_list):
                delete_path = os.path.join(upload_dir, filename)
                if os.path.exists(delete_path):
                    os.remove(delete_path)
        index = 0
        while 'contract_file_' + str(index) in file_dict:
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            f = file_dict['contract_file_' + str(index)]
            upload_path = os.path.join(upload_dir, f.filename)
            f.save(upload_path)
            index += 1
        
        for photoname in old_photoname_list:
            if (photoname not in photoname_list) or (photoname in photo_list):
                delete_path = os.path.join(upload_dir, photoname)
                if os.path.exists(delete_path):
                    os.remove(delete_path)
        index = 0
        while 'photo_' + str(index) in file_dict:
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            f = file_dict['photo_' + str(index)]
            upload_path = os.path.join(upload_dir, f.filename)
            f.save(upload_path)
            index += 1
        
        for photoname in old_loc_photoname_list:
            if (photoname not in loc_photoname_list) or (photoname in loc_photo_list):
                delete_path = os.path.join(upload_dir, photoname)
                if os.path.exists(delete_path):
                    os.remove(delete_path)
        index = 0
        while 'location_photo_' + str(index) in file_dict:
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            f = file_dict['location_photo_' + str(index)]
            upload_path = os.path.join(upload_dir, f.filename)
            f.save(upload_path)
            index += 1
        
        for manualname in old_manualname_list:
            if (manualname not in manualname_list) or (manualname in manual_list):
                delete_path = os.path.join(upload_dir, manualname)
                if os.path.exists(delete_path):
                    os.remove(delete_path)
        index = 0
        while 'manual_' + str(index) in file_dict:
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            f = file_dict['manual_' + str(index)]
            upload_path = os.path.join(upload_dir, f.filename)
            f.save(upload_path)
            index += 1
        
        cursor.close()
        db.commit()
    record = get_record(id)
    if record['arrival_date'] is None:
        record['arrival_date'] = ''
    if record['contract_files'] is not None and record['contract_files'] != '':
        record['contract_files'] = record['contract_files'].split(';')
    else:
        record['contract_files'] = None
    if record['photo'] is not None and record['photo'] != '':
        record['photo'] = record['photo'].split(';')
    else:
        record['photo'] = None
    if record['location_photo'] is not None and record['location_photo'] != '':
        record['location_photo'] = record['location_photo'].split(';')
    else:
        record['location_photo'] = None
    if record['manual'] is not None and record['manual'] != '':
        record['manual'] = record['manual'].split(';')
    else:
        record['manual'] = None
    return render_template('info/details.html', record=record)

@bp.route('/get_resource/<int:id>/<filename>', methods=('GET', 'POST'))
@login_required
def get_resource(id, filename):
    app = manager.create_app()
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], str(id), filename)
    return send_file(file_path)

@bp.route('/<int:id>/delete')
@login_required
def delete(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM `information` WHERE `id`=%s", [int(id)]
    )
    cursor.close()
    db.commit()
    app = manager.create_app()
    delete_dir = os.path.join(app.config['UPLOAD_FOLDER'], str(id))
    if os.path.exists(delete_dir):
        shutil.rmtree(delete_dir)
    return redirect(url_for('index'))

@bp.route('/import_item', methods=('GET',))
@login_required
def import_item():
    return render_template('info/import_item.html')

@bp.route('/import_excel', methods=('POST',))
@login_required
def import_excel():
    xlsfile = request.files['file']
    if xlsfile.filename != '':
        db = get_db()
        cursor = db.cursor()
        f = xlsfile.read()
        data = xlrd.open_workbook(file_contents=f)
        table = data.sheets()[0]
        nrows = table.nrows
        query = "INSERT INTO `information` (`type`, `name`, `model`, `serial_number`, `contract_number`, `arrival_date`, `transactor`, `status`, `location`, `comment`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        for i in range(1, nrows):
            value = table.row_values(i)
            if value[5] == '':
                value[5] = None
            cursor.execute(query, value)
        db.commit()
        cursor.close()
    return redirect(url_for('index'))

@bp.route('/import_one', methods=('POST',))
@login_required
def import_one():
    form_dict = request.form.to_dict()
    file_dict = request.files.to_dict()
    
    app = manager.create_app()
    contract_filename_list = []
    index = 0
    while 'contract_filename_' + str(index) in form_dict:
        contract_filename_list.append(form_dict['contract_filename_' + str(index)])
        index += 1
    
    photoname_list = []
    index = 0
    while 'photoname_' + str(index) in form_dict:
        photoname_list.append(form_dict['photoname_' + str(index)])
        index += 1
    
    loc_photoname_list = []
    index = 0
    while 'location_photoname_' + str(index) in form_dict:
        loc_photoname_list.append(form_dict['location_photoname_' + str(index)])
        index += 1
    
    manualname_list = []
    index = 0
    while 'manualname_' + str(index) in form_dict:
        manualname_list.append(form_dict['manualname_' + str(index)])
        index += 1
    
    new_record = form_dict
    if new_record['arrival_date'] == '':
        new_record['arrival_date'] = None
    new_record['contract_files'] = ';'.join(contract_filename_list)
    new_record['photo'] = ';'.join(photoname_list)
    new_record['location_photo'] = ';'.join(loc_photoname_list)
    new_record['manual'] = ';'.join(manualname_list)
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO `information` (`type`, `name`, `model`, `serial_number`, `contract_number`, `arrival_date`, `transactor`, `status`, `location`, `contract_files`, `photo`, `location_photo`, `manual`, `comment`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        [new_record['type'], new_record['name'], new_record['model'], new_record['serial_number'], new_record['contract_number'], new_record['arrival_date'], new_record['transactor'], new_record['status'], new_record['location'], new_record['contract_files'], new_record['photo'], new_record['location_photo'], new_record['manual'], new_record['comment']]
    )
    cursor.execute(
        "SELECT `id` FROM `information` WHERE `name`=%s AND `model`=%s AND `serial_number`=%s",
        [new_record['name'], new_record['model'], new_record['serial_number']]
    )
    id = cursor.fetchone()['id']
    upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], str(id))
    index = 0
    while 'contract_file_' + str(index) in file_dict:
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        f = file_dict['contract_file_' + str(index)]
        upload_path = os.path.join(upload_dir, f.filename)
        f.save(upload_path)
        index += 1

    index = 0
    while 'photo_' + str(index) in file_dict:
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        f = file_dict['photo_' + str(index)]
        upload_path = os.path.join(upload_dir, f.filename)
        f.save(upload_path)
        index += 1

    index = 0
    while 'location_photo_' + str(index) in file_dict:
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        f = file_dict['location_photo_' + str(index)]
        upload_path = os.path.join(upload_dir, f.filename)
        f.save(upload_path)
        index += 1
    
    index = 0
    while 'manual_' + str(index) in file_dict:
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        f = file_dict['manual_' + str(index)]
        upload_path = os.path.join(upload_dir, f.filename)
        f.save(upload_path)
        index += 1

    cursor.close()
    db.commit()
    return redirect(url_for('index'))
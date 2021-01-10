from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_file
)
from werkzeug.exceptions import abort

import manager
from manager.auth import login_required
from manager.db import get_db

bp = Blueprint('count', __name__)


@bp.route('/amount')
def amount():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT `type`, `name`, `model`, `amount` FROM `amount_count` ORDER BY `amount` DESC"
    )
    cursor.close()
    records = cursor.fetchall()
    return render_template('count/amount.html', records=records)
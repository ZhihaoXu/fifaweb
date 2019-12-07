from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from fifa.db import get_db

bp = Blueprint('team_detail', __name__)

@bp.route('/<int:id>/team_detail')
def index(id):
    # Here we need to implement an algorithm to select the team to display
    g.current = "team_detail"
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
    "SELECT p.id id, p.photo photo, p.name name, n.flag flag, n.nationality nationality, p.value value, p.wage wage, p.overall overall, p.potential potential"
    " FROM player p, nation n "
    " WHERE p.nation_id = n.nation_id AND club_id = %s", id
)
    players = cursor.fetchall()
    for player in players:
        player["value"] = '%.1f' % (player["value"])
    cursor.execute(
        "SELECT club_name"
        " FROM team"
        " WHERE club_id = %s", id
    )
    club_name = cursor.fetchone()

    cursor.execute(
    "SELECT *"
    " FROM player0"
    " WHERE club_id = %s", id
)
    attributes = cursor.fetchall()
    return render_template('team_detail.html', players = players, club_name = club_name, attributes = attributes)


    # if (g.user):
    #     g.current = "index"
    #     db = get_db()
    #     cursor = db.cursor()
    #     if g.user['position'] == 'projectmanager':
    #         cursor.execute(
    #             "SELECT *"
    #             " FROM porder"
    #             " WHERE NOT status = 'complete' AND managerid = '%d' "
    #             " ORDER BY orderid" % (g.user['id'])
    #         )
    #     if g.user['position'] == 'photographer':
    #         cursor.execute(
    #             "SELECT *"
    #             " FROM porder"
    #             " WHERE NOT status = 'complete' AND orderid IN (SELECT"
    #             " orderid FROM takephoto WHERE photographerid = '%d')"
    #             " ORDER BY orderid" % (g.user['id'])
    #         )
    #     if g.user['position'] == 'aftereffect':
    #         cursor.execute(
    #             "SELECT *"
    #             " FROM porder"
    #             " WHERE NOT status = 'complete' AND orderid IN (SELECT "
    #             "orderid FROM doeffect WHERE effectid = '%d')"
    #             " ORDER BY orderid" % (g.user['id'])
    #         )
    #     print(g.user['position'])
    #     orders = cursor.fetchall()

    #     cursor.execute(
    #         "SELECT MONTH(startdate) month, SUM(price) sale"
    #         " FROM porder"
    #         " WHERE YEAR(startdate) = YEAR(CURDATE())"
    #         " GROUP BY MONTH(startdate)"
    #     )
    #     sales = cursor.fetchall()

        # cursor.execute(
        #     "SELECT o.managerid o.SUM(price) m.username"
        #     "FROM porder o, projectmanager m"
        #     "WHERE o.managerid = m.id AND"
        # )
    #     return render_template('dashboard/index.html', orders=orders, sales = sales)
    # else:
    #     return redirect(url_for('auth.login'))


# @bp.route('/create', methods=('GET', 'POST'))
# # @login_required
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             cursor = db.cursor()
#             cursor.execute(
#                 "INSERT INTO post (title, body, author_id)"
#                 " VALUES ('%s', '%s', '%d')" % \
#                 (title, body, g.user['id'])
#             )
#             db.commit()
#             return redirect(url_for('dashboard.index'))

#     return render_template('dashboard/create.html')

# def get_post(id, check_author=True):
#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute(
#         "SELECT p.id, title, body, created, author_id, username"
#         " FROM post p JOIN user u ON p.author_id = u.id"
#         " WHERE p.id = '%d'" % \
#         (id,)
#     )
#     post = cursor.fetchone()

#     if post is None:
#         abort(404, "Post id {0} doesn't exist.".format(id))

#     if check_author and post['author_id'] != g.user['id']:
#         abort(403)

#     return post

# @bp.route('/<int:id>/update', methods=('GET', 'POST'))
# # @login_required
# def update(id):
#     post = get_post(id)

#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             cursor = db.cursor()
#             cursor.execute(
#                 "UPDATE post SET title = '%s', body = '%s'"
#                 " WHERE id = '%d'" % \
#                 (title, body, id)
#             )
#             db.commit()
#             return redirect(url_for('dashboard.index'))

#     return render_template('dashboard/update.html', post=post)

# @bp.route('/<int:id>/delete', methods=('POST',))
# # @login_required
# def delete(id):
#     get_post(id)
#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute("DELETE FROM post WHERE id = '%d'" % (id,))
#     db.commit()
#     return redirect(url_for('dashboard.index',orders=None, sales = None))
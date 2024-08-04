# views.py
from flask import Blueprint, request, session, render_template, redirect, url_for, jsonify
from models import curator_info, curatorlike_status, curator_like, curator_unlike, plyy_like, plyy_unlike, plyylike_status, cu_plyy
from utils import extract_user
import database as db

main = Blueprint('main', __name__)
logout = Blueprint('logout', __name__)
mypage = Blueprint('mypage', __name__)
login = Blueprint('login', __name__)
curator = Blueprint('curator', __name__)
api_curator = Blueprint('api_curator', __name__)
like_curator = Blueprint('like_curator', __name__)
unlike_curator = Blueprint('unlike_curator', __name__)
like_plyy = Blueprint('like_plyy', __name__)
unlike_plyy = Blueprint('unlike_plyy', __name__)

@main.route('/main', methods=['GET', 'POST'])
def main_view():
    return render_template('main.html')

@login.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        id = request.form['userid']
        pw = request.form['userpw']
        user = db.get_query('SELECT email, pw FROM USER WHERE email = ? and pw = ?', (id, pw),mul=False)

        if user:
            session['id'] = id
            return redirect(url_for('main.main_view'))
        else:
            session['id'] = None
    return render_template('login.html')

@logout.route('/logout', methods=['POST'])
def logout_view():
    session.pop('id', None)
    return redirect(url_for('main.main_view'))

@mypage.route('/mypage')
def mypage_view():
    return render_template('mypage.html')


@curator.route('/curator/<c_id>')
def curator_view(c_id):
    return render_template('test.html')

@api_curator.route('/plyy/api/curator/<c_id>', methods=['GET'])
def api_curator_view(c_id):
    play_lists = []
    c_info = curator_info(c_id)
    c_plyy = cu_plyy(c_id)
    c_isliked = None

    for plyy in c_plyy:
        plyy_data = {
            'pid': plyy[0],
            'ptitle': plyy[1],
            'pimg': plyy[2],
            'pgen': plyy[3],
            'pupdate': plyy[4],
            'pcmt': plyy[5],
            'ptag': plyy[8],
            'pliked': None
        }
        play_lists.append(plyy_data)

    pidlist = [play_lists[i]['pid'] for i in range(len(play_lists))]

    if 'id' in session and session['id']:
        u_id = extract_user(session['id'])
        if u_id:
            c_isliked = curatorlike_status(c_id, u_id)
            p_isliked = plyylike_status(pidlist, u_id)

            for plyy in play_lists:
                plyy['pliked'] = p_isliked.get(plyy['pid'], False)

    return jsonify({
        'curator': {
            'c_info': {
                'c_id': c_info[0],
                'c_name': c_info[1],
                'c_img': c_info[2],
                'c_intro': c_info[3],
                'c_tags': c_info[4],
                'c_liked': c_isliked
            },
            'plyy': play_lists
        }
    })

@like_curator.route('/plyy/api/like/<u_id>/<c_id>', methods=['POST'])
def like_curator_view(u_id, c_id):
    u_id = extract_user(u_id)
    success = curator_like(c_id, u_id)
    if success:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 500

@unlike_curator.route('/plyy/api/unlike/<u_id>/<c_id>', methods=['DELETE'])
def unlike_curator_view(u_id, c_id):
    u_id = extract_user(u_id)
    success = curator_unlike(c_id, u_id)
    if success:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 500

@like_plyy.route('/plyy/api/plyylike/<u_id>/<p_id>', methods=['POST'])
def like_plyy_view(u_id, p_id):
    u_id = extract_user(u_id)
    success = plyy_like(p_id, u_id)
    if success:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 500

@unlike_plyy.route('/plyy/api/plyyunlike/<u_id>/<p_id>', methods=['DELETE'])
def unlike_plyy_view(u_id, p_id):
    u_id = extract_user(u_id)
    success = plyy_unlike(p_id, u_id)
    if success:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 500

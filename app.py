# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request

from flask import abort
from flask import flash

from flask import session
from models import User
from models import Bloglist
from models import Comment
from chilog import log

app = Flask(__name__)
app.secret_key = 'chi'
cookie_dict = {}


def current_user():
    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).first()
    return user


@app.route('/')
def index():
    return redirect(url_for('login_view'))


@app.route('/login')
def login_view():
    return render_template('login.html')


@app.route('/login', methods=['Post'])
def login():
    u = User(request.form)
    print('u', u)
    print('u.username', u.username)
    user = User.query.filter_by(username=u.username).first()
    x = User.query.filter(User.username != 'admin').all()
    print('x',x)
    print('user', user)
    # print('user.username',user.username)
    log(user)
    # log(user.validate(u))
    if user == None:
        log('用户登录失败')
        flash('此用户不存在')
        #return redirect(url_for
        return '此用户不存在'
    elif user.validate(u):
        log('用户登录成功')
        session['user_id'] = user.id
        r = url_for('bloglist_view', username=user.username)
        print('r',r)
        # cookie_id = str(uuid.uuid4())
        # cookie_dict[cookie_id] = user
        # r.set_cookie('cookie_id', cookie_id)
        return r
    else:
        log('用户登录失败')
        flash('用户密码错误')
        #return redirect(url_for('login_view'))
        return '用户密码错误'


@app.route('/register', methods=['POST'])
def register():
    u = User(request.form)
    # log(u)
    log(u.valid())
    log(u.valid_unique_existence())
    if u.valid() and u.valid_unique_existence():
        flash('注册成功')
        log('用户注册成功')
        u.save()
        #return redirect(url_for('login_view'))
        return '注册成功'
    else:
        flash('失败')
        log('注册失败', request.form)
        #return redirect(url_for('login_view'))
        return '注册失败'


@app.route('/bloglist/<username>')
def bloglist_view(username):
    # sql = str(User.query.filter_by(username=username))
    # log(sql)
    u = User.query.filter_by(username=username).first()
    user_list = User.query.all()
    log(u)
    if u is None:
        abort(404)
    user = current_user()
    log('currentuser', user)
    # log('user.id',user.id)
    log('u.id', u.id)
    log('u.bloglist', u.bloglist)
    bloglist = u.bloglist
    # bloglist.sort(key=lambda t: t.created_time, reverse=True)
    print(username, current_user().username)
    return render_template('bloglist.html', bloglist=bloglist, username=username, user=current_user(),
                           all_users=user_list)


@app.route('/bloglist/<username>/<blog_id>')#title实际上是b.id
def blogdetail(username, blog_id):
    user = current_user()
    print(user)
    b = Bloglist.query.filter_by(id=blog_id).first()
    print(b)
    print('title',blog_id)
    c = Comment.query.filter_by(blog_id=blog_id).all()
    print('c', c)
    # print(c.poster)
    print(b)
    print(b.id)
    return render_template('blogdetail.html', current_user=user, b=b, c=c)


@app.route('/bloglist/comment/<blog_id>', methods=['POST'])
def bloglist_comment(blog_id):
    user = current_user()
    c = Comment(request.form)
    # 设置是谁评论的
    print('c',c.comment_content)
    c.poster = user.username
    c.blog_id = blog_id
    # 保存到数据库
    c.save()
    print('c.save',c.save())
    return redirect(url_for('blogdetail', username=user.username, blog_id=blog_id))


@app.route('/bloglist/add', methods=['POST'])
def bloglist_add():
    user = current_user()
    if user is None:
        return redirect(url_for('login_view'))
    else:
        b = Bloglist(request.form)
        # 设置是谁发的
        b.user = user
        # 保存到数据库
        b.save()
        return redirect(url_for('bloglist_view', username=user.username))


@app.route('/bloglist/delete/<bloglist_id>')
def bloglist_delete(bloglist_id):
    t = Bloglist.query.filter_by(id=bloglist_id).first()
    if t is None:
        abort(404)
    # 获取当前登录的用户, 如果用户没登录或者用户不是这条的主人, 就返回 401 错误
    user = current_user()
    if user is None or user.id != t.user_id:
        abort(401)
    else:
        t.delete()
        return redirect(url_for('bloglist_view', username=user.username))


@app.route('/bloglist/update/<bloglist_id>')
def bloglist_update_view(bloglist_id):
    t = Bloglist.query.filter_by(id=bloglist_id).first()
    if t is None:
        abort(404)
    # 获取当前登录的用户, 如果用户没登录或者用户不是这条微博的主人, 就返回 401 错误
    user = current_user()
    if user is None or user.id != t.user_id:
        abort(401)
    else:
        return render_template('bloglist_edit.html', bloglist=t)


# 处理 更新 微博的请求
@app.route('/bloglist/update/<bloglist_id>', methods=['POST'])
def bloglist_update(bloglist_id):
    t = Bloglist.query.filter_by(id=bloglist_id).first()
    if t is None:
        abort(404)
    # 获取当前登录的用户, 如果用户没登录或者用户不是这条微博的主人, 就返回 401 错误
    user = current_user()
    if user is None or user.id != t.user_id:
        abort(401)
    else:
        t.content = request.form.get('content', '')
        t.save()
        return redirect(url_for('bloglist_view', username=user.username))







if __name__ == '__main__':
    app.run(debug=True, port=8000)

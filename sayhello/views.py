# -*- coding: utf-8 -*-
"""

"""
from flask import flash, redirect, url_for, render_template, request

from sayhello import app, db
from sayhello.forms import HelloForm
from sayhello.models import Message


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    # TODO 分页BUG未解决
    """
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        message = Message(body=body, name=name)
        db.session.add(message)
        db.session.commit()
        flash('添加成功')
        return redirect(url_for('index'))
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    total_page = divmod(len(messages),10)[0]+1 if divmod(len(messages),10)[1] else divmod(len(messages),10)[0]
    page_num = request.args.get('page_num') and int(request.args.get('page_num'))
    li_list = []
    if not page_num:
        start_page = 1
        end_page = 5
        page_num = 0
    else:
        start_page = int(request.args.get('start_page'))
        end_page = int(request.args.get('end_page'))
        mid_page = (int(start_page) + int(end_page)) // 2
        offset_page = page_num - mid_page
        if offset_page > 0:
            start_page += offset_page
            end_page += offset_page
            if end_page > total_page:
                end_page = total_page
    for i in range(start_page, end_page+1):
        standard_li = '<li><a href="/?page_num={0}&start_page={1}&end_page={2}">{0}</a></li>'.format(i,start_page,end_page)
        li_list.append(standard_li)
    page_block = "".join(li_list)
    messages = Message.query.order_by(Message.timestamp.desc()).offset(page_num).limit(100000).all()
    return render_template('index.html', form=form, messages=messages,page_block=page_block)

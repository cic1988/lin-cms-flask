from flask import jsonify, request
from sqlalchemy import desc, func
import math

from lin import db, route_meta, group_required, login_required
from lin.exception import Success
from lin.redprint import Redprint
from lin.jwt import admin_required
from lin.db import get_total_nums

from app.models.video import Video, Category
from app.validators.video_validator import NewCategory, CategorySearchForm, VideoSearchForm, CreateOrUpdateVideoForm
from app.libs.utils import get_page_from_query, json_res, paginate

video_api = Redprint('video')

# ------------------------------------------------
# Category
# ------------------------------------------------


@video_api.route('/category/<id>', methods=['GET'])
@login_required
def get_category(id):
    category = Category.get_detail(id)
    return jsonify(category)


@video_api.route('/category', methods=['GET'])
@login_required
def get_categories():
    categories = Category.get_all()
    return jsonify(categories)


@video_api.route('/category', methods=['POST'])
@admin_required
def create_category():
    form = NewCategory().validate_for_api()
    Category.new_category(form)
    return Success(msg='create category successfully')


@video_api.route('/category/search', methods=['GET'])
def search_category():
    form = CategorySearchForm().validate_for_api()
    categories = Category.search_by_keywords(form.q.data)
    return jsonify(categories)

# ------------------------------------------------
# Video
# ------------------------------------------------


@video_api.route('/<id>', methods=['GET'])
@login_required
def get_video(id):
    video = Video.get_detail(id)
    return jsonify(video)


@video_api.route('', methods=['GET'])
@login_required
def get_videos():

    videos = []

    start, count = paginate()
    category_id = request.args.get('c')

    condition = {}

    if category_id:
        condition['category'] = category_id

    videos = db.session.query(Video).filter_by(
        soft=True, **condition).order_by(desc(Video.id)).offset(start).limit(count).all()

    total = get_total_nums(Video, is_soft=True, **condition)
    total_page = math.ceil(total / count)
    page = get_page_from_query()
    return json_res(count=count, items=videos, page=page, total=total, total_page=total_page)


@video_api.route('/search', methods=['GET'])
def search():
    form = VideoSearchForm().validate()
    # search with pagination
    start, count = paginate()
    like = Video.title.like('%' + form.q.data + '%')

    # TODO: why not work?
    #videos = db.session.query(Video).filter_by(
    #    **condition).order_by(desc(Video.id)).offset(start).limit(count).all()
    videos = db.session.query(Video).filter(like).offset(start).limit(count).all()

    total = db.session.query(func.count(Video.id))
    total = total.filter(Video.delete_time == None).filter(like).scalar()

    if not total:
        total = 0

    total_page = math.ceil(total / count)
    page = get_page_from_query()

    return json_res(count=count, items=videos, page=page, total=total, total_page=total_page)


@video_api.route('', methods=['POST'])
def create_video():
    form = CreateOrUpdateVideoForm().validate_for_api()
    Video.new_video(form)
    return Success(msg='create video successfully')


@video_api.route('/<bid>', methods=['PUT'])
def update_video(bid):
    form = CreateOrUpdateVideoForm().validate_for_api()
    Video.edit_video(bid, form)
    return Success(msg='update video successfully')


@video_api.route('/<bid>', methods=['DELETE'])
@route_meta(auth='delete video', module='video')
@group_required
def delete_video(bid):
    Video.remove_video(bid)
    return Success(msg='delete video successfully')

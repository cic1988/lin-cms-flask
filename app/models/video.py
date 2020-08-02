from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer
from sqlalchemy_utils import URLType

from app.libs.error_code import VideoNotFound, CategoryNotFound


#------------------------------------------------
# Category
#------------------------------------------------

class Category(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    description = Column(String(100))

    @classmethod
    def get_detail(cls, bid):
        category = cls.query.filter_by(id=bid, delete_time=None).first()
        if category is None:
            raise CategoryNotFound()
        return category

    @classmethod
    def get_all(cls):
        categories = cls.query.filter_by(delete_time=None).all()
        if not categories:
            raise CategoryNotFound()
        return categories

    @classmethod
    def search_by_keywords(cls, q):
        categories = []

        if q:
            categories = cls.query.filter(Category.name.like(
                '%' + q + '%'), Category.delete_time == None).all()

        if not categories:
            raise CategoryNotFound()
        return categories

    @classmethod
    def new_category(cls, form):
        category = Category.query.filter_by(
            name=form.name.data, delete_time=None).first()
        if category is not None:
            raise ParameterException(msg='category already exists')

        Category.create(
            name=form.name.data,
            description=form.description.data,
            commit=True
        )
        return True

    @classmethod
    def edit_category(cls, bid, form):
        category = Category.query.filter_by(id=bid, delete_time=None).first()
        if category is None:
            raise CategoryNotFound()

        category.update(
            id=bid,
            name=form.name.data,
            description=form.description.data,
            commit=True
        )
        return True

    @classmethod
    def remove_category(cls, bid):
        category = cls.query.filter_by(id=bid, delete_time=None).first()
        if category is None:
            raise CategoryNotFound()
        category.delete(commit=True)
        return True


#------------------------------------------------
# Video
#------------------------------------------------

class Video(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    description = Column(String(50), nullable=False)
    thumbnail = Column(URLType)
    url = Column(URLType)
    embedded = Column(String(500))
    category = Column(String(20), default='others')
    tags = Column(String(100))

    @classmethod
    def validateCategory(cls, id):
        category = Category.query.filter_by(id=id, delete_time=None).first()
        if category is None:
            raise CategoryNotFound()

    @classmethod
    def get_detail(cls, bid):
        video = cls.query.filter_by(id=bid, delete_time=None).first()
        if video is None:
            raise VideoNotFound()
        return video

    @classmethod
    def get_all(cls, category_id):
        videos = []

        if not category_id:
            videos = cls.query.filter_by(delete_time=None).all()
        else:
            videos = cls.query.filter_by(delete_time=None, category=category_id).all()

        if not videos:
            raise VideoNotFound()
        return videos

    @classmethod
    def search_by_keywords(cls, q, c):
        videos = []

        if q:
            videos = cls.query.filter(Video.title.like('%' + q + '%'), Video.delete_time == None).all()
        
        if c:
            videos = cls.query.filter(Video.category == c, Video.delete_time == None).all()

        if not videos:
            raise VideoNotFound()
        return videos

    @classmethod
    def new_video(cls, form):
        # use url as video identifier
        video = Video.query.filter_by(url=form.url.data, delete_time=None).first()
        if video is not None:
            raise ParameterException(msg='video already exists')

        cls.validateCategory(form.category.data)

        Video.create(
            title=form.title.data,
            description=form.description.data,
            thumbnail=form.thumbnail.data,
            url=form.url.data,
            embedded=form.embedded.data,
            category=form.category.data,
            tags=form.tags.data,
            commit=True
        )
        return True

    @classmethod
    def edit_video(cls, bid, form):
        video = Video.query.filter_by(id=bid, delete_time=None).first()
        if video is None:
            raise VideoNotFound()

        cls.validateCategory(form.category.data)

        video.update(
            id=bid,
            title=form.title.data,
            description=form.description.data,
            thumbnail=form.thumbnail.data,
            url=form.url.data,
            embedded=form.embedded.data,
            category=form.category.data,
            tags=form.tags.data,
            commit=True
        )
        return True

    @classmethod
    def remove_video(cls, bid):
        video = cls.query.filter_by(id=bid, delete_time=None).first()
        if video is None:
            raise VideoNotFound()
        # 删除图书，软删除
        video.delete(commit=True)
        return True

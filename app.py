from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import _basedir
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqlamodel import ModelView
from flask_babel import Babel
from flask_admin.contrib.fileadmin import FileAdmin
from flask_cors import CORS
from flask_basicauth import BasicAuth


app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
babel = Babel(app)
basic_auth = BasicAuth(app)
cors = CORS(app, resources={r"/admin": {"origins": "*"}})


if __name__ == '__main__':
    from apps.admin import views

    admin = Admin(app, name='Товарка', template_mode='bootstrap3', index_view=views.MyAdminIndexView())
    admin.add_view(FileAdmin(_basedir, '/static/', name='Static Files'))

    admin.add_view(views.BrandAdmin(views.models.Brand, db.session, 'Бренды'))
    admin.add_view(views.SizeAdmin(views.models.Size, db.session, 'Размеры'))
    admin.add_view(views.ColorAdmin(views.models.Color, db.session, 'Цвета'))
    admin.add_view(ModelView(views.models.Category, db.session, 'Категории'))
    admin.add_view(views.ProductAdmin(views.models.Product, db.session, 'Товары'))
    admin.add_view(views.ProductImageAdmin(views.models.ProductImage, db.session, 'Фотки'))

    app.run(debug=True, host='0.0.0.0')

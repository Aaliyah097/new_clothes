from flask import url_for
from sqlalchemy import event
from app import db, app
import os
from flask import Markup


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(50), nullable=False)

    products = db.relationship('Product',
                               backref=db.backref('brand'))

    # for logo
    path = db.Column(db.Unicode(128))
    type = db.Column(db.Unicode(4))
    name = db.Column(db.Unicode(50))

    def __init__(self, title: str) -> None:
        self.title = title

    def __repr__(self) -> str:
        return self.title

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'logo': url_for('static', filename=os.path.join('', self.path))
        }


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(50), nullable=False, unique=True)

    products = db.relationship('Product',
                               backref=db.backref('category'))

    def __init__(self, title: str) -> None:
        self.title = title

    def __repr__(self) -> str:
        return self.title


products_images = db.Table('products_images',
                           db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
                           db.Column('product_image_id', db.Integer, db.ForeignKey('product_image.id'))
                           )


class Size(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    literal = db.Column(db.String(3), nullable=False, unique=True)
    numeric = db.Column(db.Integer(), nullable=False)

    products = db.relationship('Product',
                               backref=db.backref('size'))

    def __repr__(self):
        return f"{self.literal} ({self.numeric})"


class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(20), nullable=False, unique=True)

    products = db.relationship('Product',
                               backref=db.backref('color'))

    def __repr__(self):
        return self.name


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    is_parent = db.Column(db.Boolean, default=False)

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))

    # артикул
    sku = db.Column(db.String(50), unique=True, nullable=False, index=True)

    # Отметка на карточке (Например, SALE, NEW, -30%)
    mark = db.Column(db.String(20), nullable=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    title = db.Column(db.String(150), nullable=False)

    description = db.Column(db.String(150), nullable=True)

    text = db.Column(db.Text, nullable=True)

    price = db.Column(db.Integer, nullable=False)

    quantity = db.Column(db.Integer, nullable=False, default=0)

    price_old = db.Column(db.Integer, nullable=True)

    parent_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True, default=None)

    children = db.relationship("Product", post_update=True, uselist=True)

    images = db.relationship("ProductImage",
                             secondary=products_images, backref='images',
                             order_by="ProductImage.name")

    color_id = db.Column(db.Integer, db.ForeignKey('color.id'))
    size_id = db.Column(db.Integer, db.ForeignKey('size.id'))

    def create_sku(self):
        sku = (self.brand.__repr__().upper()[0:3] if self.brand else '?') + '-' + \
              (self.color.name.upper()[0:3] if self.color else '?') + '-' + \
              (self.category.__repr__().upper()[0:3] if self.category else '?') + '-' + \
               str(self.size.numeric if self.size else '00')

        sku += '1' if self.is_parent else '0'
        sku += '-'
        sku += self._get_last_sku_id()

        return sku

    @property
    def children_amount(self) -> str:
        return Markup('<br>'.join([f'<a href="/admin/product/details/?id={ch.id}">{ch.sku}</a>' for ch in self.children]))

    def _get_last_id(self) -> int:
        try:
            return self.id if self.id else Product.query.order_by(Product.id.desc()).limit(1).first().id + 1
        except (KeyError, AttributeError, IndexError, TypeError):
            return 0

    def _get_last_sku_id(self) -> str:
        last_id = str(self._get_last_id())
        sku_id = '0' * (4 - len(last_id))
        sku_id += last_id

        return sku_id

    def create_name(self) -> str:
        return f"{self.color.name} {self.category.title[:-1]} {self.brand.title}"

    def __repr__(self):
        return f"{self.title} ({self.sku})"

    @property
    def primary_image(self):
        data = self.images[0] if len(self.images) != 0 else ""

        if not data:
            return ''

        url = url_for('static', filename=os.path.join('', data.path))

        return Markup('<img src="%s" width="100">' % url)


@event.listens_for(Product, "before_insert")
@event.listens_for(Product, "before_update")
def create_sku(mapper, connection, target):
    target.sku = target.create_sku()
    target.title = target.create_name()


class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # for logo
    path = db.Column(db.Unicode(128))
    type = db.Column(db.Unicode(3))
    name = db.Column(db.Unicode(50), unique=True)

    def __repr__(self):
        return f"{self.name}"

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'product_id': self.product_id,
            'logo': url_for('static', filename=os.path.join('', self.path))
        }

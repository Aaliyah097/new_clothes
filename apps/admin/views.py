import csv
from io import StringIO
import os

from apps.products import models
from app import basic_auth, app
from flask_admin.contrib import sqla
from flask_admin import form, expose, AdminIndexView
from flask import Markup, make_response, redirect, url_for


from werkzeug.exceptions import HTTPException
from werkzeug import Response


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}))


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        print(1)
        return redirect(basic_auth.challenge())


class ImageView(sqla.ModelView):
    form_extra_fields = {
        'file': form.FileUploadField('file', base_path=app.config['UPLOAD_FOLDER'])
    }

    def _change_path_data(view, _form):
        try:
            logo = _form.file.data

            if logo:
                ext = logo.filename.split('.')[-1]
                print(logo.filename.split('.')[0])
                path = '%s.%s' % (logo.filename.split('.')[0], ext)

                logo.save(
                    os.path.join(app.config['UPLOAD_FOLDER'], path)
                )

                _form.name.data = _form.name.data or logo.filename.split('.')[0]
                _form.path.data = path
                _form.type.data = ext

                del _form.file
        except Exception as e:
            print(str(e))

        return _form

    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        url = url_for('static', filename=os.path.join('', model.path))

        if model.type in app.config['ALLOWED_EXTENSIONS']:
            return Markup('<img src="%s" width="100">' % url)

    column_formatters = {
        'path': _list_thumbnail
    }

    def edit_form(self, obj=None):
        return self._change_path_data(
            super().edit_form(obj)
        )

    def create_form(self, obj=None):
        return self._change_path_data(
            super().create_form(obj)
        )


class BrandAdmin(ImageView):
    column_filters = ('title', 'name', 'type',)

    column_labels = {
        'title': 'Наименование',
        'name': 'Название файла',
        'type': 'Расширение'
    }

    column_display_pk = True

    column_default_sort = 'title'


class ProductImageAdmin(ImageView):
    column_filters = (models.Product.sku, 'type', 'name')

    column_display_pk = True

    column_default_sort = 'name'


class SizeAdmin(sqla.ModelView):
    column_display_pk = True
    column_labels = {
        'literal': 'Символ',
        'numeric': 'Число'
    }


class ColorAdmin(sqla.ModelView):
    column_display_pk = True
    column_labels = {
        'name': 'Название'
    }


class ProductAdmin(sqla.ModelView):
    column_filters = ('id', models.Brand.title, 'is_parent', 'sku', 'mark',
                      models.Category.title, 'title', 'description',
                      'text', 'price', 'quantity', 'price_old',
                      'parent_id', models.Size.literal, models.Color.name)

    list_template = 'admin/list.html'

    column_list = ('id', 'computed', 'is_parent', 'children_amount', 'sku', 'mark',
                   'title', 'price', 'quantity', 'brand', 'category',
                   'size', 'color')

    export_columns = None

    def _get_data_for_export(view):
        return models.Product.query.order_by('parent_id', 'sku')

    def row_attributes(view, obj):
        if obj.is_parent:
            return {'class': 'success'}

    column_searchable_list = ('sku', 'title', 'id')

    column_default_sort = 'parent_id'

    can_export = True

    def get_export_csv(self):
        self.export_columns = ['SKU', 'Title', 'Category', 'Description', 'Text',
                               'Photo', 'Price', 'Quantity', 'Price Old',
                               'Editions', 'Modifications', 'TildaUID',
                               'Parent UID', 'External ID']

        io = StringIO()
        rows = csv.DictWriter(io, self.export_columns, lineterminator="\n")

        data = self._get_data_for_export()

        rows.writeheader()

        for item in data:
            row = {
                'SKU': item.sku if not item.is_parent else "",
                'Category': item.category.title,
                'Title': item.title if item.is_parent else item.title + " / " + item.size.literal,
                'Description': item.description,
                'Text': item.text,
                'Photo': ' '.join(
                    ["https://arcane-switch.com:5000/static/" + im.path for im in item.images]
                ) if len(item.images) != 0 else "",
                'Price': item.price if not item.is_parent else "",
                'Quantity': item.quantity if not item.is_parent else "",
                'Price Old': item.price_old,
                'Editions': f"Размер:{item.size.literal}" if not item.is_parent else "",
                'Modifications': '',
                'TildaUID': item.id,
                'Parent UID': item.parent_id if not item.is_parent else "",
                'External ID': item.id
            }
            rows.writerow(row)

        io.seek(0)
        return io.getvalue()

    @expose('/export/')
    def export(self):
        response = make_response(self.get_export_csv())
        response.mimetype = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=%s.csv' % 'products'

        return response

    can_view_details = True

    def _computed_formatter(view, context, model, name):
        return model.primary_image

    def _computed_children(view, context, model, name):
        return model.children_amount

    column_formatters = {
        'computed': _computed_formatter,
        'children_amount': _computed_children,
    }

    column_labels = {
        'id': 'ID',
        'children': 'Дети',
        'color': 'Цвет',
        'size': 'Размер',
        'is_parent': 'Признак родителя',
        'sku': 'Артикул',
        'mark': 'Метка',
        'title': 'Наименование',
        'description': 'Кр. опис.',
        'text': 'Описание',
        'price': 'Цена',
        'quantity': 'Кол-во',
        'price_old': 'Старая цена',
        'brand': 'Бренд',
        'category': 'Категория',
        'computed': 'Фото',
        'children_amount': 'Моделей'
    }

    column_display_pk = True

    form_excluded_columns: list[str] = ['sku', 'title', ]

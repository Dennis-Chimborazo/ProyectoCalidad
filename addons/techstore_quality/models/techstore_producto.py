from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class TechstoreProducto(models.Model):
    _name = 'techstore.producto'
    _description = 'Producto TechStore'
    _order = 'name'

    name = fields.Char(
        string='Producto',
        required=True
    )

    codigo = fields.Char(
        string='Código',
        required=True
    )

    precio_unitario = fields.Float(
        string='Precio unitario',
        required=True
    )

    stock_disponible = fields.Integer(
        string='Stock disponible',
        default=10,
        required=True
    )

    activo = fields.Boolean(
        string='Activo',
        default=True
    )

    _sql_constraints = [
        (
            'unique_name_producto',
            'unique(name)',
            'El nombre del producto ya está registrado.'
        ),
        (
            'unique_codigo_producto',
            'unique(codigo)',
            'El código del producto ya está registrado.'
        ),
    ]

    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if not record.name or len(record.name.strip()) < 3:
                raise ValidationError(
                    'El nombre del producto debe tener al menos 3 caracteres.'
                )

            producto_existente = self.search([
                ('id', '!=', record.id),
                ('name', '=ilike', record.name.strip())
            ], limit=1)

            if producto_existente:
                raise ValidationError(
                    'Ya existe un producto con ese nombre.'
                )

    @api.constrains('codigo')
    def _check_codigo(self):
        for record in self:
            if not record.codigo or len(record.codigo.strip()) < 3:
                raise ValidationError(
                    'El código del producto debe tener al menos 3 caracteres.'
                )

            codigo = record.codigo.strip().upper()

            if not re.match(r'^[A-Z0-9\-]+$', codigo):
                raise ValidationError(
                    'El código solo puede contener letras, números y guiones.'
                )

            producto_existente = self.search([
                ('id', '!=', record.id),
                ('codigo', '=ilike', codigo)
            ], limit=1)

            if producto_existente:
                raise ValidationError(
                    'Ya existe un producto con ese código.'
                )

    @api.constrains('precio_unitario')
    def _check_precio_unitario(self):
        for record in self:
            if record.precio_unitario <= 0:
                raise ValidationError(
                    'El precio unitario debe ser mayor a 0.'
                )

    @api.constrains('stock_disponible')
    def _check_stock_disponible(self):
        for record in self:
            if record.stock_disponible < 0:
                raise ValidationError(
                    'El stock disponible no puede ser negativo.'
                )

    @api.model
    def create(self, vals):
        if vals.get('name'):
            vals['name'] = vals.get('name').strip()

        if vals.get('codigo'):
            vals['codigo'] = vals.get('codigo').strip().upper()

        return super().create(vals)

    def write(self, vals):
        if vals.get('name'):
            vals['name'] = vals.get('name').strip()

        if vals.get('codigo'):
            vals['codigo'] = vals.get('codigo').strip().upper()

        return super().write(vals)

    @api.model
    def get_productos_data(self):
        productos = self.search([], order='name asc')

        return [
            {
                'id': producto.id,
                'name': producto.name or '',
                'codigo': producto.codigo or '',
                'precio_unitario': producto.precio_unitario or 0,
                'stock_disponible': producto.stock_disponible or 0,
                'activo': producto.activo,
            }
            for producto in productos
        ]

    @api.model
    def create_producto_custom(self, values):
        producto = self.create({
            'name': values.get('name'),
            'codigo': values.get('codigo'),
            'precio_unitario': float(values.get('precio_unitario') or 0),
            'stock_disponible': int(values.get('stock_disponible') or 0),
            'activo': values.get('activo', True),
        })

        return {
            'id': producto.id,
            'name': producto.name or '',
            'codigo': producto.codigo or '',
            'precio_unitario': producto.precio_unitario or 0,
            'stock_disponible': producto.stock_disponible or 0,
            'activo': producto.activo,
        }

    @api.model
    def update_producto_custom(self, producto_id, values):
        producto = self.browse(producto_id)

        if not producto.exists():
            raise ValidationError('El producto no existe.')

        producto.write({
            'name': values.get('name'),
            'codigo': values.get('codigo'),
            'precio_unitario': float(values.get('precio_unitario') or 0),
            'stock_disponible': int(values.get('stock_disponible') or 0),
            'activo': values.get('activo', True),
        })

        return {
            'id': producto.id,
            'name': producto.name or '',
            'codigo': producto.codigo or '',
            'precio_unitario': producto.precio_unitario or 0,
            'stock_disponible': producto.stock_disponible or 0,
            'activo': producto.activo,
        }

    @api.model
    def toggle_producto_activo_custom(self, producto_id):
        producto = self.browse(producto_id)

        if not producto.exists():
            raise ValidationError('El producto no existe.')

        producto.write({
            'activo': not producto.activo
        })

        return {
            'id': producto.id,
            'activo': producto.activo,
        }
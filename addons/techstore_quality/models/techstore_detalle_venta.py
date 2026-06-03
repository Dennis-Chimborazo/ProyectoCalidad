from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TechstoreDetalleVenta(models.Model):
    _name = 'techstore.detalle.venta'
    _description = 'Detalle de Venta TechStore'
    _order = 'id asc'

    venta_id = fields.Many2one(
        'techstore.venta',
        string='Venta',
        required=True,
        ondelete='cascade'
    )

    producto_id = fields.Many2one(
        'techstore.producto',
        string='Producto',
        required=True
    )

    cantidad = fields.Integer(
        string='Cantidad',
        required=True,
        default=1
    )

    precio_unitario = fields.Float(
        string='Precio unitario',
        required=True
    )

    subtotal = fields.Float(
        string='Subtotal',
        compute='_compute_subtotal',
        store=True
    )

    stock_actual = fields.Integer(
        string='Stock actual',
        related='producto_id.stock_disponible',
        store=False
    )

    codigo_producto = fields.Char(
        string='Código',
        related='producto_id.codigo',
        store=False
    )

    @api.onchange('producto_id')
    def _onchange_producto_id(self):
        for record in self:
            if record.producto_id:
                record.precio_unitario = record.producto_id.precio_unitario

    @api.depends('cantidad', 'precio_unitario')
    def _compute_subtotal(self):
        for record in self:
            cantidad = record.cantidad or 0
            precio = record.precio_unitario or 0

            if cantidad < 0:
                raise ValidationError('La cantidad no puede ser negativa.')

            if precio < 0:
                raise ValidationError('El precio unitario no puede ser negativo.')

            record.subtotal = cantidad * precio

    @api.constrains('producto_id', 'cantidad', 'precio_unitario')
    def _check_detalle_venta(self):
        for record in self:
            if not record.producto_id:
                raise ValidationError('Debe seleccionar un producto.')

            if not record.producto_id.exists():
                raise ValidationError('El producto seleccionado no existe.')

            if hasattr(record.producto_id, 'activo') and not record.producto_id.activo:
                raise ValidationError(
                    f'El producto {record.producto_id.name} está inactivo.'
                )

            if record.cantidad <= 0:
                raise ValidationError('La cantidad debe ser mayor a cero.')

            if record.precio_unitario <= 0:
                raise ValidationError('El precio unitario debe ser mayor a cero.')

            if record.producto_id.precio_unitario <= 0:
                raise ValidationError(
                    f'El producto {record.producto_id.name} no tiene un precio válido.'
                )

    def validar_stock_disponible(self):
        for record in self:
            if not record.producto_id:
                raise ValidationError('Debe seleccionar un producto.')

            if record.cantidad > record.producto_id.stock_disponible:
                raise ValidationError(
                    f'No hay suficiente stock para el producto {record.producto_id.name}. '
                    f'Stock disponible: {record.producto_id.stock_disponible}. '
                    f'Cantidad solicitada: {record.cantidad}.'
                )

    def descontar_stock(self):
        for record in self:
            record.validar_stock_disponible()

            nuevo_stock = record.producto_id.stock_disponible - record.cantidad

            if nuevo_stock < 0:
                raise ValidationError(
                    f'El stock del producto {record.producto_id.name} no puede quedar negativo.'
                )

            record.producto_id.sudo().write({
                'stock_disponible': nuevo_stock
            })

    def restaurar_stock(self):
        for record in self:
            if record.producto_id:
                record.producto_id.sudo().write({
                    'stock_disponible': record.producto_id.stock_disponible + record.cantidad
                })

    def to_dict(self):
        self.ensure_one()

        return {
            'id': self.id,
            'producto_id': self.producto_id.id,
            'producto_name': self.producto_id.name or '',
            'producto_codigo': self.producto_id.codigo or '',
            'cantidad': self.cantidad or 0,
            'precio_unitario': self.precio_unitario or 0,
            'subtotal': self.subtotal or 0,
            'stock_actual': self.producto_id.stock_disponible or 0,
        }
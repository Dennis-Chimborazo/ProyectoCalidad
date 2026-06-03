from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
import random
import time


class TechstoreVenta(models.Model):
    _name = 'techstore.venta'
    _description = 'Venta TechStore'
    _order = 'create_date desc'

    name = fields.Char(
        string='Referencia',
        default='Nueva venta',
        readonly=True
    )

    cliente_id = fields.Many2one(
        'techstore.cliente',
        string='Cliente',
        required=True
    )

    detalle_ids = fields.One2many(
        'techstore.detalle.venta',
        'venta_id',
        string='Detalle de venta'
    )

    subtotal = fields.Float(
        string='Subtotal',
        compute='_compute_totales',
        store=True
    )

    descuento = fields.Float(
        string='Descuento global',
        default=0.0
    )

    iva = fields.Float(
        string='IVA',
        compute='_compute_totales',
        store=True
    )

    total = fields.Float(
        string='Total',
        compute='_compute_totales',
        store=True
    )

    tiempo_respuesta = fields.Float(
        string='Tiempo de respuesta'
    )

    estado_calidad = fields.Selection(
        [
            ('pendiente', 'Pendiente'),
            ('observado', 'Observado'),
            ('aceptable', 'Aceptable'),
        ],
        string='Estado de calidad',
        default='pendiente'
    )

    observacion = fields.Text(
        string='Observación'
    )

    @api.depends('detalle_ids.subtotal', 'descuento')
    def _compute_totales(self):
        for venta in self:
            subtotal_bruto = sum(venta.detalle_ids.mapped('subtotal'))
            descuento = venta.descuento or 0

            subtotal_final = subtotal_bruto - descuento

            if subtotal_final < 0:
                subtotal_final = 0

            venta.subtotal = subtotal_final
            venta.iva = subtotal_final * 0.15
            venta.total = subtotal_final + venta.iva

    def _validar_cliente(self, cliente):
        if not cliente or not cliente.exists():
            raise ValidationError('Debe seleccionar un cliente válido.')

        if hasattr(cliente, 'activo') and not cliente.activo:
            raise ValidationError('No se puede vender a un cliente inactivo.')

    def _validar_descuento(self, descuento, subtotal_bruto):
        if descuento < 0:
            raise ValidationError('El descuento no puede ser negativo.')

        if descuento > subtotal_bruto:
            raise ValidationError('El descuento no puede ser mayor al subtotal de la venta.')

    def _validar_detalles_values(self, detalles):
        if not detalles:
            raise ValidationError('Debe agregar al menos un producto a la venta.')

        productos_repetidos = set()

        for detalle in detalles:
            producto_id = int(detalle.get('producto_id') or 0)
            cantidad = int(detalle.get('cantidad') or 0)

            producto = self.env['techstore.producto'].browse(producto_id)

            if not producto.exists():
                raise ValidationError('Uno de los productos seleccionados no existe.')

            if hasattr(producto, 'activo') and not producto.activo:
                raise ValidationError(f'El producto {producto.name} está inactivo.')

            if producto.precio_unitario <= 0:
                raise ValidationError(f'El producto {producto.name} no tiene un precio válido.')

            if cantidad <= 0:
                raise ValidationError(f'La cantidad del producto {producto.name} debe ser mayor a cero.')

            if cantidad > producto.stock_disponible:
                raise ValidationError(
                    f'No hay suficiente stock para {producto.name}. '
                    f'Stock disponible: {producto.stock_disponible}. '
                    f'Cantidad solicitada: {cantidad}.'
                )

            if producto_id in productos_repetidos:
                raise ValidationError(
                    f'El producto {producto.name} está repetido en el detalle. '
                    f'Use una sola línea con la cantidad total.'
                )

            productos_repetidos.add(producto_id)

    def _generar_referencia(self):
        fecha = datetime.now().strftime('%Y%m%d%H%M%S')
        aleatorio = random.randint(100, 999)
        return f'VTA-{fecha}-{aleatorio}'

    @api.constrains('cliente_id', 'detalle_ids', 'descuento')
    def _check_venta(self):
        if self.env.context.get('skip_venta_detalle_check'):
            return

        for venta in self:
            venta._validar_cliente(venta.cliente_id)

            if not venta.detalle_ids:
                raise ValidationError('Debe agregar al menos un detalle de venta.')

            subtotal_bruto = sum(venta.detalle_ids.mapped('subtotal'))
            venta._validar_descuento(venta.descuento or 0, subtotal_bruto)

    @api.model
    def create_venta_custom(self, values):
        cliente_id = int(values.get('cliente_id') or 0)
        descuento = float(values.get('descuento') or 0)
        observacion = values.get('observacion') or ''
        detalles = values.get('detalles') or []

        cliente = self.env['techstore.cliente'].browse(cliente_id)
        self._validar_cliente(cliente)
        self._validar_detalles_values(detalles)

        subtotal_bruto = 0

        for item in detalles:
            producto = self.env['techstore.producto'].browse(int(item.get('producto_id')))
            cantidad = int(item.get('cantidad') or 0)
            subtotal_bruto += cantidad * producto.precio_unitario

        self._validar_descuento(descuento, subtotal_bruto)

        tiempo = random.uniform(0.10, 2.50)
        time.sleep(0.05)

        venta = self.with_context(skip_venta_detalle_check=True).create({
            'name': self._generar_referencia(),
            'cliente_id': cliente.id,
            'descuento': descuento,
            'tiempo_respuesta': tiempo,
            'estado_calidad': 'aceptable',
            'observacion': observacion,
        })

        for item in detalles:
            producto = self.env['techstore.producto'].browse(int(item.get('producto_id')))
            cantidad = int(item.get('cantidad') or 0)

            detalle = self.env['techstore.detalle.venta'].create({
                'venta_id': venta.id,
                'producto_id': producto.id,
                'cantidad': cantidad,
                'precio_unitario': producto.precio_unitario,
            })

            detalle.descontar_stock()

        venta._compute_totales()

        return self._venta_to_dict(venta)

    @api.model
    def update_venta_custom(self, venta_id, values):
        venta = self.browse(int(venta_id or 0))

        if not venta.exists():
            raise ValidationError('La venta no existe.')

        cliente_id = int(values.get('cliente_id') or 0)
        descuento = float(values.get('descuento') or 0)
        observacion = values.get('observacion') or ''
        detalles = values.get('detalles') or []

        cliente = self.env['techstore.cliente'].browse(cliente_id)
        self._validar_cliente(cliente)

        for detalle in venta.detalle_ids:
            detalle.restaurar_stock()

        venta.with_context(skip_venta_detalle_check=True).detalle_ids.unlink()

        self._validar_detalles_values(detalles)

        subtotal_bruto = 0

        for item in detalles:
            producto = self.env['techstore.producto'].browse(int(item.get('producto_id')))
            cantidad = int(item.get('cantidad') or 0)
            subtotal_bruto += cantidad * producto.precio_unitario

        self._validar_descuento(descuento, subtotal_bruto)

        venta.with_context(skip_venta_detalle_check=True).write({
            'cliente_id': cliente.id,
            'descuento': descuento,
            'observacion': observacion,
            'estado_calidad': 'aceptable',
        })

        for item in detalles:
            producto = self.env['techstore.producto'].browse(int(item.get('producto_id')))
            cantidad = int(item.get('cantidad') or 0)

            detalle = self.env['techstore.detalle.venta'].create({
                'venta_id': venta.id,
                'producto_id': producto.id,
                'cantidad': cantidad,
                'precio_unitario': producto.precio_unitario,
            })

            detalle.descontar_stock()

        venta._compute_totales()

        return self._venta_to_dict(venta)

    @api.model
    def delete_venta_custom(self, venta_id):
        venta = self.browse(int(venta_id or 0))

        if not venta.exists():
            raise ValidationError('La venta no existe.')

        venta.unlink()

        return True

    def unlink(self):
        if not self.env.context.get('skip_restore_stock'):
            for venta in self:
                for detalle in venta.detalle_ids:
                    detalle.restaurar_stock()

        return super().unlink()

    @api.model
    def get_ventas_data(self):
        ventas = self.search([], order='create_date desc')

        return [
            self._venta_to_dict(venta)
            for venta in ventas
        ]

    @api.model
    def get_venta_catalogos(self):
        clientes = self.env['techstore.cliente'].search([
            ('activo', '=', True)
        ], order='name asc')

        productos = self.env['techstore.producto'].search([
            ('activo', '=', True),
            ('stock_disponible', '>', 0)
        ], order='name asc')

        return {
            'clientes': [
                {
                    'id': cliente.id,
                    'label': cliente.name,
                    'cedula': cliente.cedula or '',
                }
                for cliente in clientes
            ],
            'productos': [
                {
                    'id': producto.id,
                    'label': producto.name,
                    'codigo': producto.codigo or '',
                    'precio_unitario': producto.precio_unitario or 0,
                    'stock_disponible': producto.stock_disponible or 0,
                }
                for producto in productos
            ],
        }

    def _venta_to_dict(self, venta):
        return {
            'id': venta.id,
            'name': venta.name or '',
            'cliente_id': venta.cliente_id.id,
            'cliente_name': venta.cliente_id.name or '',
            'cliente_cedula': venta.cliente_id.cedula or '',
            'subtotal': venta.subtotal or 0,
            'descuento': venta.descuento or 0,
            'iva': venta.iva or 0,
            'total': venta.total or 0,
            'tiempo_respuesta': round(venta.tiempo_respuesta or 0, 2),
            'estado_calidad': venta.estado_calidad or 'pendiente',
            'observacion': venta.observacion or '',
            'create_date': str(venta.create_date or ''),
            'detalles': [
                detalle.to_dict()
                for detalle in venta.detalle_ids
            ],
            'productos_resumen': ', '.join([
                f'{detalle.producto_id.name} x{detalle.cantidad}'
                for detalle in venta.detalle_ids
            ]),
            'cantidad_productos': len(venta.detalle_ids),
        }

    def action_marcar_aceptable(self):
        for venta in self:
            venta.estado_calidad = 'aceptable'

    def action_marcar_observado(self):
        for venta in self:
            venta.estado_calidad = 'observado'
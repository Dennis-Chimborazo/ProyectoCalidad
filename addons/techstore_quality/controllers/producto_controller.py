from odoo import http
from odoo.http import request
from .base_controller import TechstoreBaseController


class TechstoreProductoController(http.Controller, TechstoreBaseController):

    @http.route(
        "/techstore_quality/api/productos",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False
    )
    def get_productos(self, **kwargs):
        try:
            productos = request.env["techstore.producto"].sudo().get_productos_data()

            return self._json_response({
                "success": True,
                "total": len(productos),
                "data": productos,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=500)

    @http.route(
        "/techstore_quality/api/productos/<int:producto_id>",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False
    )
    def get_producto_by_id(self, producto_id, **kwargs):
        try:
            producto = request.env["techstore.producto"].sudo().get_producto_by_id_custom(producto_id)

            return self._json_response({
                "success": True,
                "data": producto,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=404)

    @http.route(
        "/techstore_quality/api/productos",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False
    )
    def create_producto(self, **kwargs):
        try:
            values = self._get_json_body()

            producto = request.env["techstore.producto"].sudo().create_producto_custom(values)

            return self._json_response({
                "success": True,
                "message": "Producto creado correctamente.",
                "data": producto,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    @http.route(
        "/techstore_quality/api/productos/<int:producto_id>",
        type="http",
        auth="public",
        methods=["PUT"],
        csrf=False
    )
    def update_producto(self, producto_id, **kwargs):
        try:
            values = self._get_json_body()

            producto = request.env["techstore.producto"].sudo().update_producto_custom(
                producto_id,
                values
            )

            return self._json_response({
                "success": True,
                "message": "Producto actualizado correctamente.",
                "data": producto,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    @http.route(
        "/techstore_quality/api/productos/<int:producto_id>/toggle",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False
    )
    def toggle_producto(self, producto_id, **kwargs):
        try:
            producto = request.env["techstore.producto"].sudo().toggle_producto_activo_custom(producto_id)

            return self._json_response({
                "success": True,
                "message": "Estado del producto actualizado.",
                "data": producto,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)
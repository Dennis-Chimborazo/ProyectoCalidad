from odoo import http
from odoo.http import request
from .base_controller import TechstoreBaseController


class TechstoreClienteController(http.Controller, TechstoreBaseController):

    @http.route(
        "/techstore_quality/api/clientes",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False
    )
    def get_clientes(self, **kwargs):
        try:
            clientes = request.env["techstore.cliente"].sudo().get_clientes_data()

            return self._json_response({
                "success": True,
                "total": len(clientes),
                "data": clientes,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=500)

    @http.route(
        "/techstore_quality/api/clientes/<int:cliente_id>",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False
    )
    def get_cliente_by_id(self, cliente_id, **kwargs):
        try:
            cliente = request.env["techstore.cliente"].sudo().get_cliente_by_id_custom(cliente_id)

            return self._json_response({
                "success": True,
                "data": cliente,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=404)

    @http.route(
        "/techstore_quality/api/clientes",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False
    )
    def create_cliente(self, **kwargs):
        try:
            values = self._get_json_body()

            cliente = request.env["techstore.cliente"].sudo().create_cliente_custom(values)

            return self._json_response({
                "success": True,
                "message": "Cliente creado correctamente.",
                "data": cliente,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    @http.route(
        "/techstore_quality/api/clientes/<int:cliente_id>",
        type="http",
        auth="public",
        methods=["PUT"],
        csrf=False
    )
    def update_cliente(self, cliente_id, **kwargs):
        try:
            values = self._get_json_body()

            cliente = request.env["techstore.cliente"].sudo().update_cliente_custom(
                cliente_id,
                values
            )

            return self._json_response({
                "success": True,
                "message": "Cliente actualizado correctamente.",
                "data": cliente,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    @http.route(
        "/techstore_quality/api/clientes/<int:cliente_id>/toggle",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False
    )
    def toggle_cliente(self, cliente_id, **kwargs):
        try:
            cliente = request.env["techstore.cliente"].sudo().toggle_cliente_activo_custom(cliente_id)

            return self._json_response({
                "success": True,
                "message": "Estado del cliente actualizado.",
                "data": cliente,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)
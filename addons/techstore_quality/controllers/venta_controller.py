from odoo import http
from odoo.http import request
from .base_controller import TechstoreBaseController


class TechstoreVentaController(http.Controller, TechstoreBaseController):

    @http.route(
        "/techstore_quality/api/ventas",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False
    )
    def get_ventas(self, **kwargs):
        try:
            ventas = request.env["techstore.venta"].sudo().get_ventas_data()

            return self._json_response({
                "success": True,
                "total": len(ventas),
                "data": ventas,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=500)

    @http.route(
        "/techstore_quality/api/ventas/<int:venta_id>",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False
    )
    def get_venta_by_id(self, venta_id, **kwargs):
        try:
            venta = request.env["techstore.venta"].sudo().get_venta_by_id_custom(venta_id)

            return self._json_response({
                "success": True,
                "data": venta,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=404)

    @http.route(
        "/techstore_quality/api/ventas/catalogos",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False
    )
    def get_catalogos_venta(self, **kwargs):
        try:
            catalogos = request.env["techstore.venta"].sudo().get_venta_catalogos()

            return self._json_response({
                "success": True,
                "data": catalogos,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=500)

    @http.route(
        "/techstore_quality/api/ventas",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False
    )
    def create_venta(self, **kwargs):
        try:
            values = self._get_json_body()

            venta = request.env["techstore.venta"].sudo().create_venta_custom(values)

            return self._json_response({
                "success": True,
                "message": "Venta creada correctamente.",
                "data": venta,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    @http.route(
        "/techstore_quality/api/ventas/<int:venta_id>",
        type="http",
        auth="public",
        methods=["PUT"],
        csrf=False
    )
    def update_venta(self, venta_id, **kwargs):
        try:
            values = self._get_json_body()

            venta = request.env["techstore.venta"].sudo().update_venta_custom(
                venta_id,
                values
            )

            return self._json_response({
                "success": True,
                "message": "Venta actualizada correctamente.",
                "data": venta,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    @http.route(
        "/techstore_quality/api/ventas/<int:venta_id>/delete",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False
    )
    def delete_venta(self, venta_id, **kwargs):
        try:
            request.env["techstore.venta"].sudo().delete_venta_custom(venta_id)

            return self._json_response({
                "success": True,
                "message": "Venta eliminada correctamente. El stock fue restaurado.",
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    @http.route(
        "/techstore_quality/api/ventas/<int:venta_id>/detalles",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False
    )
    def get_detalles_by_venta(self, venta_id, **kwargs):
        try:
            venta = request.env["techstore.venta"].sudo().get_venta_by_id_custom(venta_id)

            return self._json_response({
                "success": True,
                "venta": venta.get("name"),
                "total_detalles": len(venta.get("detalles", [])),
                "data": venta.get("detalles", []),
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=404)
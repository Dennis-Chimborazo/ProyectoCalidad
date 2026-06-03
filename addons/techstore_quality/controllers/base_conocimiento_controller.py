from odoo import http
from odoo.http import request
from .base_controller import TechstoreBaseController


class TechstoreBaseConocimientoController(http.Controller, TechstoreBaseController):

    @http.route(
        "/techstore_quality/api/base_conocimiento",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False
    )
    def get_base_conocimiento(self, **kwargs):
        try:
            # Aprovechamos el filtro opcional por tipo de equipo desde Query Params (?equipment_type_id=X)
            equipment_type_id = kwargs.get("equipment_type_id", None)
            
            registros = request.env["techstore.base.conocimiento"].sudo().get_base_conocimiento_data(
                equipment_type_id=equipment_type_id
            )

            return self._json_response({
                "success": True,
                "total": len(registros),
                "data": registros,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=500)

    @http.route(
        "/techstore_quality/api/base_conocimiento/<int:base_id>",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False
    )
    def get_base_conocimiento_by_id(self, base_id, **kwargs):
        try:
            registro = request.env["techstore.base.conocimiento"].sudo().get_base_conocimiento_by_id_custom(base_id)

            return self._json_response({
                "success": True,
                "data": registro,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=404)

    @http.route(
        "/techstore_quality/api/base_conocimiento",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False
    )
    def create_base_conocimiento(self, **kwargs):
        try:
            values = self._get_json_body()

            registro = request.env["techstore.base.conocimiento"].sudo().create_base_conocimiento_custom(values)

            return self._json_response({
                "success": True,
                "message": "Registro de base de conocimiento creado correctamente.",
                "data": registro,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    @http.route(
        "/techstore_quality/api/base_conocimiento/<int:base_id>",
        type="http",
        auth="public",
        methods=["PUT"],
        csrf=False
    )
    def update_base_conocimiento(self, base_id, **kwargs):
        try:
            values = self._get_json_body()

            registro = request.env["techstore.base.conocimiento"].sudo().update_base_conocimiento_custom(
                base_id,
                values
            )

            return self._json_response({
                "success": True,
                "message": "Registro de base de conocimiento actualizado correctamente.",
                "data": registro,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    @http.route(
        "/techstore_quality/api/base_conocimiento/<int:base_id>/toggle",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False
    )
    def toggle_base_conocimiento(self, base_id, **kwargs):
        try:
            registro = request.env["techstore.base.conocimiento"].sudo().toggle_base_conocimiento_activo_custom(base_id)

            return self._json_response({
                "success": True,
                "message": "Estado del registro de conocimiento actualizado.",
                "data": registro,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)
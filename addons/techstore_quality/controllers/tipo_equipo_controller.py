from odoo import http
from odoo.http import request
from .base_controller import TechstoreBaseController


class TechstoreTipoEquipoController(http.Controller, TechstoreBaseController):

    @http.route(
        "/techstore_quality/api/tipos_equipo",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False
    )
    def get_tipos_equipo(self, **kwargs):
        try:
            tipos = request.env["techstore.tipo.equipo"].sudo().get_tipos_equipo_data()

            return self._json_response({
                "success": True,
                "total": len(tipos),
                "data": tipos,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=500)

    @http.route(
        "/techstore_quality/api/tipos_equipo/<int:tipo_equipo_id>",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False
    )
    def get_tipo_equipo_by_id(self, tipo_equipo_id, **kwargs):
        try:
            tipo = request.env["techstore.tipo.equipo"].sudo().get_tipo_equipo_by_id_custom(tipo_equipo_id)

            return self._json_response({
                "success": True,
                "data": tipo,
            })

        except Exception as error:
            # Se usa 404 porque el modelo levanta una ValidationError si no existe
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=404)

    @http.route(
        "/techstore_quality/api/tipos_equipo",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False
    )
    def create_tipo_equipo(self, **kwargs):
        try:
            values = self._get_json_body()

            tipo = request.env["techstore.tipo.equipo"].sudo().create_tipo_equipo_custom(values)

            return self._json_response({
                "success": True,
                "message": "Tipo de equipo creado correctamente.",
                "data": tipo,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    @http.route(
        "/techstore_quality/api/tipos_equipo/<int:tipo_equipo_id>",
        type="http",
        auth="public",
        methods=["PUT"],
        csrf=False
    )
    def update_tipo_equipo(self, tipo_equipo_id, **kwargs):
        try:
            values = self._get_json_body()

            tipo = request.env["techstore.tipo.equipo"].sudo().update_tipo_equipo_custom(
                tipo_equipo_id,
                values
            )

            return self._json_response({
                "success": True,
                "message": "Tipo de equipo actualizado correctamente.",
                "data": tipo,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    @http.route(
        "/techstore_quality/api/tipos_equipo/<int:tipo_equipo_id>/toggle",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False
    )
    def toggle_tipo_equipo(self, tipo_equipo_id, **kwargs):
        try:
            tipo = request.env["techstore.tipo.equipo"].sudo().toggle_tipo_equipo_activo_custom(tipo_equipo_id)

            return self._json_response({
                "success": True,
                "message": "Estado del tipo de equipo actualizado.",
                "data": tipo,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)
from odoo import http
from odoo.http import request
from .base_controller import TechstoreBaseController


class TechstoreTecnicoController(http.Controller, TechstoreBaseController):

    @http.route(
        "/techstore_quality/api/tecnicos",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False
    )
    def get_tecnicos(self, **kwargs):
        try:
            tecnicos = request.env["techstore.tecnico"].sudo().get_tecnicos_data()

            return self._json_response({
                "success": True,
                "total": len(tecnicos),
                "data": tecnicos,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=500)

    @http.route(
        "/techstore_quality/api/tecnicos/<int:tecnico_id>",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False
    )
    def get_tecnico_by_id(self, tecnico_id, **kwargs):
        try:
            tecnico = request.env["techstore.tecnico"].sudo().get_tecnico_by_id_custom(tecnico_id)

            return self._json_response({
                "success": True,
                "data": tecnico,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=404)

    @http.route(
        "/techstore_quality/api/tecnicos",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False
    )
    def create_tecnico(self, **kwargs):
        try:
            values = self._get_json_body()

            tecnico = request.env["techstore.tecnico"].sudo().create_tecnico_custom(values)

            return self._json_response({
                "success": True,
                "message": "Técnico creado correctamente.",
                "data": tecnico,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    @http.route(
        "/techstore_quality/api/tecnicos/<int:tecnico_id>",
        type="http",
        auth="public",
        methods=["PUT"],
        csrf=False
    )
    def update_tecnico(self, tecnico_id, **kwargs):
        try:
            values = self._get_json_body()

            tecnico = request.env["techstore.tecnico"].sudo().update_tecnico_custom(
                tecnico_id,
                values
            )

            return self._json_response({
                "success": True,
                "message": "Técnico actualizado correctamente.",
                "data": tecnico,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    @http.route(
        "/techstore_quality/api/tecnicos/<int:tecnico_id>/toggle",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False
    )
    def toggle_tecnico(self, tecnico_id, **kwargs):
        try:
            tecnico = request.env["techstore.tecnico"].sudo().toggle_tecnico_activo_custom(tecnico_id)

            return self._json_response({
                "success": True,
                "message": "Estado del técnico actualizado.",
                "data": tecnico,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)
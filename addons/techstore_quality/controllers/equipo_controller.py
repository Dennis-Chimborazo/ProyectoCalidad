from odoo import http
from odoo.http import request
from .base_controller import TechstoreBaseController


class TechstoreEquipoController(http.Controller, TechstoreBaseController):

    # =========================================================================
    # ENDPOINTS PARA EL EQUIPO PRINCIPAL (techstore.equipo)
    # =========================================================================

    @http.route(
        "/techstore_quality/api/equipos",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False
    )
    def get_equipos(self, **kwargs):
        try:
            equipos = request.env["techstore.equipo"].sudo().get_equipos_data()

            return self._json_response({
                "success": True,
                "total": len(equipos),
                "data": equipos,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=500)

    @http.route(
        "/techstore_quality/api/equipos/<int:equipo_id>",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False
    )
    def get_equipo_by_id(self, equipo_id, **kwargs):
        try:
            equipo = request.env["techstore.equipo"].sudo().get_equipo_by_id_custom(equipo_id)

            return self._json_response({
                "success": True,
                "data": equipo,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=404)

    @http.route(
        "/techstore_quality/api/equipos",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False
    )
    def create_equipo(self, **kwargs):
        try:
            values = self._get_json_body()

            equipo = request.env["techstore.equipo"].sudo().create_equipo_custom(values)

            return self._json_response({
                "success": True,
                "message": "Equipo creado correctamente.",
                "data": equipo,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    @http.route(
        "/techstore_quality/api/equipos/<int:equipo_id>",
        type="http",
        auth="public",
        methods=["PUT"],
        csrf=False
    )
    def update_equipo(self, equipo_id, **kwargs):
        try:
            values = self._get_json_body()

            equipo = request.env["techstore.equipo"].sudo().update_equipo_custom(
                equipo_id,
                values
            )

            return self._json_response({
                "success": True,
                "message": "Equipo actualizado correctamente.",
                "data": equipo,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    @http.route(
        "/techstore_quality/api/equipos/<int:equipo_id>",
        type="http",
        auth="public",
        methods=["DELETE"],
        csrf=False
    )
    def delete_equipo(self, equipo_id, **kwargs):
        try:
            result = request.env["techstore.equipo"].sudo().delete_equipo_custom(equipo_id)

            return self._json_response({
                "success": True,
                "message": "Equipo eliminado correctamente.",
                "data": result,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    # =========================================================================
    # ENDPOINTS PARA CARACTERÍSTICAS/DETALLES (techstore.detalle.equipo)
    # =========================================================================

    @http.route(
        "/techstore_quality/api/equipos/detalles",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False
    )
    def get_detalles_equipo(self, **kwargs):
        try:
            # Permite filtrar detalles usando un query param: ?equipo_id=X
            equipo_id = kwargs.get("equipo_id", None)

            detalles = request.env["techstore.detalle.equipo"].sudo().get_detalles_equipo_data(
                equipo_id=equipo_id
            )

            return self._json_response({
                "success": True,
                "total": len(detalles),
                "data": detalles,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=500)

    @http.route(
        "/techstore_quality/api/equipos/detalles",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False
    )
    def create_detalle_equipo(self, **kwargs):
        try:
            values = self._get_json_body()

            detalle = request.env["techstore.detalle.equipo"].sudo().create_detalle_equipo_custom(values)

            return self._json_response({
                "success": True,
                "message": "Característica agregada al equipo correctamente.",
                "data": detalle,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    @http.route(
        "/techstore_quality/api/equipos/detalles/<int:detalle_id>",
        type="http",
        auth="public",
        methods=["PUT"],
        csrf=False
    )
    def update_detalle_equipo(self, detalle_id, **kwargs):
        try:
            values = self._get_json_body()

            detalle = request.env["techstore.detalle.equipo"].sudo().update_detalle_equipo_custom(
                detalle_id,
                values
            )

            return self._json_response({
                "success": True,
                "message": "Característica modificada correctamente.",
                "data": detalle,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    @http.route(
        "/techstore_quality/api/equipos/detalles/<int:detalle_id>",
        type="http",
        auth="public",
        methods=["DELETE"],
        csrf=False
    )
    def delete_detalle_equipo(self, detalle_id, **kwargs):
        try:
            result = request.env["techstore.detalle.equipo"].sudo().delete_detalle_equipo_custom(detalle_id)

            return self._json_response({
                "success": True,
                "message": "Característica eliminada correctamente del equipo.",
                "data": result,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)
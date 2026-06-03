from odoo import http
from odoo.http import request
from .base_controller import TechstoreBaseController


class TechstoreMantenimientoController(http.Controller, TechstoreBaseController):

    # =========================================================================
    # 1. ORDEN DE MANTENIMIENTO GLOBAL (techstore.mantenimiento)
    # =========================================================================

    @http.route(
        "/techstore_quality/api/mantenimientos",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False
    )
    def get_mantenimientos(self, **kwargs):
        try:
            mantenimientos = request.env["techstore.mantenimiento"].sudo().get_mantenimientos_data()

            return self._json_response({
                "success": True,
                "total": len(mantenimientos),
                "data": mantenimientos,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=500)

    @http.route(
        "/techstore_quality/api/mantenimientos/<int:mantenimiento_id>",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False
    )
    def get_mantenimiento_by_id(self, mantenimiento_id, **kwargs):
        try:
            mantenimiento = request.env["techstore.mantenimiento"].sudo().get_mantenimiento_by_id_custom(mantenimiento_id)

            return self._json_response({
                "success": True,
                "data": mantenimiento,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=404)

    @http.route(
        "/techstore_quality/api/mantenimientos",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False
    )
    def create_mantenimiento(self, **kwargs):
        try:
            values = self._get_json_body()
            mantenimiento = request.env["techstore.mantenimiento"].sudo().create_mantenimiento_custom(values)

            return self._json_response({
                "success": True,
                "message": "Orden de mantenimiento generada correctamente.",
                "data": mantenimiento,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    @http.route(
        "/techstore_quality/api/mantenimientos/<int:mantenimiento_id>/estado",
        type="http",
        auth="public",
        methods=["PUT"],
        csrf=False
    )
    def update_estado_mantenimiento(self, mantenimiento_id, **kwargs):
        try:
            values = self._get_json_body()
            nuevo_estado = values.get("estado")

            mantenimiento = request.env["techstore.mantenimiento"].sudo().update_estado_mantenimiento_custom(
                mantenimiento_id, 
                nuevo_estado
            )

            return self._json_response({
                "success": True,
                "message": f"Mantenimiento actualizado al estado: {nuevo_estado}.",
                "data": mantenimiento,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    # =========================================================================
    # 2. ENDPOINTS ESPECIALIZADOS (Dashboard e Información Extendida)
    # =========================================================================

    @http.route(
        "/techstore_quality/api/mantenimientos/dashboard",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False
    )
    def get_dashboard_data(self, **kwargs):
        try:
            dashboard = request.env["techstore.mantenimiento"].sudo().get_dashboard_mantenimientos_data()

            return self._json_response({
                "success": True,
                "data": dashboard,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=500)

    @http.route(
        "/techstore_quality/api/mantenimientos/<int:mantenimiento_id>/info",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False
    )
    def get_mantenimiento_info_completa(self, mantenimiento_id, **kwargs):
        try:
            info = request.env["techstore.mantenimiento"].sudo().get_mantenimiento_info_custom(mantenimiento_id)

            return self._json_response({
                "success": True,
                "data": info,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=404)

    # =========================================================================
    # 3. EQUIPOS ASOCIADOS AL MANTENIMIENTO (techstore.mantenimiento.equipo)
    # =========================================================================

    @http.route(
        "/techstore_quality/api/mantenimientos/equipos",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False
    )
    def get_equipos_mantenimiento(self, **kwargs):
        try:
            mantenimiento_id = kwargs.get("mantenimiento_id", None)
            registros = request.env["techstore.mantenimiento.equipo"].sudo().get_equipos_mantenimiento_data(mantenimiento_id)

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
        "/techstore_quality/api/mantenimientos/equipos/vincular",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False
    )
    def create_or_attach_equipo(self, **kwargs):
        try:
            values = self._get_json_body()
            # Utiliza tu lógica inteligente que busca duplicados por serie o crea el equipo base con sus detalles
            result = request.env["techstore.mantenimiento.equipo"].sudo().create_or_attach_equipo_custom(values)

            return self._json_response(result)

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    @http.route(
        "/techstore_quality/api/mantenimientos/equipos/<int:mantenimiento_equipo_id>/estado",
        type="http",
        auth="public",
        methods=["PUT"],
        csrf=False
    )
    def update_estado_equipo_mantenimiento(self, mantenimiento_equipo_id, **kwargs):
        try:
            values = self._get_json_body()
            nuevo_estado = values.get("estado_equipo")

            # Este método también verifica internamente si debe cerrar el mantenimiento global
            result = request.env["techstore.mantenimiento.equipo"].sudo().update_estado_equipo_custom(
                mantenimiento_equipo_id, 
                nuevo_estado
            )

            return self._json_response({
                "success": True,
                "message": "Estado del equipo actualizado de forma correcta.",
                "data": result,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    @http.route(
        "/techstore_quality/api/mantenimientos/equipos/<int:mantenimiento_equipo_id>/solucion",
        type="http",
        auth="public",
        methods=["PUT"],
        csrf=False
    )
    def update_solucion_equipo_mantenimiento(self, mantenimiento_equipo_id, **kwargs):
        try:
            values = self._get_json_body()
            result = request.env["techstore.mantenimiento.equipo"].sudo().update_solucion_equipo_custom(
                mantenimiento_equipo_id, 
                values
            )

            return self._json_response({
                "success": True,
                "message": "Solución del equipo actualizada correctamente.",
                "data": result,
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    # =========================================================================
    # 4. FALLAS ENCONTRADAS VS BASE CONOCIMIENTO (techstore.mantenimiento.equipo.falla)
    # =========================================================================

    @http.route(
        "/techstore_quality/api/mantenimientos/equipos/fallas",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False
    )
    def agregar_falla_desde_base(self, **kwargs):
        try:
            values = self._get_json_body()
            
            # Validación manual rápida previa antes de insertar en el modelo cruzado
            m_equipo_id = values.get("mantenimiento_equipo_id")
            base_id = values.get("base_conocimiento_id")
            
            if not m_equipo_id or not base_id:
                return self._json_response({
                    "success": False,
                    "message": "Faltan parámetros: mantenimiento_equipo_id y base_conocimiento_id son requeridos."
                }, status=400)

            falla_vinculo = request.env["techstore.mantenimiento.equipo.falla"].sudo().create({
                "mantenimiento_equipo_id": int(m_equipo_id),
                "base_conocimiento_id": int(base_id),
            })

            return self._json_response({
                "success": True,
                "message": "Falla de la base de conocimiento vinculada correctamente al equipo.",
                "data": falla_vinculo._mantenimiento_equipo_falla_to_dict(),
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)

    @http.route(
        "/techstore_quality/api/mantenimientos/equipos/fallas/<int:falla_id>",
        type="http",
        auth="public",
        methods=["DELETE"],
        csrf=False
    )
    def eliminar_falla_vinculada(self, falla_id, **kwargs):
        try:
            falla_registro = request.env["techstore.mantenimiento.equipo.falla"].sudo().browse(falla_id)

            if not falla_registro.exists():
                return self._json_response({
                    "success": False,
                    "message": "El vínculo de la falla especificada no existe.",
                }, status=404)

            falla_registro.unlink()

            return self._json_response({
                "success": True,
                "message": "Vínculo de falla removido del equipo de manera correcta.",
                "data": {"id": falla_id, "deleted": True}
            })

        except Exception as error:
            return self._json_response({
                "success": False,
                "message": str(error),
            }, status=400)
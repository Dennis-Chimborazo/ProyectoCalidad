from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class TechstoreMantenimiento(models.Model):
    _name = "techstore.mantenimiento"
    _description = "Orden de Mantenimiento TechStore"
    _order = "id desc"

    name = fields.Char(
        string="Código de mantenimiento",
        required=True,
        copy=False,
        readonly=True,
        default="Nuevo"
    )

    cliente_id = fields.Many2one(
        "techstore.cliente",
        string="Cliente",
        required=True
    )

    tecnico_id = fields.Many2one(
        "techstore.tecnico",
        string="Técnico asignado",
        required=True
    )

    fecha_inicio = fields.Datetime(
        string="Fecha de inicio"
    )

    fecha_fin = fields.Datetime(
        string="Fecha de finalización"
    )

    prioridad = fields.Selection(
        [
            ("baja", "Baja"),
            ("media", "Media"),
            ("alta", "Alta"),
            ("critica", "Crítica"),
        ],
        string="Prioridad",
        required=True,
        default="media"
    )

    estado = fields.Selection(
        [
            ("pendiente", "Pendiente"),
            ("en_proceso", "En proceso"),
            ("finalizado", "Finalizado"),
            ("cancelado", "Cancelado"),
        ],
        string="Estado",
        required=True,
        default="pendiente"
    )

    descripcion_general = fields.Text(
        string="Descripción general",
        required=True
    )

    equipo_mantenimiento_ids = fields.One2many(
        "techstore.mantenimiento.equipo",
        "mantenimiento_id",
        string="Equipos del mantenimiento"
    )

    total_equipos = fields.Integer(
        string="Total de equipos",
        compute="_compute_total_equipos",
        store=True
    )

    @api.depends("equipo_mantenimiento_ids")
    def _compute_total_equipos(self):
        for record in self:
            record.total_equipos = len(record.equipo_mantenimiento_ids)

    @api.constrains("descripcion_general")
    def _check_descripcion_general(self):
        for record in self:
            if record.descripcion_general and len(record.descripcion_general.strip()) < 10:
                raise ValidationError(
                    "La descripción general debe tener al menos 10 caracteres."
                )

    @api.constrains("fecha_inicio", "fecha_fin")
    def _check_fechas(self):
        for record in self:
            if record.fecha_inicio and record.fecha_fin:
                if record.fecha_fin < record.fecha_inicio:
                    raise ValidationError(
                        "La fecha de finalización no puede ser menor que la fecha de inicio."
                    )

    @api.constrains("tecnico_id")
    def _check_tecnico_activo(self):
        for record in self:
            if record.tecnico_id and not record.tecnico_id.activo:
                raise ValidationError(
                    "No se puede asignar un técnico inactivo."
                )

    def _normalize_datetime_value(self, value):
        if not value:
            return False

        if isinstance(value, str):
            value = value.replace("T", " ")

            if len(value) == 16:
                value = f"{value}:00"

        return value

    @api.model
    def create(self, vals):
        # Lógica para generar el código personalizado MANT-(FECHA)-CONTEO
        if vals.get("name", "Nuevo") == "Nuevo":
            # 1. Obtener la fecha actual local/servidor
            hoy = datetime.now()
            fecha_str = hoy.strftime("%Y%m%d") # Resultado ejemplo: 20260603
            prefix = f"MANT-{fecha_str}-"

            # 2. Buscar cuántos registros se han creado hoy con este prefijo
            # Usamos una consulta rápida con el operador 'like'
            mantenimientos_hoy = self.search_count([
                ("name", "like", f"{prefix}%")
            ])

            # 3. Calcular el nuevo secuencial incrementando en 1
            nuevo_secuencial = mantenimientos_hoy + 1
            
            # 4. Formatear el código rellenando con ceros a la izquierda (001, 002, etc.)
            vals["name"] = f"{prefix}{str(nuevo_secuencial).zfill(3)}"

        if vals.get("descripcion_general"):
            vals["descripcion_general"] = vals.get("descripcion_general").strip()

        if vals.get("fecha_inicio"):
            vals["fecha_inicio"] = self._normalize_datetime_value(
                vals.get("fecha_inicio")
            )

        if vals.get("fecha_fin"):
            vals["fecha_fin"] = self._normalize_datetime_value(
                vals.get("fecha_fin")
            )

        return super().create(vals)

    def write(self, vals):
        if vals.get("descripcion_general"):
            vals["descripcion_general"] = vals.get("descripcion_general").strip()

        if vals.get("fecha_inicio"):
            vals["fecha_inicio"] = self._normalize_datetime_value(
                vals.get("fecha_inicio")
            )

        if vals.get("fecha_fin"):
            vals["fecha_fin"] = self._normalize_datetime_value(
                vals.get("fecha_fin")
            )

        return super().write(vals)

    def _mantenimiento_to_dict(self):
        self.ensure_one()

        return {
            "id": self.id,
            "name": self.name or "",
            "cliente_id": self.cliente_id.id,
            "cliente": self.cliente_id.name or "",
            "tecnico_id": self.tecnico_id.id,
            "tecnico": self.tecnico_id.name or "",
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "prioridad": self.prioridad or "",
            "estado": self.estado or "",
            "descripcion_general": self.descripcion_general or "",
            "total_equipos": self.total_equipos,
        }

    @api.model
    def get_mantenimientos_data(self):
        mantenimientos = self.search([], order="id desc")

        return [
            mantenimiento._mantenimiento_to_dict()
            for mantenimiento in mantenimientos
        ]

    @api.model
    def get_mantenimiento_by_id_custom(self, mantenimiento_id):
        mantenimiento = self.browse(int(mantenimiento_id))

        if not mantenimiento.exists():
            raise ValidationError("El mantenimiento no existe.")

        return mantenimiento._mantenimiento_to_dict()

    @api.model
    def create_mantenimiento_custom(self, values):
        cliente_id = values.get("cliente_id")
        tecnico_id = values.get("tecnico_id")

        if not cliente_id:
            raise ValidationError("Debe seleccionar un cliente.")

        if not tecnico_id:
            raise ValidationError("Debe seleccionar un técnico.")

        cliente = self.env["techstore.cliente"].browse(int(cliente_id))

        if not cliente.exists():
            raise ValidationError("El cliente no existe.")

        tecnico = self.env["techstore.tecnico"].browse(int(tecnico_id))

        if not tecnico.exists():
            raise ValidationError("El técnico no existe.")

        if not tecnico.activo:
            raise ValidationError("No se puede asignar un técnico inactivo.")

        mantenimiento = self.create({
            "cliente_id": cliente.id,
            "tecnico_id": tecnico.id,
            "fecha_inicio": fields.Datetime.now(),
            "fecha_fin": False,
            "prioridad": values.get("prioridad", "media"),
            "estado": "pendiente",
            "descripcion_general": values.get("descripcion_general"),
        })

        return mantenimiento._mantenimiento_to_dict()

    @api.model
    def update_estado_mantenimiento_custom(self, mantenimiento_id, estado):
        mantenimiento = self.browse(int(mantenimiento_id))

        if not mantenimiento.exists():
            raise ValidationError("El mantenimiento no existe.")

        estados_validos = [
            "pendiente",
            "en_proceso",
            "finalizado",
            "cancelado",
        ]

        if estado not in estados_validos:
            raise ValidationError("Estado de mantenimiento no válido.")

        vals = {
            "estado": estado
        }

        if estado == "en_proceso" and not mantenimiento.fecha_inicio:
            vals["fecha_inicio"] = fields.Datetime.now()

        if estado == "finalizado" and not mantenimiento.fecha_fin:
            vals["fecha_fin"] = fields.Datetime.now()

        mantenimiento.write(vals)

        return mantenimiento._mantenimiento_to_dict()

    @api.model
    def cancelar_mantenimiento_custom(self, mantenimiento_id):
        mantenimiento = self.browse(int(mantenimiento_id))

        if not mantenimiento.exists():
            raise ValidationError("El mantenimiento no existe.")

        mantenimiento.write({
            "estado": "cancelado"
        })

        return mantenimiento._mantenimiento_to_dict()

    @api.model
    def finalizar_mantenimiento_custom(self, mantenimiento_id):
        mantenimiento = self.browse(int(mantenimiento_id))

        if not mantenimiento.exists():
            raise ValidationError("El mantenimiento no existe.")

        mantenimiento.write({
            "estado": "finalizado",
            "fecha_fin": fields.Datetime.now(),
        })

        return mantenimiento._mantenimiento_to_dict()
    @api.model
    def cerrar_si_todos_equipos_cerrados_custom(self, mantenimiento_id):
        mantenimiento = self.browse(int(mantenimiento_id))

        if not mantenimiento.exists():
            raise ValidationError("El mantenimiento no existe.")

        equipos = mantenimiento.equipo_mantenimiento_ids

        if not equipos:
            return {
                "cerrado": False,
                "mantenimiento": mantenimiento._mantenimiento_to_dict(),
            }

        todos_cerrados = all(
            equipo.estado_equipo in ["finalizado", "cancelado"]
            for equipo in equipos
        )

        if todos_cerrados and mantenimiento.estado != "finalizado":
            mantenimiento.write({
                "estado": "finalizado",
                "fecha_fin": fields.Datetime.now(),
            })

            return {
                "cerrado": True,
                "mantenimiento": mantenimiento._mantenimiento_to_dict(),
            }

        return {
            "cerrado": False,
            "mantenimiento": mantenimiento._mantenimiento_to_dict(),
        }
        
    @api.model
    def get_mantenimiento_info_custom(self, mantenimiento_id):
        mantenimiento = self.browse(int(mantenimiento_id))

        if not mantenimiento.exists():
            raise ValidationError("El mantenimiento no existe.")

        equipos_data = []

        for mantenimiento_equipo in mantenimiento.equipo_mantenimiento_ids:
            fallas = self.env["techstore.mantenimiento.equipo.falla"].search([
                ("mantenimiento_equipo_id", "=", mantenimiento_equipo.id)
            ])

            equipos_data.append({
                "id": mantenimiento_equipo.id,
                "equipo_id": mantenimiento_equipo.equipo_id.id,
                "equipo": mantenimiento_equipo.equipo_id.name or "",
                "tipo_equipo": mantenimiento_equipo.equipo_id.tipo_equipo_id.name or "",
                "marca": mantenimiento_equipo.equipo_id.marca or "",
                "modelo": mantenimiento_equipo.equipo_id.modelo or "",
                "numero_serie": mantenimiento_equipo.equipo_id.numero_serie or "",
                "color": mantenimiento_equipo.equipo_id.color or "",
                "descripcion": mantenimiento_equipo.equipo_id.descripcion or "",
                "estado_equipo": mantenimiento_equipo.estado_equipo or "",
                "falla_reportada": mantenimiento_equipo.falla_reportada or "",
                "solucion": mantenimiento_equipo.solucion or "",
                "detalles": [
                    detalle._detalle_equipo_to_dict()
                    for detalle in mantenimiento_equipo.equipo_id.detalle_ids
                ],
                "fallas_base": [
                    falla._mantenimiento_equipo_falla_to_dict()
                    for falla in fallas
                ],
            })

        total_equipos = len(equipos_data)

        total_finalizados = len([
            item for item in equipos_data
            if item["estado_equipo"] == "finalizado"
        ])

        total_cancelados = len([
            item for item in equipos_data
            if item["estado_equipo"] == "cancelado"
        ])

        total_en_proceso = len([
            item for item in equipos_data
            if item["estado_equipo"] == "en_proceso"
        ])

        total_pendientes = len([
            item for item in equipos_data
            if item["estado_equipo"] == "pendiente"
        ])

        total_con_solucion = len([
            item for item in equipos_data
            if item["solucion"]
        ])

        total_con_base_conocimiento = len([
            item for item in equipos_data
            if item["fallas_base"]
        ])

        return {
            "id": mantenimiento.id,
            "name": mantenimiento.name or "",
            "cliente_id": mantenimiento.cliente_id.id,
            "cliente": mantenimiento.cliente_id.name or "",
            "tecnico_id": mantenimiento.tecnico_id.id,
            "tecnico": mantenimiento.tecnico_id.name or "",
            "fecha_inicio": mantenimiento.fecha_inicio,
            "fecha_fin": mantenimiento.fecha_fin,
            "prioridad": mantenimiento.prioridad or "",
            "estado": mantenimiento.estado or "",
            "descripcion_general": mantenimiento.descripcion_general or "",
            "total_equipos": total_equipos,
            "total_finalizados": total_finalizados,
            "total_cancelados": total_cancelados,
            "total_en_proceso": total_en_proceso,
            "total_pendientes": total_pendientes,
            "total_con_solucion": total_con_solucion,
            "total_con_base_conocimiento": total_con_base_conocimiento,
            "equipos": equipos_data,
        }
    
    @api.model
    def get_dashboard_mantenimientos_data(self):
        mantenimientos = self.search([], order="id desc")
        mantenimiento_equipos = self.env["techstore.mantenimiento.equipo"].search([])
        fallas_base = self.env["techstore.mantenimiento.equipo.falla"].search([])

        clientes = self.env["techstore.cliente"].search([], order="name asc")
        tipos_equipo = self.env["techstore.tipo.equipo"].search([], order="name asc")

        fallas_by_mantenimiento_equipo = {}
        for falla in fallas_base:
            mantenimiento_equipo_id = falla.mantenimiento_equipo_id.id

            if mantenimiento_equipo_id not in fallas_by_mantenimiento_equipo:
                fallas_by_mantenimiento_equipo[mantenimiento_equipo_id] = []

            fallas_by_mantenimiento_equipo[mantenimiento_equipo_id].append(
                falla._mantenimiento_equipo_falla_to_dict()
            )

        mantenimientos_data = []
        equipos_data = []

        for mantenimiento in mantenimientos:
            mantenimientos_data.append({
                "id": mantenimiento.id,
                "name": mantenimiento.name or "",
                "cliente_id": mantenimiento.cliente_id.id,
                "cliente": mantenimiento.cliente_id.name or "",
                "tipo_cliente": mantenimiento.cliente_id.tipo_cliente or "",
                "tipo_cliente_label": "Corporativo" if mantenimiento.cliente_id.tipo_cliente == "corporativo" else "Particular",
                "tecnico_id": mantenimiento.tecnico_id.id,
                "tecnico": mantenimiento.tecnico_id.name or "",
                "fecha_inicio": mantenimiento.fecha_inicio,
                "fecha_fin": mantenimiento.fecha_fin,
                "prioridad": mantenimiento.prioridad or "",
                "estado": mantenimiento.estado or "",
                "descripcion_general": mantenimiento.descripcion_general or "",
                "total_equipos": mantenimiento.total_equipos,
            })

        for item in mantenimiento_equipos:
            fallas = fallas_by_mantenimiento_equipo.get(item.id, [])

            equipos_data.append({
                "id": item.id,
                "mantenimiento_id": item.mantenimiento_id.id,
                "mantenimiento": item.mantenimiento_id.name or "",

                "cliente_id": item.mantenimiento_id.cliente_id.id,
                "cliente": item.mantenimiento_id.cliente_id.name or "",
                "tipo_cliente": item.mantenimiento_id.cliente_id.tipo_cliente or "",
                "tipo_cliente_label": "Corporativo" if item.mantenimiento_id.cliente_id.tipo_cliente == "corporativo" else "Particular",

                "tecnico_id": item.mantenimiento_id.tecnico_id.id,
                "tecnico": item.mantenimiento_id.tecnico_id.name or "",

                "prioridad": item.mantenimiento_id.prioridad or "",
                "estado_mantenimiento": item.mantenimiento_id.estado or "",

                "equipo_id": item.equipo_id.id,
                "equipo": item.equipo_id.name or "",
                "tipo_equipo_id": item.equipo_id.tipo_equipo_id.id,
                "tipo_equipo": item.equipo_id.tipo_equipo_id.name or "",

                "marca": item.equipo_id.marca or "",
                "modelo": item.equipo_id.modelo or "",
                "numero_serie": item.equipo_id.numero_serie or "",

                "estado_equipo": item.estado_equipo or "",
                "falla_reportada": item.falla_reportada or "",
                "solucion": item.solucion or "",

                "tiene_solucion": bool(item.solucion),
                "tiene_base_conocimiento": bool(fallas),
                "fallas_base": fallas,
            })

        return {
            "mantenimientos": mantenimientos_data,
            "equipos": equipos_data,
            "clientes": [
                {
                    "id": cliente.id,
                    "label": cliente.name or "",
                }
                for cliente in clientes
            ],
            "tipos_equipo": [
                {
                    "id": tipo.id,
                    "label": tipo.name or "",
                }
                for tipo in tipos_equipo
            ],
        }
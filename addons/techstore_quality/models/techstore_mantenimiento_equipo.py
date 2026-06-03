from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TechstoreMantenimientoEquipo(models.Model):
    _name = "techstore.mantenimiento.equipo"
    _description = "Equipo asignado a mantenimiento TechStore"
    _order = "id desc"

    mantenimiento_id = fields.Many2one(
        "techstore.mantenimiento",
        string="Mantenimiento",
        required=True,
        ondelete="cascade"
    )

    equipo_id = fields.Many2one(
        "techstore.equipo",
        string="Equipo",
        required=True
    )

    estado_equipo = fields.Selection(
        [
            ("pendiente", "Pendiente"),
            ("en_proceso", "En proceso"),
            ("finalizado", "Finalizado"),
            ("cancelado", "Cancelado"),
        ],
        string="Estado del equipo",
        required=True,
        default="pendiente"
    )

    falla_reportada = fields.Text(
        string="Falla reportada"
    )

    solucion = fields.Text(
        string="Solución aplicada"
    )

    @api.constrains("mantenimiento_id", "equipo_id")
    def _check_mantenimiento_equipo(self):
        for record in self:
            if record.mantenimiento_id and record.equipo_id:
                existente = self.search([
                    ("id", "!=", record.id),
                    ("mantenimiento_id", "=", record.mantenimiento_id.id),
                    ("equipo_id", "=", record.equipo_id.id),
                ], limit=1)

                if existente:
                    raise ValidationError(
                        "Este equipo ya está asignado a este mantenimiento."
                    )

    @api.constrains("falla_reportada")
    def _check_falla_reportada(self):
        for record in self:
            if record.falla_reportada and len(record.falla_reportada.strip()) < 5:
                raise ValidationError(
                    "La falla reportada debe tener al menos 5 caracteres."
                )

    @api.constrains("solucion")
    def _check_solucion(self):
        for record in self:
            if record.solucion and len(record.solucion.strip()) < 5:
                raise ValidationError(
                    "La solución aplicada debe tener al menos 5 caracteres."
                )

    def _mantenimiento_equipo_to_dict(self):
        self.ensure_one()

        return {
            "id": self.id,
            "mantenimiento_id": self.mantenimiento_id.id,
            "mantenimiento": self.mantenimiento_id.name or "",

            "equipo_id": self.equipo_id.id,
            "equipo": self.equipo_id.name or "",

            "tipo_equipo_id": self.equipo_id.tipo_equipo_id.id,
            "tipo_equipo": self.equipo_id.tipo_equipo_id.name or "",

            "marca": self.equipo_id.marca or "",
            "modelo": self.equipo_id.modelo or "",
            "numero_serie": self.equipo_id.numero_serie or "",
            "color": self.equipo_id.color or "",
            "descripcion": self.equipo_id.descripcion or "",

            "estado_equipo": self.estado_equipo or "",
            "falla_reportada": self.falla_reportada or "",
            "solucion": self.solucion or "",

            "detalles": [
                detalle._detalle_equipo_to_dict()
                for detalle in self.equipo_id.detalle_ids
            ],
        }

    @api.model
    def get_equipos_mantenimiento_data(self, mantenimiento_id=None):
        domain = []

        if mantenimiento_id:
            domain.append(("mantenimiento_id", "=", int(mantenimiento_id)))

        registros = self.search(domain, order="id desc")

        return [
            registro._mantenimiento_equipo_to_dict()
            for registro in registros
        ]

    @api.model
    def get_mantenimiento_equipo_by_id_custom(self, mantenimiento_equipo_id):
        registro = self.browse(int(mantenimiento_equipo_id))

        if not registro.exists():
            raise ValidationError("El equipo asignado al mantenimiento no existe.")

        return registro._mantenimiento_equipo_to_dict()

    @api.model
    def create_mantenimiento_equipo_custom(self, values):
        mantenimiento_id = values.get("mantenimiento_id")
        equipo_id = values.get("equipo_id")
        solucion = (values.get("solucion") or "").strip()

        if not mantenimiento_id:
            raise ValidationError("Debe seleccionar un mantenimiento.")

        if not equipo_id:
            raise ValidationError("Debe seleccionar un equipo.")

        mantenimiento = self.env["techstore.mantenimiento"].browse(
            int(mantenimiento_id)
        )

        if not mantenimiento.exists():
            raise ValidationError("El mantenimiento no existe.")

        equipo = self.env["techstore.equipo"].browse(
            int(equipo_id)
        )

        if not equipo.exists():
            raise ValidationError("El equipo no existe.")

        registro = self.create({
            "mantenimiento_id": mantenimiento.id,
            "equipo_id": equipo.id,
            "estado_equipo": "pendiente",
            "falla_reportada": values.get("falla_reportada") or False,
            "solucion": solucion or False,
        })

        return registro._mantenimiento_equipo_to_dict()
    @api.model
    def update_estado_equipo_custom(self, mantenimiento_equipo_id, estado_equipo):
        registro = self.browse(int(mantenimiento_equipo_id))

        if not registro.exists():
            raise ValidationError("El equipo asignado al mantenimiento no existe.")

        estados_validos = [
            "pendiente",
            "en_proceso",
            "finalizado",
            "cancelado",
        ]

        if estado_equipo not in estados_validos:
            raise ValidationError("Estado del equipo no válido.")

        registro.write({
            "estado_equipo": estado_equipo
        })

        cierre = self.env["techstore.mantenimiento"].cerrar_si_todos_equipos_cerrados_custom(
            registro.mantenimiento_id.id
        )

        result = registro._mantenimiento_equipo_to_dict()
        result["mantenimiento_cerrado"] = cierre.get("cerrado", False)
        result["mantenimiento"] = cierre.get("mantenimiento")

        return result

    @api.model
    def update_solucion_equipo_custom(self, mantenimiento_equipo_id, values):
        registro = self.browse(int(mantenimiento_equipo_id))

        if not registro.exists():
            raise ValidationError("El equipo asignado al mantenimiento no existe.")

        solucion = (values.get("solucion") or "").strip()

        registro.write({
            "solucion": solucion or False,
        })

        return registro._mantenimiento_equipo_to_dict()

    @api.model
    def create_or_attach_equipo_custom(self, values):
        mantenimiento_id = values.get("mantenimiento_id")
        equipo_values = values.get("equipo") or {}

        if not mantenimiento_id:
            raise ValidationError("Debe existir un mantenimiento seleccionado.")

        mantenimiento = self.env["techstore.mantenimiento"].browse(
            int(mantenimiento_id)
        )

        if not mantenimiento.exists():
            raise ValidationError("El mantenimiento no existe.")

        name = (equipo_values.get("name") or "").strip()
        tipo_equipo_id = equipo_values.get("tipo_equipo_id")
        numero_serie = (equipo_values.get("numero_serie") or "").strip().upper()
        falla_reportada = (equipo_values.get("falla_reportada") or "").strip()
        solucion = (equipo_values.get("solucion") or "").strip()
        detalles_values = equipo_values.get("detalles", [])

        if not name or len(name) < 3:
            raise ValidationError(
                "El nombre del equipo debe tener al menos 3 caracteres."
            )

        if not tipo_equipo_id:
            raise ValidationError(
                "Debe seleccionar un tipo de equipo."
            )

        if not numero_serie or len(numero_serie) < 3:
            raise ValidationError(
                "El número de serie debe tener al menos 3 caracteres."
            )

        if not falla_reportada or len(falla_reportada) < 5:
            raise ValidationError(
                "Debe registrar la falla reportada del equipo."
            )

        equipo = self.env["techstore.equipo"].search([
            ("numero_serie", "=", numero_serie)
        ], limit=1)

        warning = ""

        if equipo:
            warning = (
                f"El equipo con serie {numero_serie} ya estaba registrado. "
                "Se reutilizó el registro existente."
            )

            otro_cliente = self.search([
                ("equipo_id", "=", equipo.id),
                ("mantenimiento_id.cliente_id", "!=", mantenimiento.cliente_id.id),
            ], limit=1)

            if otro_cliente:
                warning += " Además, este equipo ya estuvo asociado a otro cliente."

        else:
            equipo = self.env["techstore.equipo"].create({
                "name": name,
                "tipo_equipo_id": int(tipo_equipo_id),
                "marca": equipo_values.get("marca") or False,
                "modelo": equipo_values.get("modelo") or False,
                "numero_serie": numero_serie,
                "color": equipo_values.get("color") or False,
                "descripcion": equipo_values.get("descripcion") or False,
            })

        existente_mantenimiento = self.search([
            ("mantenimiento_id", "=", mantenimiento.id),
            ("equipo_id", "=", equipo.id),
        ], limit=1)

        if existente_mantenimiento:
            raise ValidationError(
                "Este equipo ya está agregado a este mantenimiento."
            )

        for detalle_values in detalles_values:
            caracteristica = (detalle_values.get("name") or "").strip()
            valor = (detalle_values.get("valor") or "").strip()

            if not caracteristica or len(caracteristica) < 2:
                raise ValidationError(
                    "Cada característica debe tener al menos 2 caracteres."
                )

            if not valor:
                raise ValidationError(
                    "Cada característica debe tener un valor."
                )

            detalle_existente = self.env["techstore.detalle.equipo"].search([
                ("equipo_id", "=", equipo.id),
                ("name", "=", caracteristica),
                ("valor", "=", valor),
            ], limit=1)

            if not detalle_existente:
                self.env["techstore.detalle.equipo"].create({
                    "equipo_id": equipo.id,
                    "name": caracteristica,
                    "valor": valor,
                })

        registro = self.create({
            "mantenimiento_id": mantenimiento.id,
            "equipo_id": equipo.id,
            "estado_equipo": "pendiente",
            "falla_reportada": falla_reportada,
            "solucion": solucion or False,
        })

        return {
            "success": True,
            "item": registro._mantenimiento_equipo_to_dict(),
            "warning": warning,
        }
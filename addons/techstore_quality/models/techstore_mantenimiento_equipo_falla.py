from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TechstoreMantenimientoEquipoFalla(models.Model):
    _name = "techstore.mantenimiento.equipo.falla"
    _description = "Falla documentada asociada a equipo en mantenimiento TechStore"
    _order = "id desc"

    mantenimiento_equipo_id = fields.Many2one(
        "techstore.mantenimiento.equipo",
        string="Equipo en mantenimiento",
        required=True,
        ondelete="cascade"
    )

    mantenimiento_id = fields.Many2one(
        "techstore.mantenimiento",
        string="Mantenimiento",
        related="mantenimiento_equipo_id.mantenimiento_id",
        store=True,
        readonly=True
    )

    base_conocimiento_id = fields.Many2one(
        "techstore.base.conocimiento",
        string="Falla documentada",
        required=True
    )

    @api.constrains("mantenimiento_equipo_id", "base_conocimiento_id")
    def _check_falla_repetida(self):
        for record in self:
            if record.mantenimiento_equipo_id and record.base_conocimiento_id:
                existente = self.search([
                    ("id", "!=", record.id),
                    ("mantenimiento_equipo_id", "=", record.mantenimiento_equipo_id.id),
                    ("base_conocimiento_id", "=", record.base_conocimiento_id.id),
                ], limit=1)

                if existente:
                    raise ValidationError(
                        "Esta falla documentada ya fue agregada a este equipo dentro del mantenimiento."
                    )

    @api.constrains("base_conocimiento_id", "mantenimiento_equipo_id")
    def _check_tipo_equipo_compatible(self):
        for record in self:
            if record.base_conocimiento_id and record.mantenimiento_equipo_id:
                tipo_equipo_base = record.base_conocimiento_id.equipment_type_id.id
                tipo_equipo_real = record.mantenimiento_equipo_id.equipo_id.tipo_equipo_id.id

                if tipo_equipo_base != tipo_equipo_real:
                    raise ValidationError(
                        "La falla documentada seleccionada no corresponde al tipo de equipo asignado."
                    )

    def _mantenimiento_equipo_falla_to_dict(self):
        self.ensure_one()

        base = self.base_conocimiento_id

        return {
            "id": self.id,

            "mantenimiento_id": self.mantenimiento_id.id,
            "mantenimiento": self.mantenimiento_id.name or "",

            "mantenimiento_equipo_id": self.mantenimiento_equipo_id.id,
            "equipo_id": self.mantenimiento_equipo_id.equipo_id.id,
            "equipo": self.mantenimiento_equipo_id.equipo_id.name or "",

            "base_conocimiento_id": base.id,
            "error_title": base.error_title or "",

            "equipment_type_id": base.equipment_type_id.id,
            "equipment_type": base.equipment_type_id.name or "",

            "symptoms": base.symptoms or "",
            "root_cause": base.root_cause or "",
            "solution": base.solution or "",
            "keywords": base.keywords or "",
        }

    @api.model
    def get_fallas_mantenimiento_equipo_data(self, mantenimiento_equipo_id=None, mantenimiento_id=None):
        domain = []

        if mantenimiento_equipo_id:
            domain.append(("mantenimiento_equipo_id", "=", int(mantenimiento_equipo_id)))

        if mantenimiento_id:
            domain.append(("mantenimiento_id", "=", int(mantenimiento_id)))

        registros = self.search(domain, order="id desc")

        return [
            registro._mantenimiento_equipo_falla_to_dict()
            for registro in registros
        ]

    @api.model
    def create_mantenimiento_equipo_falla_custom(self, values):
        mantenimiento_equipo_id = values.get("mantenimiento_equipo_id")
        base_conocimiento_id = values.get("base_conocimiento_id")

        if not mantenimiento_equipo_id:
            raise ValidationError("Debe seleccionar el equipo dentro del mantenimiento.")

        if not base_conocimiento_id:
            raise ValidationError("Debe seleccionar una falla documentada.")

        mantenimiento_equipo = self.env["techstore.mantenimiento.equipo"].browse(
            int(mantenimiento_equipo_id)
        )

        if not mantenimiento_equipo.exists():
            raise ValidationError("El equipo asignado al mantenimiento no existe.")

        base = self.env["techstore.base.conocimiento"].browse(
            int(base_conocimiento_id)
        )

        if not base.exists():
            raise ValidationError("La falla documentada no existe.")

        registro = self.create({
            "mantenimiento_equipo_id": mantenimiento_equipo.id,
            "base_conocimiento_id": base.id,
        })

        return registro._mantenimiento_equipo_falla_to_dict()

    @api.model
    def delete_mantenimiento_equipo_falla_custom(self, falla_id):
        registro = self.browse(int(falla_id))

        if not registro.exists():
            raise ValidationError("La falla documentada asociada no existe.")

        result = {
            "id": registro.id,
            "deleted": True,
        }

        registro.unlink()

        return result
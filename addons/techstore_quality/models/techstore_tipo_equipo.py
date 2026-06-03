from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TechstoreTipoEquipo(models.Model):
    _name = "techstore.tipo.equipo"
    _description = "Tipo de Equipo TechStore"
    _order = "name"

    name = fields.Char(
        string="Tipo de equipo",
        required=True
    )

    descripcion = fields.Text(
        string="Descripción"
    )

    activo = fields.Boolean(
        string="Activo",
        default=True
    )

    _sql_constraints = [
        (
            "unique_name_tipo_equipo",
            "unique(name)",
            "El tipo de equipo ya está registrado."
        ),
    ]

    @api.constrains("name")
    def _check_name(self):
        for record in self:
            if record.name and len(record.name.strip()) < 3:
                raise ValidationError(
                    "El tipo de equipo debe tener al menos 3 caracteres."
                )

    @api.model
    def create(self, vals):
        if vals.get("name"):
            vals["name"] = vals.get("name").strip()

        return super().create(vals)

    def write(self, vals):
        if vals.get("name"):
            vals["name"] = vals.get("name").strip()

        return super().write(vals)

    def _tipo_equipo_to_dict(self):
        self.ensure_one()

        return {
            "id": self.id,
            "name": self.name or "",
            "descripcion": self.descripcion or "",
            "activo": self.activo,
        }

    @api.model
    def get_tipos_equipo_data(self):
        tipos = self.search([], order="name asc")

        return [
            tipo._tipo_equipo_to_dict()
            for tipo in tipos
        ]

    @api.model
    def get_tipo_equipo_by_id_custom(self, tipo_equipo_id):
        tipo = self.browse(tipo_equipo_id)

        if not tipo.exists():
            raise ValidationError("El tipo de equipo no existe.")

        return tipo._tipo_equipo_to_dict()

    @api.model
    def create_tipo_equipo_custom(self, values):
        tipo = self.create({
            "name": values.get("name"),
            "descripcion": values.get("descripcion") or False,
            "activo": values.get("activo", True),
        })

        return tipo._tipo_equipo_to_dict()

    @api.model
    def update_tipo_equipo_custom(self, tipo_equipo_id, values):
        tipo = self.browse(tipo_equipo_id)

        if not tipo.exists():
            raise ValidationError("El tipo de equipo no existe.")

        tipo.write({
            "name": values.get("name", tipo.name),
            "descripcion": values.get("descripcion", tipo.descripcion) or False,
            "activo": values.get("activo", tipo.activo),
        })

        return tipo._tipo_equipo_to_dict()

    @api.model
    def toggle_tipo_equipo_activo_custom(self, tipo_equipo_id):
        tipo = self.browse(tipo_equipo_id)

        if not tipo.exists():
            raise ValidationError("El tipo de equipo no existe.")

        tipo.write({
            "activo": not tipo.activo
        })

        return {
            "id": tipo.id,
            "activo": tipo.activo,
        }
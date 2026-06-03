from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TechstoreDetalleEquipo(models.Model):
    _name = "techstore.detalle.equipo"
    _description = "Detalle de Equipo TechStore"
    _order = "name"

    equipo_id = fields.Many2one(
        "techstore.equipo",
        string="Equipo",
        required=True,
        ondelete="cascade"
    )

    name = fields.Char(
        string="Característica",
        required=True
    )

    valor = fields.Char(
        string="Valor",
        required=True
    )

    @api.constrains("name")
    def _check_name(self):
        for record in self:
            if record.name and len(record.name.strip()) < 2:
                raise ValidationError(
                    "La característica debe tener al menos 2 caracteres."
                )

    @api.constrains("valor")
    def _check_valor(self):
        for record in self:
            if record.valor and len(record.valor.strip()) < 1:
                raise ValidationError(
                    "El valor de la característica no puede estar vacío."
                )

    @api.model
    def create(self, vals):
        if vals.get("name"):
            vals["name"] = vals.get("name").strip()

        if vals.get("valor"):
            vals["valor"] = vals.get("valor").strip()

        return super().create(vals)

    def write(self, vals):
        if vals.get("name"):
            vals["name"] = vals.get("name").strip()

        if vals.get("valor"):
            vals["valor"] = vals.get("valor").strip()

        return super().write(vals)

    def _detalle_equipo_to_dict(self):
        self.ensure_one()

        return {
            "id": self.id,
            "equipo_id": self.equipo_id.id,
            "caracteristica": self.name or "",
            "valor": self.valor or "",
        }

    @api.model
    def get_detalles_equipo_data(self, equipo_id=None):
        domain = []

        if equipo_id:
            domain.append(("equipo_id", "=", int(equipo_id)))

        detalles = self.search(domain, order="name asc")

        return [
            detalle._detalle_equipo_to_dict()
            for detalle in detalles
        ]

    @api.model
    def create_detalle_equipo_custom(self, values):
        equipo_id = values.get("equipo_id")

        if not equipo_id:
            raise ValidationError("Debe existir un equipo seleccionado.")

        equipo = self.env["techstore.equipo"].browse(int(equipo_id))

        if not equipo.exists():
            raise ValidationError("El equipo no existe.")

        detalle = self.create({
            "equipo_id": equipo.id,
            "name": values.get("name"),
            "valor": values.get("valor"),
        })

        return detalle._detalle_equipo_to_dict()

    @api.model
    def update_detalle_equipo_custom(self, detalle_id, values):
        detalle = self.browse(int(detalle_id))

        if not detalle.exists():
            raise ValidationError("El detalle del equipo no existe.")

        detalle.write({
            "name": values.get("name", detalle.name),
            "valor": values.get("valor", detalle.valor),
        })

        return detalle._detalle_equipo_to_dict()

    @api.model
    def delete_detalle_equipo_custom(self, detalle_id):
        detalle = self.browse(int(detalle_id))

        if not detalle.exists():
            raise ValidationError("El detalle del equipo no existe.")

        result = {
            "id": detalle.id,
            "deleted": True,
        }

        detalle.unlink()

        return result
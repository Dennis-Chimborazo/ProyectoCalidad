from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TechstoreEquipo(models.Model):
    _name = "techstore.equipo"
    _description = "Equipo TechStore"
    _order = "name"

    name = fields.Char(
        string="Nombre del equipo",
        required=True
    )

    tipo_equipo_id = fields.Many2one(
        "techstore.tipo.equipo",
        string="Tipo de equipo",
        required=True
    )

    marca = fields.Char(
        string="Marca"
    )

    modelo = fields.Char(
        string="Modelo"
    )

    numero_serie = fields.Char(
        string="Número de serie"
    )

    color = fields.Char(
        string="Color"
    )

    descripcion = fields.Text(
        string="Descripción general"
    )

    detalle_ids = fields.One2many(
        "techstore.detalle.equipo",
        "equipo_id",
        string="Características"
    )

    mantenimiento_equipo_ids = fields.One2many(
        "techstore.mantenimiento.equipo",
        "equipo_id",
        string="Mantenimientos asociados"
    )

    _sql_constraints = [
        (
            "unique_numero_serie_equipo",
            "unique(numero_serie)",
            "El número de serie del equipo ya está registrado."
        ),
    ]

    @api.constrains("name")
    def _check_name(self):
        for record in self:
            if record.name and len(record.name.strip()) < 3:
                raise ValidationError(
                    "El nombre del equipo debe tener al menos 3 caracteres."
                )

    @api.constrains("numero_serie")
    def _check_numero_serie(self):
        for record in self:
            if record.numero_serie and len(record.numero_serie.strip()) < 3:
                raise ValidationError(
                    "El número de serie debe tener al menos 3 caracteres."
                )

    @api.model
    def create(self, vals):
        if vals.get("name"):
            vals["name"] = vals.get("name").strip()

        if vals.get("marca"):
            vals["marca"] = vals.get("marca").strip()

        if vals.get("modelo"):
            vals["modelo"] = vals.get("modelo").strip()

        if vals.get("numero_serie"):
            vals["numero_serie"] = vals.get("numero_serie").strip().upper()

        if vals.get("color"):
            vals["color"] = vals.get("color").strip()

        return super().create(vals)

    def write(self, vals):
        if vals.get("name"):
            vals["name"] = vals.get("name").strip()

        if vals.get("marca"):
            vals["marca"] = vals.get("marca").strip()

        if vals.get("modelo"):
            vals["modelo"] = vals.get("modelo").strip()

        if vals.get("numero_serie"):
            vals["numero_serie"] = vals.get("numero_serie").strip().upper()

        if vals.get("color"):
            vals["color"] = vals.get("color").strip()

        return super().write(vals)

    def _equipo_to_dict(self):
        self.ensure_one()

        return {
            "id": self.id,
            "name": self.name or "",
            "tipo_equipo_id": self.tipo_equipo_id.id,
            "tipo_equipo": self.tipo_equipo_id.name or "",
            "marca": self.marca or "",
            "modelo": self.modelo or "",
            "numero_serie": self.numero_serie or "",
            "color": self.color or "",
            "descripcion": self.descripcion or "",
            "detalles": [
                detalle._detalle_equipo_to_dict()
                for detalle in self.detalle_ids
            ],
        }

    @api.model
    def get_equipos_data(self):
        equipos = self.search([], order="name asc")

        return [
            equipo._equipo_to_dict()
            for equipo in equipos
        ]

    @api.model
    def get_equipo_by_id_custom(self, equipo_id):
        equipo = self.browse(int(equipo_id))

        if not equipo.exists():
            raise ValidationError("El equipo no existe.")

        return equipo._equipo_to_dict()

    @api.model
    def create_equipo_custom(self, values):
        equipo = self.create({
            "name": values.get("name"),
            "tipo_equipo_id": int(values.get("tipo_equipo_id")),
            "marca": values.get("marca") or False,
            "modelo": values.get("modelo") or False,
            "numero_serie": values.get("numero_serie") or False,
            "color": values.get("color") or False,
            "descripcion": values.get("descripcion") or False,
        })

        return equipo._equipo_to_dict()

    @api.model
    def update_equipo_custom(self, equipo_id, values):
        equipo = self.browse(int(equipo_id))

        if not equipo.exists():
            raise ValidationError("El equipo no existe.")

        equipo.write({
            "name": values.get("name", equipo.name),
            "tipo_equipo_id": int(values.get("tipo_equipo_id")) if values.get("tipo_equipo_id") else equipo.tipo_equipo_id.id,
            "marca": values.get("marca", equipo.marca) or False,
            "modelo": values.get("modelo", equipo.modelo) or False,
            "numero_serie": values.get("numero_serie", equipo.numero_serie) or False,
            "color": values.get("color", equipo.color) or False,
            "descripcion": values.get("descripcion", equipo.descripcion) or False,
        })

        return equipo._equipo_to_dict()

    @api.model
    def delete_equipo_custom(self, equipo_id):
        equipo = self.browse(int(equipo_id))

        if not equipo.exists():
            raise ValidationError("El equipo no existe.")

        result = {
            "id": equipo.id,
            "deleted": True,
        }

        equipo.unlink()

        return result
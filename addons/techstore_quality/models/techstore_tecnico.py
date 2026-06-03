from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class TechstoreTecnico(models.Model):
    _name = "techstore.tecnico"
    _description = "Técnico TechStore"
    _order = "name"

    name = fields.Char(
        string="Nombre del técnico",
        required=True
    )

    cedula = fields.Char(
        string="Cédula",
        required=True
    )

    email = fields.Char(
        string="Correo",
        required=True
    )

    telefono = fields.Char(
        string="Teléfono"
    )

    especialidad = fields.Selection(
        [
            ("hardware", "Hardware"),
            ("software", "Software"),
            ("mantenimiento_general", "Mantenimiento general"),
        ],
        string="Especialidad",
        required=True,
        default="mantenimiento_general"
    )

    nivel_experiencia = fields.Selection(
        [
            ("junior", "Junior"),
            ("intermedio", "Intermedio"),
            ("senior", "Senior"),
        ],
        string="Nivel de experiencia",
        required=True,
        default="junior"
    )

    mantenimientos_asignados = fields.Integer(
        string="Mantenimientos asignados",
        compute="_compute_mantenimientos_asignados",
        store=False
    )

    activo = fields.Boolean(
        string="Activo",
        default=True
    )

    _sql_constraints = [
        (
            "unique_cedula_tecnico",
            "unique(cedula)",
            "La cédula del técnico ya está registrada."
        ),
        (
            "unique_email_tecnico",
            "unique(email)",
            "El correo del técnico ya está registrado."
        ),
    ]

    @api.depends("name")
    def _compute_mantenimientos_asignados(self):
        for record in self:
            record.mantenimientos_asignados = self.env["techstore.mantenimiento"].search_count([
                ("tecnico_id", "=", record.id)
            ])

    @api.constrains("name")
    def _check_name(self):
        for record in self:
            if record.name and len(record.name.strip()) < 3:
                raise ValidationError(
                    "El nombre del técnico debe tener al menos 3 caracteres."
                )

    @api.constrains("cedula")
    def _check_cedula(self):
        for record in self:
            if record.cedula:
                cedula = record.cedula.strip()

                if not cedula.isdigit():
                    raise ValidationError(
                        "La cédula solo debe contener números."
                    )

                if len(cedula) != 10:
                    raise ValidationError(
                        "La cédula debe tener 10 dígitos."
                    )

    @api.constrains("email")
    def _check_email(self):
        for record in self:
            if record.email:
                pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

                if not re.match(pattern, record.email):
                    raise ValidationError(
                        "Ingrese un correo electrónico válido."
                    )

    @api.constrains("telefono")
    def _check_telefono(self):
        for record in self:
            if record.telefono:
                telefono = record.telefono.strip()

                if not telefono.isdigit():
                    raise ValidationError(
                        "El teléfono solo debe contener números."
                    )

                if len(telefono) < 7 or len(telefono) > 10:
                    raise ValidationError(
                        "El teléfono debe tener entre 7 y 10 dígitos."
                    )

    @api.model
    def create(self, vals):
        if vals.get("name"):
            vals["name"] = vals.get("name").strip()

        if vals.get("cedula"):
            vals["cedula"] = vals.get("cedula").strip()

        if vals.get("email"):
            vals["email"] = vals.get("email").strip().lower()

        if vals.get("telefono"):
            vals["telefono"] = vals.get("telefono").strip()

        return super().create(vals)

    def write(self, vals):
        if vals.get("name"):
            vals["name"] = vals.get("name").strip()

        if vals.get("cedula"):
            vals["cedula"] = vals.get("cedula").strip()

        if vals.get("email"):
            vals["email"] = vals.get("email").strip().lower()

        if vals.get("telefono"):
            vals["telefono"] = vals.get("telefono").strip()

        return super().write(vals)

    def _tecnico_to_dict(self):
        self.ensure_one()

        return {
            "id": self.id,
            "name": self.name or "",
            "cedula": self.cedula or "",
            "email": self.email or "",
            "telefono": self.telefono or "",
            "especialidad": self.especialidad or "",
            "nivel_experiencia": self.nivel_experiencia or "",
            "mantenimientos_asignados": self.mantenimientos_asignados,
            "activo": self.activo,
        }

    @api.model
    def get_tecnicos_data(self):
        tecnicos = self.search([], order="name asc")

        return [
            tecnico._tecnico_to_dict()
            for tecnico in tecnicos
        ]

    @api.model
    def get_tecnico_by_id_custom(self, tecnico_id):
        tecnico = self.browse(tecnico_id)

        if not tecnico.exists():
            raise ValidationError("El técnico no existe.")

        return tecnico._tecnico_to_dict()

    @api.model
    def create_tecnico_custom(self, values):
        tecnico = self.create({
            "name": values.get("name"),
            "cedula": values.get("cedula"),
            "email": values.get("email"),
            "telefono": values.get("telefono") or False,
            "especialidad": values.get("especialidad", "mantenimiento_general"),
            "nivel_experiencia": values.get("nivel_experiencia", "junior"),
            "activo": values.get("activo", True),
        })

        return tecnico._tecnico_to_dict()

    @api.model
    def update_tecnico_custom(self, tecnico_id, values):
        tecnico = self.browse(tecnico_id)

        if not tecnico.exists():
            raise ValidationError("El técnico no existe.")

        tecnico.write({
            "name": values.get("name", tecnico.name),
            "cedula": values.get("cedula", tecnico.cedula),
            "email": values.get("email", tecnico.email),
            "telefono": values.get("telefono", tecnico.telefono) or False,
            "especialidad": values.get("especialidad", tecnico.especialidad),
            "nivel_experiencia": values.get("nivel_experiencia", tecnico.nivel_experiencia),
            "activo": values.get("activo", tecnico.activo),
        })

        return tecnico._tecnico_to_dict()

    @api.model
    def toggle_tecnico_activo_custom(self, tecnico_id):
        tecnico = self.browse(tecnico_id)

        if not tecnico.exists():
            raise ValidationError("El técnico no existe.")

        tecnico.write({
            "activo": not tecnico.activo
        })

        return {
            "id": tecnico.id,
            "activo": tecnico.activo,
        }
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TechstoreBaseConocimiento(models.Model):
    _name = "techstore.base.conocimiento"
    _description = "Base de Conocimiento TechStore"
    _order = "error_title"

    error_title = fields.Char(
        string="Título de la falla",
        required=True
    )

    equipment_type_id = fields.Many2one(
        "techstore.tipo.equipo",
        string="Tipo de equipo",
        required=True
    )

    symptoms = fields.Text(
        string="Síntomas",
        required=True
    )

    root_cause = fields.Text(
        string="Causa raíz",
        required=True
    )

    solution = fields.Text(
        string="Solución documentada",
        required=True
    )

    keywords = fields.Char(
        string="Palabras clave"
    )

    activo = fields.Boolean(
        string="Activo",
        default=True
    )

    _sql_constraints = [
        (
            "unique_error_title_equipment_type",
            "unique(error_title, equipment_type_id)",
            "Ya existe una falla con ese título para este tipo de equipo."
        ),
    ]

    @api.constrains("error_title")
    def _check_error_title(self):
        for record in self:
            if record.error_title and len(record.error_title.strip()) < 5:
                raise ValidationError(
                    "El título de la falla debe tener al menos 5 caracteres."
                )

    @api.constrains("symptoms", "root_cause", "solution")
    def _check_textos_calidad(self):
        for record in self:
            if record.symptoms and len(record.symptoms.strip()) < 10:
                raise ValidationError(
                    "Los síntomas deben tener al menos 10 caracteres."
                )

            if record.root_cause and len(record.root_cause.strip()) < 10:
                raise ValidationError(
                    "La causa raíz debe tener al menos 10 caracteres."
                )

            if record.solution and len(record.solution.strip()) < 10:
                raise ValidationError(
                    "La solución debe tener al menos 10 caracteres."
                )

    @api.model
    def create(self, vals):
        if vals.get("error_title"):
            vals["error_title"] = vals.get("error_title").strip()

        if vals.get("keywords"):
            vals["keywords"] = vals.get("keywords").strip().lower()

        return super().create(vals)

    def write(self, vals):
        if vals.get("error_title"):
            vals["error_title"] = vals.get("error_title").strip()

        if vals.get("keywords"):
            vals["keywords"] = vals.get("keywords").strip().lower()

        return super().write(vals)

    def _base_conocimiento_to_dict(self):
        self.ensure_one()

        return {
            "id": self.id,
            "error_title": self.error_title or "",
            "equipment_type_id": self.equipment_type_id.id,
            "equipment_type": self.equipment_type_id.name or "",
            "symptoms": self.symptoms or "",
            "root_cause": self.root_cause or "",
            "solution": self.solution or "",
            "keywords": self.keywords or "",
            "activo": self.activo,
        }

    @api.model
    def get_base_conocimiento_data(self, equipment_type_id=None):
        domain = []

        if equipment_type_id:
            domain.append(("equipment_type_id", "=", int(equipment_type_id)))

        registros = self.search(domain, order="error_title asc")

        return [
            registro._base_conocimiento_to_dict()
            for registro in registros
        ]

    @api.model
    def get_base_conocimiento_by_id_custom(self, base_id):
        registro = self.browse(base_id)

        if not registro.exists():
            raise ValidationError("El registro de base de conocimiento no existe.")

        return registro._base_conocimiento_to_dict()

    @api.model
    def create_base_conocimiento_custom(self, values):
        registro = self.create({
            "error_title": values.get("error_title"),
            "equipment_type_id": int(values.get("equipment_type_id")),
            "symptoms": values.get("symptoms"),
            "root_cause": values.get("root_cause"),
            "solution": values.get("solution"),
            "keywords": values.get("keywords") or False,
            "activo": values.get("activo", True),
        })

        return registro._base_conocimiento_to_dict()

    @api.model
    def update_base_conocimiento_custom(self, base_id, values):
        registro = self.browse(base_id)

        if not registro.exists():
            raise ValidationError("El registro de base de conocimiento no existe.")

        registro.write({
            "error_title": values.get("error_title", registro.error_title),
            "equipment_type_id": int(values.get("equipment_type_id")) if values.get("equipment_type_id") else registro.equipment_type_id.id,
            "symptoms": values.get("symptoms", registro.symptoms),
            "root_cause": values.get("root_cause", registro.root_cause),
            "solution": values.get("solution", registro.solution),
            "keywords": values.get("keywords", registro.keywords) or False,
            "activo": values.get("activo", registro.activo),
        })

        return registro._base_conocimiento_to_dict()

    @api.model
    def toggle_base_conocimiento_activo_custom(self, base_id):
        registro = self.browse(base_id)

        if not registro.exists():
            raise ValidationError("El registro de base de conocimiento no existe.")

        registro.write({
            "activo": not registro.activo
        })

        return {
            "id": registro.id,
            "activo": registro.activo,
        }
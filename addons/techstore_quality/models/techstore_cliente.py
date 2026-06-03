from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class TechstoreCliente(models.Model):
    _name = "techstore.cliente"
    _description = "Cliente TechStore"
    _order = "name"

    name = fields.Char(
        string="Nombre del cliente",
        required=True
    )

    tipo_cliente = fields.Selection(
        [
            ("particular", "Particular"),
            ("corporativo", "Corporativo"),
        ],
        string="Tipo de cliente",
        required=True,
        default="particular"
    )

    cedula = fields.Char(
        string="Cédula/RUC"
    )

    email = fields.Char(
        string="Correo"
    )

    telefono = fields.Char(
        string="Teléfono"
    )

    activo = fields.Boolean(
        string="Activo",
        default=True
    )

    _sql_constraints = [
        (
            "unique_cedula_cliente",
            "unique(cedula)",
            "La cédula/RUC ya está registrada."
        ),
        (
            "unique_email_cliente",
            "unique(email)",
            "El correo electrónico ya está registrado."
        ),
    ]

    @api.constrains("name")
    def _check_name(self):
        for record in self:
            if record.name and len(record.name.strip()) < 3:
                raise ValidationError("El nombre debe tener al menos 3 caracteres.")

    @api.constrains("tipo_cliente")
    def _check_tipo_cliente(self):
        tipos_validos = ["particular", "corporativo"]

        for record in self:
            if record.tipo_cliente not in tipos_validos:
                raise ValidationError("Tipo de cliente no válido.")

    @api.constrains("email")
    def _check_email(self):
        for record in self:
            if record.email:
                pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

                if not re.match(pattern, record.email):
                    raise ValidationError("Ingrese un correo electrónico válido.")

    @api.constrains("cedula", "tipo_cliente")
    def _check_cedula_ruc(self):
        for record in self:
            if record.cedula:
                cedula = record.cedula.strip()

                if not cedula.isdigit():
                    raise ValidationError("La cédula/RUC solo debe contener números.")

                if record.tipo_cliente == "particular" and len(cedula) != 10:
                    raise ValidationError("Para cliente particular, la cédula debe tener 10 dígitos.")

                if record.tipo_cliente == "corporativo" and len(cedula) != 13:
                    raise ValidationError("Para cliente corporativo, el RUC debe tener 13 dígitos.")

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

    def _cliente_to_dict(self):
        self.ensure_one()

        return {
            "id": self.id,
            "name": self.name or "",
            "tipo_cliente": self.tipo_cliente or "",
            "tipo_cliente_label": self._get_tipo_cliente_label(),
            "cedula": self.cedula or "",
            "email": self.email or "",
            "telefono": self.telefono or "",
            "activo": self.activo,
        }

    def _get_tipo_cliente_label(self):
        labels = {
            "particular": "Particular",
            "corporativo": "Corporativo",
        }

        return labels.get(self.tipo_cliente, self.tipo_cliente or "")

    @api.model
    def get_clientes_data(self):
        clientes = self.search([], order="name asc")

        return [
            cliente._cliente_to_dict()
            for cliente in clientes
        ]

    @api.model
    def create_cliente_custom(self, values):
        cliente = self.create({
            "name": values.get("name"),
            "tipo_cliente": values.get("tipo_cliente", "particular"),
            "cedula": values.get("cedula") or False,
            "email": values.get("email") or False,
            "telefono": values.get("telefono") or False,
            "activo": values.get("activo", True),
        })

        return cliente._cliente_to_dict()

    @api.model
    def update_cliente_custom(self, cliente_id, values):
        cliente = self.browse(int(cliente_id))

        if not cliente.exists():
            raise ValidationError("El cliente no existe.")

        cliente.write({
            "name": values.get("name", cliente.name),
            "tipo_cliente": values.get("tipo_cliente", cliente.tipo_cliente),
            "cedula": values.get("cedula", cliente.cedula) or False,
            "email": values.get("email", cliente.email) or False,
            "telefono": values.get("telefono", cliente.telefono) or False,
            "activo": values.get("activo", cliente.activo),
        })

        return cliente._cliente_to_dict()

    @api.model
    def toggle_cliente_activo_custom(self, cliente_id):
        cliente = self.browse(int(cliente_id))

        if not cliente.exists():
            raise ValidationError("El cliente no existe.")

        cliente.write({
            "activo": not cliente.activo
        })

        return {
            "id": cliente.id,
            "activo": cliente.activo,
        }
/** @odoo-module **/

import { Component, useState, onWillUpdateProps } from "@odoo/owl";
import { TechStoreTheme } from "../../../core/theme";

import { TsInput } from "../../../components/input/input";
import { TsButton } from "../../../components/button/button";

export class ClienteForm extends Component {
    setup() {
        this.theme = TechStoreTheme;

        this.state = useState({
            form: {
                name: "",
                tipo_cliente: "particular",
                cedula: "",
                email: "",
                telefono: "",
                activo: true,
            },
            error: "",
        });

        onWillUpdateProps((nextProps) => {
            this.setForm(nextProps.cliente);
        });

        this.setForm(this.props.cliente);
    }

    setForm(cliente) {
        if (cliente) {
            this.state.form.name = cliente.name || "";
            this.state.form.tipo_cliente = cliente.tipo_cliente || "particular";
            this.state.form.cedula = cliente.cedula || "";
            this.state.form.email = cliente.email || "";
            this.state.form.telefono = cliente.telefono || "";
            this.state.form.activo = cliente.activo;
        } else {
            this.clearForm();
        }
    }

    clearForm() {
        this.state.form.name = "";
        this.state.form.tipo_cliente = "particular";
        this.state.form.cedula = "";
        this.state.form.email = "";
        this.state.form.telefono = "";
        this.state.form.activo = true;
        this.state.error = "";
    }

    updateField(field, value) {
        this.state.form[field] = value;
    }

    validate() {
        const name = String(this.state.form.name || "").trim();
        const tipoCliente = this.state.form.tipo_cliente;
        const cedula = String(this.state.form.cedula || "").trim();
        const email = String(this.state.form.email || "").trim();

        if (!name || name.length < 3) {
            throw new Error("El nombre debe tener al menos 3 caracteres.");
        }

        if (!["particular", "corporativo"].includes(tipoCliente)) {
            throw new Error("Seleccione el tipo de cliente.");
        }

        if (cedula) {
            if (!/^\d+$/.test(cedula)) {
                throw new Error("La cédula/RUC solo debe contener números.");
            }

            if (tipoCliente === "particular" && cedula.length !== 10) {
                throw new Error("Para cliente particular, la cédula debe tener 10 dígitos.");
            }

            if (tipoCliente === "corporativo" && cedula.length !== 13) {
                throw new Error("Para cliente corporativo, el RUC debe tener 13 dígitos.");
            }
        }

        if (email) {
            const emailRegex = /^[\w.-]+@[\w.-]+\.\w+$/;

            if (!emailRegex.test(email)) {
                throw new Error("Ingrese un correo electrónico válido.");
            }
        }
    }

    async saveCliente() {
        try {
            this.state.error = "";

            this.validate();

            await this.props.onSave({
                name: this.state.form.name,
                tipo_cliente: this.state.form.tipo_cliente,
                cedula: this.state.form.cedula,
                email: this.state.form.email,
                telefono: this.state.form.telefono,
                activo: this.state.form.activo,
            });

            this.clearForm();

        } catch (error) {
            this.state.error = error.message || "No se pudo guardar el cliente.";
        }
    }

    cancelEdit() {
        this.clearForm();
        this.props.onCancel();
    }

    get isEditing() {
        return Boolean(this.props.cliente);
    }

    get buttonLabel() {
        return this.isEditing ? "Actualizar Cliente" : "Guardar Cliente";
    }

    get cedulaLabel() {
        return this.state.form.tipo_cliente === "corporativo"
            ? "RUC"
            : "Cédula";
    }

    get cedulaPlaceholder() {
        return this.state.form.tipo_cliente === "corporativo"
            ? "Ej. 1890000000001"
            : "Ej. 1800000000";
    }
}

ClienteForm.template = "techstore.ClienteForm";

ClienteForm.components = {
    TsInput,
    TsButton,
};
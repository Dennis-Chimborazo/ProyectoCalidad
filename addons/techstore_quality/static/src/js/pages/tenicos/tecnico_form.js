/** @odoo-module **/

import { Component, useState, onWillUpdateProps } from "@odoo/owl";
import { TechStoreTheme } from "../../../core/theme";

import { TsInput } from "../../../components/input/input";
import { TsButton } from "../../../components/button/button";

export class TecnicoForm extends Component {
    setup() {
        this.theme = TechStoreTheme;

        this.state = useState({
            form: {
                name: "",
                cedula: "",
                email: "",
                telefono: "",
                especialidad: "mantenimiento_general",
                nivel_experiencia: "junior",
                activo: true,
            },
            error: "",
        });

        onWillUpdateProps((nextProps) => {
            this.setForm(nextProps.tecnico);
        });

        this.setForm(this.props.tecnico);
    }

    setForm(tecnico) {
        if (tecnico) {
            this.state.form.name = tecnico.name || "";
            this.state.form.cedula = tecnico.cedula || "";
            this.state.form.email = tecnico.email || "";
            this.state.form.telefono = tecnico.telefono || "";
            this.state.form.especialidad = tecnico.especialidad || "mantenimiento_general";
            this.state.form.nivel_experiencia = tecnico.nivel_experiencia || "junior";
            this.state.form.activo = tecnico.activo;
        } else {
            this.clearForm();
        }
    }

    clearForm() {
        this.state.form.name = "";
        this.state.form.cedula = "";
        this.state.form.email = "";
        this.state.form.telefono = "";
        this.state.form.especialidad = "mantenimiento_general";
        this.state.form.nivel_experiencia = "junior";
        this.state.form.activo = true;
        this.state.error = "";
    }

    updateField(field, value) {
        this.state.form[field] = value;
    }

    async saveTecnico() {
        this.state.error = "";

        if (!this.state.form.name || this.state.form.name.trim().length < 3) {
            this.state.error = "El nombre debe tener al menos 3 caracteres.";
            return;
        }

        if (!this.state.form.cedula || this.state.form.cedula.trim().length !== 10) {
            this.state.error = "La cédula debe tener 10 dígitos.";
            return;
        }

        if (!this.state.form.email || !this.state.form.email.includes("@")) {
            this.state.error = "Ingrese un correo electrónico válido.";
            return;
        }

        await this.props.onSave({
            name: this.state.form.name,
            cedula: this.state.form.cedula,
            email: this.state.form.email,
            telefono: this.state.form.telefono,
            especialidad: this.state.form.especialidad,
            nivel_experiencia: this.state.form.nivel_experiencia,
            activo: this.state.form.activo,
        });

        this.clearForm();
    }

    cancelEdit() {
        this.clearForm();
        this.props.onCancel();
    }

    get isEditing() {
        return Boolean(this.props.tecnico);
    }

    get buttonLabel() {
        return this.isEditing ? "Actualizar Técnico" : "Guardar Técnico";
    }
}

TecnicoForm.template = "techstore.TecnicoForm";

TecnicoForm.components = {
    TsInput,
    TsButton,
};
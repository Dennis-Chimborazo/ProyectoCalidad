/** @odoo-module **/

import { Component, useState, onWillUpdateProps } from "@odoo/owl";
import { TechStoreTheme } from "../../../core/theme";

import { TsInput } from "../../../components/input/input";
import { TsButton } from "../../../components/button/button";

export class TipoEquipoForm extends Component {
    setup() {
        this.theme = TechStoreTheme;

        this.state = useState({
            form: {
                name: "",
                descripcion: "",
                activo: true,
            },
            error: "",
        });

        onWillUpdateProps((nextProps) => {
            this.setForm(nextProps.tipoEquipo);
        });

        this.setForm(this.props.tipoEquipo);
    }

    setForm(tipoEquipo) {
        if (tipoEquipo) {
            this.state.form.name = tipoEquipo.name || "";
            this.state.form.descripcion = tipoEquipo.descripcion || "";
            this.state.form.activo = tipoEquipo.activo;
        } else {
            this.clearForm();
        }
    }

    clearForm() {
        this.state.form.name = "";
        this.state.form.descripcion = "";
        this.state.form.activo = true;
        this.state.error = "";
    }

    updateField(field, value) {
        this.state.form[field] = value;
    }

    async saveTipoEquipo() {
        this.state.error = "";

        if (!this.state.form.name || this.state.form.name.trim().length < 3) {
            this.state.error = "El tipo de equipo debe tener al menos 3 caracteres.";
            return;
        }

        await this.props.onSave({
            name: this.state.form.name,
            descripcion: this.state.form.descripcion,
            activo: this.state.form.activo,
        });

        this.clearForm();
    }

    cancelEdit() {
        this.clearForm();
        this.props.onCancel();
    }

    get isEditing() {
        return Boolean(this.props.tipoEquipo);
    }

    get buttonLabel() {
        return this.isEditing ? "Actualizar Tipo" : "Guardar Tipo";
    }
}

TipoEquipoForm.template = "techstore.TipoEquipoForm";

TipoEquipoForm.components = {
    TsInput,
    TsButton,
};
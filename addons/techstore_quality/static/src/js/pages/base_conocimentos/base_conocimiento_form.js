/** @odoo-module **/

import { Component, useState, onWillUpdateProps } from "@odoo/owl";
import { TechStoreTheme } from "../../../core/theme";

import { TsInput } from "../../../components/input/input";
import { TsButton } from "../../../components/button/button";

export class BaseConocimientoForm extends Component {
    setup() {
        this.theme = TechStoreTheme;

        this.state = useState({
            form: {
                error_title: "",
                equipment_type_id: "",
                symptoms: "",
                root_cause: "",
                solution: "",
                keywords: "",
                activo: true,
            },
            error: "",
        });

        onWillUpdateProps((nextProps) => {
            this.setForm(nextProps.registro);
        });

        this.setForm(this.props.registro);
    }

    setForm(registro) {
        if (registro) {
            this.state.form.error_title = registro.error_title || "";
            this.state.form.equipment_type_id = registro.equipment_type_id || "";
            this.state.form.symptoms = registro.symptoms || "";
            this.state.form.root_cause = registro.root_cause || "";
            this.state.form.solution = registro.solution || "";
            this.state.form.keywords = registro.keywords || "";
            this.state.form.activo = registro.activo;
        } else {
            this.clearForm();
        }
    }

    clearForm() {
        this.state.form.error_title = "";
        this.state.form.equipment_type_id = "";
        this.state.form.symptoms = "";
        this.state.form.root_cause = "";
        this.state.form.solution = "";
        this.state.form.keywords = "";
        this.state.form.activo = true;
        this.state.error = "";
    }

    updateField(field, value) {
        this.state.form[field] = value;
    }

    async saveBaseConocimiento() {
        this.state.error = "";

        if (!this.state.form.error_title || this.state.form.error_title.trim().length < 5) {
            this.state.error = "El título de la falla debe tener al menos 5 caracteres.";
            return;
        }

        if (!this.state.form.equipment_type_id) {
            this.state.error = "Seleccione un tipo de equipo.";
            return;
        }

        if (!this.state.form.symptoms || this.state.form.symptoms.trim().length < 10) {
            this.state.error = "Los síntomas deben tener al menos 10 caracteres.";
            return;
        }

        if (!this.state.form.root_cause || this.state.form.root_cause.trim().length < 10) {
            this.state.error = "La causa raíz debe tener al menos 10 caracteres.";
            return;
        }

        if (!this.state.form.solution || this.state.form.solution.trim().length < 10) {
            this.state.error = "La solución debe tener al menos 10 caracteres.";
            return;
        }

        await this.props.onSave({
            error_title: this.state.form.error_title,
            equipment_type_id: this.state.form.equipment_type_id,
            symptoms: this.state.form.symptoms,
            root_cause: this.state.form.root_cause,
            solution: this.state.form.solution,
            keywords: this.state.form.keywords,
            activo: this.state.form.activo,
        });

        this.clearForm();
    }

    cancelEdit() {
        this.clearForm();
        this.props.onCancel();
    }

    get isEditing() {
        return Boolean(this.props.registro);
    }

    get buttonLabel() {
        return this.isEditing ? "Actualizar Registro" : "Guardar Registro";
    }
}

BaseConocimientoForm.template = "techstore.BaseConocimientoForm";

BaseConocimientoForm.components = {
    TsInput,
    TsButton,
};
/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TechStoreTheme } from "../../../core/theme";

import { TsButton } from "../../../components/button/button";

export class MantenimientoForm extends Component {
    setup() {
        this.theme = TechStoreTheme;

        this.state = useState({
            form: {
                cliente_id: "",
                tecnico_id: "",
                prioridad: "media",
                descripcion_general: "",
            },

            clienteSearch: "",
            tecnicoSearch: "",

            selectedCliente: null,
            selectedTecnico: null,

            error: "",
        });
    }

    updateField(field, value) {
        this.state.form[field] = value;
    }

    updateClienteSearch(value) {
        this.state.clienteSearch = value;
    }

    updateTecnicoSearch(value) {
        this.state.tecnicoSearch = value;
    }

    selectCliente(cliente) {
        this.state.selectedCliente = cliente;
        this.state.form.cliente_id = cliente.id;
        this.state.clienteSearch = cliente.name || "";
    }

    selectTecnico(tecnico) {
        this.state.selectedTecnico = tecnico;
        this.state.form.tecnico_id = tecnico.id;
        this.state.tecnicoSearch = tecnico.name || "";
    }

    clearCliente() {
        this.state.selectedCliente = null;
        this.state.form.cliente_id = "";
        this.state.clienteSearch = "";
    }

    clearTecnico() {
        this.state.selectedTecnico = null;
        this.state.form.tecnico_id = "";
        this.state.tecnicoSearch = "";
    }

    get filteredClientes() {
        const term = this.state.clienteSearch.trim().toLowerCase();

        if (!term) {
            return [];
        }

        return (this.props.clientes || [])
            .filter((cliente) => {
                const name = (cliente.name || "").toLowerCase();
                const cedula = (cliente.cedula || "").toLowerCase();
                const email = (cliente.email || "").toLowerCase();

                return (
                    cliente.activo !== false &&
                    (
                        name.includes(term) ||
                        cedula.includes(term) ||
                        email.includes(term)
                    )
                );
            })
            .slice(0, 6);
    }

    get filteredTecnicos() {
        const term = this.state.tecnicoSearch.trim().toLowerCase();

        if (!term) {
            return [];
        }

        return (this.props.tecnicos || [])
            .filter((tecnico) => {
                const name = (tecnico.name || "").toLowerCase();
                const cedula = (tecnico.cedula || "").toLowerCase();
                const email = (tecnico.email || "").toLowerCase();
                const especialidad = (tecnico.especialidad || "").toLowerCase();

                return (
                    tecnico.activo !== false &&
                    (
                        name.includes(term) ||
                        cedula.includes(term) ||
                        email.includes(term) ||
                        especialidad.includes(term)
                    )
                );
            })
            .slice(0, 6);
    }

    get especialidadTecnicoLabel() {
        const values = {
            hardware: "Hardware",
            software: "Software",
            mantenimiento_general: "Mantenimiento general",
        };

        if (!this.state.selectedTecnico) {
            return "";
        }

        return values[this.state.selectedTecnico.especialidad] || this.state.selectedTecnico.especialidad;
    }

    get nivelTecnicoLabel() {
        const values = {
            junior: "Junior",
            intermedio: "Intermedio",
            senior: "Senior",
        };

        if (!this.state.selectedTecnico) {
            return "";
        }

        return values[this.state.selectedTecnico.nivel_experiencia] || this.state.selectedTecnico.nivel_experiencia;
    }

    clearForm() {
        this.state.form.cliente_id = "";
        this.state.form.tecnico_id = "";
        this.state.form.prioridad = "media";
        this.state.form.descripcion_general = "";

        this.state.clienteSearch = "";
        this.state.tecnicoSearch = "";

        this.state.selectedCliente = null;
        this.state.selectedTecnico = null;

        this.state.error = "";
    }

    async saveMantenimiento() {
        this.state.error = "";

        if (!this.state.form.cliente_id) {
            this.state.error = "Busque y seleccione un cliente.";
            return;
        }

        if (!this.state.form.tecnico_id) {
            this.state.error = "Busque y seleccione un técnico.";
            return;
        }

        if (
            !this.state.form.descripcion_general ||
            this.state.form.descripcion_general.trim().length < 10
        ) {
            this.state.error = "La descripción general debe tener al menos 10 caracteres.";
            return;
        }

        await this.props.onSave({
            cliente_id: this.state.form.cliente_id,
            tecnico_id: this.state.form.tecnico_id,
            prioridad: this.state.form.prioridad,
            descripcion_general: this.state.form.descripcion_general,
        });

        this.clearForm();
    }

    cancel() {
        this.clearForm();
        this.props.onCancel();
    }
}

MantenimientoForm.template = "techstore.MantenimientoForm";

MantenimientoForm.components = {
    TsButton,
};
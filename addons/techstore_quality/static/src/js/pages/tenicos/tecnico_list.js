/** @odoo-module **/

import { Component } from "@odoo/owl";
import { TechStoreTheme } from "../../../core/theme";

import { TsCard } from "../../../components/card/card";
import { TsTable } from "../../../components/table/table";

export class TecnicoList extends Component {
    setup() {
        this.theme = TechStoreTheme;
    }

    get columns() {
        return [
            {
                key: "name",
                label: "Técnico",
            },
            {
                key: "cedula",
                label: "Cédula",
            },
            {
                key: "email",
                label: "Correo",
            },
            {
                key: "telefono",
                label: "Teléfono",
            },
            {
                key: "especialidad",
                label: "Especialidad",
                type: "selection_badge",
                options: {
                    hardware: "Hardware",
                    software: "Software",
                    mantenimiento_general: "Mantenimiento general",
                },
            },
            {
                key: "nivel_experiencia",
                label: "Experiencia",
                type: "selection_badge",
                options: {
                    junior: "Junior",
                    intermedio: "Intermedio",
                    senior: "Senior",
                },
            },
            {
                key: "mantenimientos_asignados",
                label: "Mantenimientos",
            },
            {
                key: "activo",
                label: "Estado",
                type: "boolean_badge",
                trueLabel: "Activo",
                falseLabel: "Suspendido",
            },
        ];
    }

    get actions() {
        return [
            {
                key: "edit",
                label: "Editar",
                variant: "secondary",
                onClick: (tecnico) => this.props.onEdit(tecnico),
            },
            {
                key: "toggle",
                label: (tecnico) => tecnico.activo ? "Suspender" : "Reactivar",
                variant: (tecnico) => tecnico.activo ? "danger" : "primary",
                onClick: (tecnico) => this.props.onToggle(tecnico),
            },
        ];
    }
}

TecnicoList.template = "techstore.TecnicoList";

TecnicoList.components = {
    TsCard,
    TsTable,
};
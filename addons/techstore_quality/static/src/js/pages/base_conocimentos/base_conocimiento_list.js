/** @odoo-module **/

import { Component } from "@odoo/owl";
import { TechStoreTheme } from "../../../core/theme";

import { TsCard } from "../../../components/card/card";
import { TsTable } from "../../../components/table/table";

export class BaseConocimientoList extends Component {
    setup() {
        this.theme = TechStoreTheme;
    }

    get columns() {
        return [
            {
                key: "error_title",
                label: "Falla",
            },
            {
                key: "equipment_type",
                label: "Tipo de equipo",
            },
            {
                key: "symptoms",
                label: "Síntomas",
            },
            {
                key: "root_cause",
                label: "Causa raíz",
            },
            {
                key: "solution",
                label: "Solución",
            },
            {
                key: "keywords",
                label: "Palabras clave",
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
                onClick: (registro) => this.props.onEdit(registro),
            },
            {
                key: "toggle",
                label: (registro) => registro.activo ? "Suspender" : "Reactivar",
                variant: (registro) => registro.activo ? "danger" : "primary",
                onClick: (registro) => this.props.onToggle(registro),
            },
        ];
    }
}

BaseConocimientoList.template = "techstore.BaseConocimientoList";

BaseConocimientoList.components = {
    TsCard,
    TsTable,
};
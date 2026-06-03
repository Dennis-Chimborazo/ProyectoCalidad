/** @odoo-module **/

import { Component } from "@odoo/owl";
import { TechStoreTheme } from "../../../core/theme";

import { TsCard } from "../../../components/card/card";
import { TsTable } from "../../../components/table/table";

export class TipoEquipoList extends Component {
    setup() {
        this.theme = TechStoreTheme;
    }

    get columns() {
        return [
            {
                key: "name",
                label: "Tipo de equipo",
            },
            {
                key: "descripcion",
                label: "Descripción",
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
                onClick: (tipoEquipo) => this.props.onEdit(tipoEquipo),
            },
            {
                key: "toggle",
                label: (tipoEquipo) => tipoEquipo.activo ? "Suspender" : "Reactivar",
                variant: (tipoEquipo) => tipoEquipo.activo ? "danger" : "primary",
                onClick: (tipoEquipo) => this.props.onToggle(tipoEquipo),
            },
        ];
    }
}

TipoEquipoList.template = "techstore.TipoEquipoList";

TipoEquipoList.components = {
    TsCard,
    TsTable,
};
/** @odoo-module **/

import { Component } from "@odoo/owl";
import { TechStoreTheme } from "../../../core/theme";

import { TsCard } from "../../../components/card/card";
import { TsTable } from "../../../components/table/table";

export class ClienteList extends Component {
    setup() {
        this.theme = TechStoreTheme;
    }

    get columns() {
        return [
            {
                key: "name",
                label: "Cliente",
            },
            {
                key: "tipo_cliente",
                label: "Tipo",
                type: "selection_badge",
                options: {
                    particular: "Particular",
                    corporativo: "Corporativo",
                },
            },
            {
                key: "cedula",
                label: "Cédula/RUC",
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
                onClick: (cliente) => this.props.onEdit(cliente),
            },
            {
                key: "toggle",
                label: (cliente) => cliente.activo ? "Suspender" : "Reactivar",
                variant: (cliente) => cliente.activo ? "danger" : "primary",
                onClick: (cliente) => this.props.onToggle(cliente),
            },
        ];
    }
}

ClienteList.template = "techstore.ClienteList";

ClienteList.components = {
    TsCard,
    TsTable,
};
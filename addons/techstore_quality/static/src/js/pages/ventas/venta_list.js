/** @odoo-module **/

import { Component } from "@odoo/owl";
import { TechStoreTheme } from "../../../core/theme";

import { TsTable } from "../../../components/table/table";

export class VentaList extends Component {
    setup() {
        this.theme = TechStoreTheme;
    }

    get columns() {
        return [
            {
                key: "name",
                label: "Referencia",
            },
            {
                key: "cliente_name",
                label: "Cliente",
            },
            {
                key: "cliente_cedula",
                label: "Cédula/RUC",
            },
            {
                key: "cantidad_productos",
                label: "Ítems",
            },
            {
                key: "subtotal",
                label: "Subtotal",
                type: "money",
            },
            {
                key: "descuento",
                label: "Descuento",
                type: "money",
            },
            {
                key: "total",
                label: "Total",
                type: "money",
            },
        ];
    }

    get actions() {
        return [
            {
                key: "view",
                label: "Ver",
                variant: "primary",
                onClick: (venta) => this.props.onView(venta),
            },
            {
                key: "edit",
                label: "Editar",
                variant: "secondary",
                onClick: (venta) => this.props.onEdit(venta),
            }
        ];
    }
}

VentaList.template = "techstore.VentaList";

VentaList.components = {
    TsTable,
};
/** @odoo-module **/

import { Component } from "@odoo/owl";
import { TechStoreTheme } from "../../../core/theme";

import { TsTable } from "../../../components/table/table";

export class ProductoList extends Component {
    setup() {
        this.theme = TechStoreTheme;
    }

    get columns() {
        return [
            {
                key: "name",
                label: "Producto",
            },
            {
                key: "codigo",
                label: "Código",
            },
            {
                key: "precio_unitario",
                label: "Precio",
                type: "money",
            },
            {
                key: "stock_disponible",
                label: "Stock",
            },
            {
                key: "activo",
                label: "Estado",
                type: "boolean_badge",
                trueLabel: "Activo",
                falseLabel: "Inactivo",
            },
        ];
    }

    get actions() {
        return [
            {
                key: "edit",
                label: "Editar",
                variant: "secondary",
                onClick: (producto) => this.props.onEdit(producto),
            },
            {
                key: "toggle",
                label: (producto) => producto.activo ? "Desactivar" : "Reactivar",
                variant: (producto) => producto.activo ? "danger" : "primary",
                onClick: (producto) => this.props.onToggle(producto),
            },
        ];
    }
}

ProductoList.template = "techstore.ProductoList";

ProductoList.components = {
    TsTable,
};
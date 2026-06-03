/** @odoo-module **/

import { Component } from "@odoo/owl";
import { TechStoreTheme } from "../../../core/theme";

export class VentaInfo extends Component {
    setup() {
        this.theme = TechStoreTheme;
    }

    formatMoney(value) {
        return "$ " + Number(value || 0).toFixed(2);
    }

    get venta() {
        return this.props.venta || {};
    }

    get detalles() {
        return this.venta.detalles || [];
    }

    get fechaVenta() {
        if (!this.venta.create_date) {
            return "Sin fecha";
        }

        return String(this.venta.create_date).replace("T", " ").slice(0, 19);
    }

    get estadoLabel() {
        const estado = this.venta.estado_calidad || "pendiente";

        if (estado === "aceptable") {
            return "Aceptable";
        }

        if (estado === "observado") {
            return "Observado";
        }

        return "Pendiente";
    }
}

VentaInfo.template = "techstore.VentaInfo";
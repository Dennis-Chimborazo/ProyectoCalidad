/** @odoo-module **/

import { Component } from "@odoo/owl";
import { TsButton } from "../../../components/button/button";

export class MantenimientoDetailInfo extends Component {
    static template = "techstore.MantenimientoDetailInfo";

    static components = {
        TsButton,
    };

    static props = {
        item: { type: Object },
        fallas: { type: Array },
        onClose: { type: Function },
    };

    get detalles() {
        return this.props.item.detalles || [];
    }

    get fallas() {
        return this.props.fallas || [];
    }

    estadoLabel(value) {
        const labels = {
            pendiente: "Pendiente",
            en_proceso: "En proceso",
            finalizado: "Finalizado",
            cancelado: "Cancelado",
        };

        return labels[value] || value || "Sin estado";
    }

    estadoBadgeClass(value) {
        const classes = {
            pendiente: "ts-badge ts-badge-warning",
            en_proceso: "ts-badge ts-badge-info",
            finalizado: "ts-badge ts-badge-success",
            cancelado: "ts-badge ts-badge-danger",
        };

        return classes[value] || "ts-badge";
    }

    close() {
        this.props.onClose();
    }
}
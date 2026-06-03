/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TsCustomPill extends Component {
    get normalizedValue() {
        return (this.props.value || "").toString().toLowerCase();
    }

    get pillText() {
        const labels = {
            // Estados mantenimiento
            pendiente: "Pendiente",
            en_proceso: "En proceso",
            finalizado: "Finalizado",
            cancelado: "Cancelado",

            // Prioridades
            baja: "Baja",
            media: "Media",
            alta: "Alta",
            critica: "Crítica",

            // Activo / Inactivo
            activo: "Activo",
            inactivo: "Inactivo",
            true: "Activo",
            false: "Inactivo",
        };

        return labels[this.normalizedValue] || this.props.label || this.props.value || "Sin estado";
    }

    get pillClass() {
        const value = this.normalizedValue;

        const baseClass = "ts-custom-pill";

        const classMap = {
            // Estados
            pendiente: "ts-pill-pendiente",
            en_proceso: "ts-pill-en-proceso",
            finalizado: "ts-pill-finalizado",
            cancelado: "ts-pill-cancelado",

            // Prioridad
            baja: "ts-pill-baja",
            media: "ts-pill-media",
            alta: "ts-pill-alta",
            critica: "ts-pill-critica",

            // Activo / Inactivo
            activo: "ts-pill-activo",
            inactivo: "ts-pill-inactivo",
            true: "ts-pill-activo",
            false: "ts-pill-inactivo",
        };

        return `${baseClass} ${classMap[value] || "ts-pill-default"}`;
    }
}

TsCustomPill.template = "techstore.TsCustomPill";
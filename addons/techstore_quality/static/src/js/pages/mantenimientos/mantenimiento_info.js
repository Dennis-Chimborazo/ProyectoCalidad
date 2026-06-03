/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

import { TechStoreTheme } from "../../../core/theme";
import { TsButton } from "../../../components/button/button";

export class MantenimientoInfo extends Component {
    static template = "techstore.MantenimientoInfo";

    static components = {
        TsButton,
    };

    static props = {
        mantenimiento: { type: Object },
        onClose: { type: Function },
    };

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.theme = TechStoreTheme;

        this.state = useState({
            loading: true,
            error: "",
            mantenimiento: null,
        });

        onWillStart(async () => {
            await this.loadInfo();
        });
    }

    async loadInfo() {
        this.state.loading = true;
        this.state.error = "";

        try {
            this.state.mantenimiento = await this.orm.call(
                "techstore.mantenimiento",
                "get_mantenimiento_info_custom",
                [this.props.mantenimiento.id]
            );
        } catch (error) {
            console.error("Error cargando información del mantenimiento:", error);

            this.state.error = "No se pudo cargar la información completa del mantenimiento.";

            this.notification.add(this.state.error, {
                type: "danger",
            });
        } finally {
            this.state.loading = false;
        }
    }

    get mantenimiento() {
        return this.state.mantenimiento || this.props.mantenimiento || {};
    }

    get equipos() {
        return this.mantenimiento.equipos || [];
    }

    get estadoLabel() {
        const estados = {
            pendiente: "Pendiente",
            en_proceso: "En proceso",
            finalizado: "Finalizado",
            cancelado: "Cancelado",
        };

        return estados[this.mantenimiento.estado] || this.mantenimiento.estado || "";
    }

    get prioridadLabel() {
        const prioridades = {
            baja: "Baja",
            media: "Media",
            alta: "Alta",
            critica: "Crítica",
        };

        return prioridades[this.mantenimiento.prioridad] || this.mantenimiento.prioridad || "";
    }

    estadoEquipoLabel(estado) {
        const estados = {
            pendiente: "Pendiente",
            en_proceso: "En proceso",
            finalizado: "Finalizado",
            cancelado: "Cancelado",
        };

        return estados[estado] || estado || "Sin estado";
    }

    estadoEquipoBadgeClass(estado) {
        const classes = {
            pendiente: "ts-badge ts-badge-warning",
            en_proceso: "ts-badge ts-badge-info",
            finalizado: "ts-badge ts-badge-success",
            cancelado: "ts-badge ts-badge-danger",
        };

        return classes[estado] || "ts-badge";
    }

    get resumenTexto() {
        const mantenimiento = this.mantenimiento;

        if (!mantenimiento.total_equipos) {
            return "Este mantenimiento no tiene equipos registrados.";
        }

        return `Se procesaron ${mantenimiento.total_equipos} equipo(s): ${mantenimiento.total_finalizados || 0} finalizado(s), ${mantenimiento.total_cancelados || 0} cancelado(s), ${mantenimiento.total_en_proceso || 0} en proceso y ${mantenimiento.total_pendientes || 0} pendiente(s).`;
    }

    formatDate(value) {
        if (!value) {
            return "Sin registrar";
        }

        try {
            return new Date(value).toLocaleString();
        } catch {
            return value;
        }
    }

    close() {
        this.props.onClose();
    }
}
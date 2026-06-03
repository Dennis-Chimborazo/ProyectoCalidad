/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

import { TsPageHeader } from "../../../components/page_header/page_header";
import { TsButton } from "../../../components/button/button";
import { TsSelect } from "../../../components/select/select";
import { TechStoreTheme } from "../../../core/theme";

class DashboardMantenimientosApp extends Component {
    static template = "techstore.DashboardMantenimientosApp";

    static components = {
        TsPageHeader,
        TsButton,
        TsSelect,
    };

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.theme = TechStoreTheme;

        this.state = useState({
            loading: true,
            error: "",

            mantenimientos: [],
            equipos: [],

            clientes: [],
            tiposEquipo: [],

            filters: {
                cliente_id: "",
                tipo_cliente: "",
                tipo_equipo_id: "",
                estado_mantenimiento: "",
                estado_equipo: "",
                prioridad: "",
            },
        });

        onWillStart(async () => {
            await this.loadDashboard();
        });
    }

    async loadDashboard() {
        this.state.loading = true;
        this.state.error = "";

        try {
            const data = await this.orm.call(
                "techstore.mantenimiento",
                "get_dashboard_mantenimientos_data",
                []
            );

            this.state.mantenimientos = data.mantenimientos || [];
            this.state.equipos = data.equipos || [];
            this.state.clientes = data.clientes || [];
            this.state.tiposEquipo = data.tipos_equipo || [];

        } catch (error) {
            console.error("Error cargando dashboard de mantenimientos:", error);

            this.state.error = "No se pudo cargar el dashboard de mantenimientos.";

            this.notification.add(this.state.error, {
                type: "danger",
            });
        } finally {
            this.state.loading = false;
        }
    }

    updateFilter(field, value) {
        this.state.filters[field] = value;
    }

    clearFilters() {
        this.state.filters.cliente_id = "";
        this.state.filters.tipo_cliente = "";
        this.state.filters.tipo_equipo_id = "";
        this.state.filters.estado_mantenimiento = "";
        this.state.filters.estado_equipo = "";
        this.state.filters.prioridad = "";
    }

    get tipoClienteOptions() {
        return [
            {
                id: "particular",
                label: "Particular",
            },
            {
                id: "corporativo",
                label: "Corporativo",
            },
        ];
    }

    get estadoMantenimientoOptions() {
        return [
            {
                id: "pendiente",
                label: "Pendiente",
            },
            {
                id: "en_proceso",
                label: "En proceso",
            },
            {
                id: "finalizado",
                label: "Finalizado",
            },
            {
                id: "cancelado",
                label: "Cancelado",
            },
        ];
    }

    get estadoEquipoOptions() {
        return [
            {
                id: "pendiente",
                label: "Pendiente",
            },
            {
                id: "en_proceso",
                label: "En proceso",
            },
            {
                id: "finalizado",
                label: "Finalizado",
            },
            {
                id: "cancelado",
                label: "Cancelado",
            },
        ];
    }

    get prioridadOptions() {
        return [
            {
                id: "baja",
                label: "Baja",
            },
            {
                id: "media",
                label: "Media",
            },
            {
                id: "alta",
                label: "Alta",
            },
            {
                id: "critica",
                label: "Crítica",
            },
        ];
    }

    get filteredEquipos() {
        const filters = this.state.filters;

        return this.state.equipos.filter((item) => {
            const clienteOk =
                !filters.cliente_id ||
                String(item.cliente_id) === String(filters.cliente_id);

            const tipoClienteOk =
                !filters.tipo_cliente ||
                item.tipo_cliente === filters.tipo_cliente;

            const tipoEquipoOk =
                !filters.tipo_equipo_id ||
                String(item.tipo_equipo_id) === String(filters.tipo_equipo_id);

            const estadoMantenimientoOk =
                !filters.estado_mantenimiento ||
                item.estado_mantenimiento === filters.estado_mantenimiento;

            const estadoEquipoOk =
                !filters.estado_equipo ||
                item.estado_equipo === filters.estado_equipo;

            const prioridadOk =
                !filters.prioridad ||
                item.prioridad === filters.prioridad;

            return (
                clienteOk &&
                tipoClienteOk &&
                tipoEquipoOk &&
                estadoMantenimientoOk &&
                estadoEquipoOk &&
                prioridadOk
            );
        });
    }

    get filteredMantenimientos() {
        const mantenimientoIds = new Set(
            this.filteredEquipos.map((item) => item.mantenimiento_id)
        );

        if (
            !this.state.filters.cliente_id &&
            !this.state.filters.tipo_cliente &&
            !this.state.filters.tipo_equipo_id &&
            !this.state.filters.estado_mantenimiento &&
            !this.state.filters.estado_equipo &&
            !this.state.filters.prioridad
        ) {
            return this.state.mantenimientos;
        }

        return this.state.mantenimientos.filter((item) => {
            return mantenimientoIds.has(item.id);
        });
    }

    countBy(items, field, value) {
        return items.filter((item) => item[field] === value).length;
    }

    get totalMantenimientos() {
        return this.filteredMantenimientos.length;
    }

    get totalEquipos() {
        return this.filteredEquipos.length;
    }

    get totalFinalizados() {
        return this.countBy(this.filteredEquipos, "estado_equipo", "finalizado");
    }

    get totalCancelados() {
        return this.countBy(this.filteredEquipos, "estado_equipo", "cancelado");
    }

    get totalEnProceso() {
        return this.countBy(this.filteredEquipos, "estado_equipo", "en_proceso");
    }

    get totalPendientes() {
        return this.countBy(this.filteredEquipos, "estado_equipo", "pendiente");
    }

    get totalConSolucion() {
        return this.filteredEquipos.filter((item) => item.tiene_solucion).length;
    }

    get totalConBase() {
        return this.filteredEquipos.filter((item) => item.tiene_base_conocimiento).length;
    }

    get totalCorporativos() {
        return this.filteredMantenimientos.filter((item) => item.tipo_cliente === "corporativo").length;
    }

    get totalParticulares() {
        return this.filteredMantenimientos.filter((item) => item.tipo_cliente === "particular").length;
    }

    percent(value, total = null) {
        const base = total === null ? this.totalEquipos : total;

        if (!base) {
            return 0;
        }

        return Math.round((value / base) * 100);
    }

    get estadoEquipoChart() {
        return [
            {
                key: "finalizado",
                label: "Finalizados",
                value: this.totalFinalizados,
                className: "ts-bar-success",
            },
            {
                key: "cancelado",
                label: "Cancelados",
                value: this.totalCancelados,
                className: "ts-bar-danger",
            },
            {
                key: "en_proceso",
                label: "En proceso",
                value: this.totalEnProceso,
                className: "ts-bar-info",
            },
            {
                key: "pendiente",
                label: "Pendientes",
                value: this.totalPendientes,
                className: "ts-bar-warning",
            },
        ];
    }

    get prioridadChart() {
        const data = [
            {
                key: "critica",
                label: "Crítica",
                value: this.countBy(this.filteredMantenimientos, "prioridad", "critica"),
                className: "ts-bar-danger",
            },
            {
                key: "alta",
                label: "Alta",
                value: this.countBy(this.filteredMantenimientos, "prioridad", "alta"),
                className: "ts-bar-warning",
            },
            {
                key: "media",
                label: "Media",
                value: this.countBy(this.filteredMantenimientos, "prioridad", "media"),
                className: "ts-bar-info",
            },
            {
                key: "baja",
                label: "Baja",
                value: this.countBy(this.filteredMantenimientos, "prioridad", "baja"),
                className: "ts-bar-success",
            },
        ];

        return data;
    }

    get tipoClienteChart() {
        return [
            {
                key: "particular",
                label: "Particulares",
                value: this.totalParticulares,
                className: "ts-bar-info",
            },
            {
                key: "corporativo",
                label: "Corporativos",
                value: this.totalCorporativos,
                className: "ts-bar-primary",
            },
        ];
    }

    get tipoEquipoChart() {
        const map = {};

        this.filteredEquipos.forEach((item) => {
            const label = item.tipo_equipo || "Sin tipo";

            if (!map[label]) {
                map[label] = 0;
            }

            map[label] += 1;
        });

        return Object.keys(map)
            .map((label) => {
                return {
                    key: label,
                    label,
                    value: map[label],
                    className: "ts-bar-primary",
                };
            })
            .sort((a, b) => b.value - a.value)
            .slice(0, 8);
    }

    get solucionChart() {
        const conSolucion = this.totalConSolucion;
        const sinSolucion = Math.max(this.totalEquipos - conSolucion, 0);

        return [
            {
                key: "con_solucion",
                label: "Con solución",
                value: conSolucion,
                className: "ts-bar-success",
            },
            {
                key: "sin_solucion",
                label: "Sin solución",
                value: sinSolucion,
                className: "ts-bar-warning",
            },
        ];
    }

    get mantenimientoEstadoChart() {
        return [
            {
                key: "finalizado",
                label: "Finalizados",
                value: this.countBy(this.filteredMantenimientos, "estado", "finalizado"),
                className: "ts-bar-success",
            },
            {
                key: "cancelado",
                label: "Cancelados",
                value: this.countBy(this.filteredMantenimientos, "estado", "cancelado"),
                className: "ts-bar-danger",
            },
            {
                key: "en_proceso",
                label: "En proceso",
                value: this.countBy(this.filteredMantenimientos, "estado", "en_proceso"),
                className: "ts-bar-info",
            },
            {
                key: "pendiente",
                label: "Pendientes",
                value: this.countBy(this.filteredMantenimientos, "estado", "pendiente"),
                className: "ts-bar-warning",
            },
        ];
    }

    get recentEquipos() {
        return this.filteredEquipos.slice(0, 8);
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

    prioridadLabel(value) {
        const labels = {
            baja: "Baja",
            media: "Media",
            alta: "Alta",
            critica: "Crítica",
        };

        return labels[value] || value || "Sin prioridad";
    }

    badgeClassEstado(value) {
        const classes = {
            pendiente: "ts-db-badge ts-db-badge-warning",
            en_proceso: "ts-db-badge ts-db-badge-info",
            finalizado: "ts-db-badge ts-db-badge-success",
            cancelado: "ts-db-badge ts-db-badge-danger",
        };

        return classes[value] || "ts-db-badge";
    }

    get estadoEquipoDonutStyle() {
    const total = this.totalEquipos || 1;

    const finalizados = (this.totalFinalizados / total) * 100;
    const cancelados = finalizados + (this.totalCancelados / total) * 100;
    const enProceso = cancelados + (this.totalEnProceso / total) * 100;

    return `
        background: conic-gradient(
            #16a34a 0% ${finalizados}%,
            #dc2626 ${finalizados}% ${cancelados}%,
            #0891b2 ${cancelados}% ${enProceso}%,
            #f59e0b ${enProceso}% 100%
        );
    `;
}

get solucionGaugeStyle() {
    const value = this.percent(this.totalConSolucion);

    return `
        background: conic-gradient(
            #16a34a 0% ${value}%,
            #e2e8f0 ${value}% 100%
        );
    `;
}

get ordenesStackedStyle() {
    const total = this.totalMantenimientos || 1;

    const finalizados = this.countBy(this.filteredMantenimientos, "estado", "finalizado");
    const cancelados = this.countBy(this.filteredMantenimientos, "estado", "cancelado");
    const enProceso = this.countBy(this.filteredMantenimientos, "estado", "en_proceso");
    const pendientes = this.countBy(this.filteredMantenimientos, "estado", "pendiente");

    const pFinalizados = (finalizados / total) * 100;
    const pCancelados = pFinalizados + (cancelados / total) * 100;
    const pEnProceso = pCancelados + (enProceso / total) * 100;

    return `
        background: linear-gradient(
            90deg,
            #16a34a 0% ${pFinalizados}%,
            #dc2626 ${pFinalizados}% ${pCancelados}%,
            #0891b2 ${pCancelados}% ${pEnProceso}%,
            #f59e0b ${pEnProceso}% 100%
        );
    `;
}

get maxTipoEquipoValue() {
    const values = this.tipoEquipoChart.map((item) => item.value);

    if (!values.length) {
        return 1;
    }

    return Math.max(...values);
}

chartHeight(value, total = null) {
    const base = total || this.totalMantenimientos || 1;
    const percent = Math.round((value / base) * 100);

    return Math.max(percent, value > 0 ? 8 : 2);
}

chartWidth(value, total = null) {
    const base = total || this.maxTipoEquipoValue || 1;
    const percent = Math.round((value / base) * 100);

    return Math.max(percent, value > 0 ? 10 : 2);
}

get mantenimientoEstadoResumen() {
    return [
        {
            key: "finalizado",
            label: "Finalizados",
            value: this.countBy(this.filteredMantenimientos, "estado", "finalizado"),
            className: "ts-dot-success",
        },
        {
            key: "cancelado",
            label: "Cancelados",
            value: this.countBy(this.filteredMantenimientos, "estado", "cancelado"),
            className: "ts-dot-danger",
        },
        {
            key: "en_proceso",
            label: "En proceso",
            value: this.countBy(this.filteredMantenimientos, "estado", "en_proceso"),
            className: "ts-dot-info",
        },
        {
            key: "pendiente",
            label: "Pendientes",
            value: this.countBy(this.filteredMantenimientos, "estado", "pendiente"),
            className: "ts-dot-warning",
        },
    ];
}
}

registry.category("actions").add(
    "techstore_dashboard_mantenimientos_app_action",
    DashboardMantenimientosApp
);
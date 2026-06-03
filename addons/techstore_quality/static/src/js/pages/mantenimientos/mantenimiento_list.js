/** @odoo-module **/

import { Component } from "@odoo/owl";
import { TechStoreTheme } from "../../../core/theme";
import { TsTable } from "../../../components/table/table";

export class MantenimientoList extends Component {
    static template = "techstore.MantenimientoList";

    static components = {
        TsTable,
    };

    static props = {
        mantenimientos: { type: Array },
        onOpenDetail: { type: Function },
        onOpenInfo: { type: Function },
    };

    setup() {
        this.theme = TechStoreTheme;
    }

    get columns() {
        return [
            {
                key: "name",
                label: "Código",
            },
            {
                key: "cliente",
                label: "Cliente",
            },
            {
                key: "tecnico",
                label: "Técnico",
            },
            {
                key: "prioridad",
                label: "Prioridad",
                type: "selection_badge",
                options: {
                    baja: "Baja",
                    media: "Media",
                    alta: "Alta",
                    critica: "Crítica",
                },
            },
            {
                key: "estado",
                label: "Estado",
                type: "selection_badge",
                options: {
                    pendiente: "Pendiente",
                    en_proceso: "En proceso",
                    finalizado: "Finalizado",
                    cancelado: "Cancelado",
                },
            },
            {
                key: "total_equipos",
                label: "Equipos",
            },
        ];
    }

    get actions() {
        return [
            {
                key: "open_detail",
                label: (mantenimiento) => {
                    return ["pendiente", "en_proceso"].includes(mantenimiento.estado)
                        ? "Abrir detalle"
                        : "Ver información";
                },
                variant: (mantenimiento) => {
                    return ["pendiente", "en_proceso"].includes(mantenimiento.estado)
                        ? "primary"
                        : "secondary";
                },
                onClick: (mantenimiento) => {
                    if (["pendiente", "en_proceso"].includes(mantenimiento.estado)) {
                        this.props.onOpenDetail(mantenimiento);
                        return;
                    }

                    this.props.onOpenInfo(mantenimiento);
                },
            },
        ];
    }
}
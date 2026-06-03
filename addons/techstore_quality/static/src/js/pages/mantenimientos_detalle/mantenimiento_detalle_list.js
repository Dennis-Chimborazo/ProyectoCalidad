/** @odoo-module **/

import { Component } from "@odoo/owl";
import { TechStoreTheme } from "../../../core/theme";
import { TsTable } from "../../../components/table/table";

export class MantenimientoDetalleList extends Component {
    static template = "techstore.MantenimientoDetalleList";

    static components = {
        TsTable,
    };

    static props = {
        equiposMantenimiento: { type: Array },
        onOpenSolution: { type: Function },
        onOpenInfo: { type: Function },
    };

    setup() {
        this.theme = TechStoreTheme;
    }

    get rows() {
        return this.props.equiposMantenimiento || [];
    }

    get columns() {
        return [
            {
                key: "equipo",
                label: "Equipo",
            },
            {
                key: "tipo_equipo",
                label: "Tipo",
            },
            {
                key: "marca",
                label: "Marca",
            },
            {
                key: "modelo",
                label: "Modelo",
            },
            {
                key: "numero_serie",
                label: "Serie",
            },
            {
                key: "falla_reportada",
                label: "Falla reportada",
            },
            {
                key: "solucion",
                label: "Solución",
            },
            {
                key: "estado_equipo",
                label: "Estado",
                type: "selection_badge",
                options: {
                    pendiente: "Pendiente",
                    en_proceso: "En proceso",
                    finalizado: "Finalizado",
                    cancelado: "Cancelado",
                },
            },
        ];
    }

    get actions() {
        return [
            {
                key: "manage_or_info",
                label: (item) => {
                    if (["finalizado", "cancelado"].includes(item.estado_equipo)) {
                        return "Ver información";
                    }

                    return "Gestionar solución";
                },
                variant: (item) => {
                    if (["finalizado", "cancelado"].includes(item.estado_equipo)) {
                        return "secondary";
                    }

                    return "primary";
                },
                onClick: (item) => {
                    if (["finalizado", "cancelado"].includes(item.estado_equipo)) {
                        this.props.onOpenInfo(item);
                        return;
                    }

                    this.props.onOpenSolution(item);
                },
            },
        ];
    }
}
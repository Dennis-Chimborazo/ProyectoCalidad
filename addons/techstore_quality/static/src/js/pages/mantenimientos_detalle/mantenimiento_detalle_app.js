/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

import { MantenimientoDetalleForm } from "./mantenimiento_detalle_form";
import { MantenimientoDetalleList } from "./mantenimiento_detalle_list";
import { MantenimientoSolucion } from "./mantenimiento_solucion";
import { MantenimientoDetailInfo } from "./mantenimiento_detail_info";

import { TsButton } from "../../../components/button/button";
import { TsModal } from "../../../components/modal/modal";
import { TechStoreTheme } from "../../../core/theme";

export class MantenimientoDetalleApp extends Component {
    static template = "techstore.MantenimientoDetalleApp";

    static components = {
        MantenimientoDetalleForm,
        MantenimientoDetalleList,
        MantenimientoSolucion,
        MantenimientoDetailInfo,
        TsButton,
        TsModal,
    };

    static props = {
        action: { type: Object, optional: true },
        actionId: { type: Number, optional: true },
        className: { type: String, optional: true },
    };

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.action = useService("action");
        this.theme = TechStoreTheme;

        this.state = useState({
            mantenimiento: null,
            tiposEquipo: [],
            equiposMantenimiento: [],

            loading: true,
            error: "",
            search: "",

            showEquipoModal: false,

            showSolutionModal: false,
            showInfoModal: false,
            selectedEquipoMantenimiento: null,

            baseConocimiento: [],
            fallasEquipo: [],
        });

        onWillStart(async () => {
            await this.refreshAll();
        });
    }

    get mantenimientoId() {
        return this.props.action?.params?.mantenimiento_id || null;
    }

    async refreshAll() {
        if (!this.mantenimientoId) {
            this.state.error = "No existe un mantenimiento seleccionado.";
            this.state.loading = false;
            return;
        }

        this.state.loading = true;
        this.state.error = "";

        try {
            await Promise.all([
                this.loadMantenimiento(),
                this.loadTiposEquipo(),
                this.loadEquiposMantenimiento(),
            ]);
        } catch (error) {
            console.error("Error cargando detalle del mantenimiento:", error);

            this.state.error = "No se pudo cargar el detalle del mantenimiento.";

            this.notification.add(this.state.error, {
                type: "danger",
            });
        } finally {
            this.state.loading = false;
        }
    }

    async loadMantenimiento() {
        this.state.mantenimiento = await this.orm.call(
            "techstore.mantenimiento",
            "get_mantenimiento_by_id_custom",
            [this.mantenimientoId]
        );
    }

    async loadTiposEquipo() {
        this.state.tiposEquipo = await this.orm.call(
            "techstore.tipo.equipo",
            "get_tipos_equipo_data",
            []
        );
    }

    async loadEquiposMantenimiento() {
        this.state.equiposMantenimiento = await this.orm.call(
            "techstore.mantenimiento.equipo",
            "get_equipos_mantenimiento_data",
            [this.mantenimientoId]
        );
    }

    updateSearch(value) {
        this.state.search = value;
    }

    get filteredEquiposMantenimiento() {
        const term = this.state.search.trim().toLowerCase();

        if (!term) {
            return this.state.equiposMantenimiento;
        }

        return this.state.equiposMantenimiento.filter((item) => {
            const detalles = (item.detalles || [])
                .map((detalle) => {
                    return [
                        detalle.caracteristica,
                        detalle.valor,
                    ].join(" ");
                })
                .join(" ");

            const text = [
                item.equipo,
                item.tipo_equipo,
                item.marca,
                item.modelo,
                item.numero_serie,
                item.estado_equipo,
                item.falla_reportada,
                item.solucion,
                detalles,
            ].join(" ").toLowerCase();

            return text.includes(term);
        });
    }

    openEquipoModal() {
        this.state.showEquipoModal = true;
    }

    closeEquipoModal() {
        this.state.showEquipoModal = false;
    }

    async onEquipoSaved(values) {
        if (!this.mantenimientoId) {
            const message = "No existe un mantenimiento seleccionado.";
            this.notification.add(message, { type: "warning" });
            throw new Error(message);
        }

        try {
            const response = await this.orm.call(
                "techstore.mantenimiento.equipo",
                "create_or_attach_equipo_custom",
                [{
                    mantenimiento_id: this.mantenimientoId,
                    equipo: values,
                }]
            );

            this.notification.add(
                "Equipo agregado correctamente al mantenimiento.",
                { type: "success" }
            );

            if (response && response.warning) {
                this.notification.add(response.warning, {
                    type: "warning",
                });
            }

            this.closeEquipoModal();
            await this.refreshAll();

        } catch (error) {
            console.error("Error guardando equipo del mantenimiento:", error);

            const message = this.getOdooErrorMessage(error);

            this.notification.add(message, {
                type: "danger",
            });

            throw new Error(message);
        }
    }

    async openSolutionModal(item) {
        this.state.selectedEquipoMantenimiento = item;
        this.state.showSolutionModal = true;

        await Promise.all([
            this.loadBaseConocimiento(item.tipo_equipo_id),
            this.loadFallasEquipo(item.id),
        ]);
    }

    async openInfoModal(item) {
        this.state.selectedEquipoMantenimiento = item;
        this.state.showInfoModal = true;

        await this.loadFallasEquipo(item.id);
    }

    closeSolutionModal() {
        this.state.showSolutionModal = false;
        this.state.selectedEquipoMantenimiento = null;
        this.state.baseConocimiento = [];
        this.state.fallasEquipo = [];
    }

    closeInfoModal() {
        this.state.showInfoModal = false;
        this.state.selectedEquipoMantenimiento = null;
        this.state.fallasEquipo = [];
    }

    async loadBaseConocimiento(tipoEquipoId) {
        if (!tipoEquipoId) {
            this.state.baseConocimiento = [];
            return;
        }

        this.state.baseConocimiento = await this.orm.call(
            "techstore.base.conocimiento",
            "get_base_conocimiento_data",
            [tipoEquipoId]
        );
    }

    async loadFallasEquipo(mantenimientoEquipoId) {
        this.state.fallasEquipo = await this.orm.call(
            "techstore.mantenimiento.equipo.falla",
            "get_fallas_mantenimiento_equipo_data",
            [mantenimientoEquipoId]
        );
    }

    async saveSolucion(values) {
        try {
            await this.orm.call(
                "techstore.mantenimiento.equipo",
                "update_solucion_equipo_custom",
                [
                    values.mantenimiento_equipo_id,
                    {
                        solucion: values.solucion || false,
                    },
                ]
            );

            const estadoResponse = await this.orm.call(
                "techstore.mantenimiento.equipo",
                "update_estado_equipo_custom",
                [
                    values.mantenimiento_equipo_id,
                    values.estado_equipo,
                ]
            );

            const actuales = this.state.fallasEquipo || [];

            const actualesIds = actuales.map((falla) => {
                return falla.base_conocimiento_id;
            });

            const nuevosIds = values.base_conocimiento_ids || [];

            const eliminar = actuales.filter((falla) => {
                return !nuevosIds.includes(falla.base_conocimiento_id);
            });

            const agregar = nuevosIds.filter((baseId) => {
                return !actualesIds.includes(baseId);
            });

            for (const falla of eliminar) {
                await this.orm.call(
                    "techstore.mantenimiento.equipo.falla",
                    "delete_mantenimiento_equipo_falla_custom",
                    [falla.id]
                );
            }

            for (const baseId of agregar) {
                await this.orm.call(
                    "techstore.mantenimiento.equipo.falla",
                    "create_mantenimiento_equipo_falla_custom",
                    [{
                        mantenimiento_equipo_id: values.mantenimiento_equipo_id,
                        base_conocimiento_id: baseId,
                    }]
                );
            }

            this.notification.add(
                "Gestión de solución guardada correctamente.",
                { type: "success" }
            );

            if (estadoResponse && estadoResponse.mantenimiento_cerrado) {
                this.notification.add(
                    "Todos los equipos fueron cerrados. El mantenimiento se finalizó automáticamente.",
                    { type: "success" }
                );

                this.closeSolutionModal();

                await this.action.doAction({
                    type: "ir.actions.client",
                    tag: "techstore_mantenimiento_app_action",
                    name: "Mantenimientos",
                });

                return;
            }

            this.closeSolutionModal();
            await this.refreshAll();

        } catch (error) {
            console.error("Error guardando solución:", error);

            const message = this.getOdooErrorMessage(error);

            this.notification.add(message, {
                type: "danger",
            });

            throw new Error(message);
        }
    }

    async back() {
        await this.action.doAction({
            type: "ir.actions.client",
            tag: "techstore_mantenimiento_app_action",
            name: "Mantenimientos",
        });
    }

    getOdooErrorMessage(error) {
        if (error?.data?.message) {
            return error.data.message;
        }

        if (error?.data?.debug) {
            const debug = error.data.debug;

            const validationMatch = debug.match(/ValidationError:\s*(.*)/);

            if (validationMatch && validationMatch[1]) {
                return validationMatch[1].trim();
            }

            const userErrorMatch = debug.match(/UserError:\s*(.*)/);

            if (userErrorMatch && userErrorMatch[1]) {
                return userErrorMatch[1].trim();
            }
        }

        if (error?.message) {
            return error.message;
        }

        return "Ocurrió un error inesperado.";
    }

    prioridadLabel(value) {
        const labels = {
            baja: "Baja",
            media: "Media",
            alta: "Alta",
            critica: "Crítica",
        };

        return labels[value] || value || "";
    }

    prioridadBadgeClass(value) {
        const classes = {
            baja: "ts-badge ts-badge-success",
            media: "ts-badge ts-badge-info",
            alta: "ts-badge ts-badge-warning",
            critica: "ts-badge ts-badge-danger",
        };

        return classes[value] || "ts-badge";
    }

    estadoLabel(value) {
        const labels = {
            pendiente: "Pendiente",
            en_proceso: "En proceso",
            finalizado: "Finalizado",
            cancelado: "Cancelado",
        };

        return labels[value] || value || "";
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
}
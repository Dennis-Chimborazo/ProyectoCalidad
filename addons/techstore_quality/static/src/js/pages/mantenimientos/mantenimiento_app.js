/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

import { MantenimientoForm } from "./mantenimiento_form";
import { MantenimientoList } from "./mantenimiento_list";
import { MantenimientoInfo } from "./mantenimiento_info";

import { TsPageHeader } from "../../../components/page_header/page_header";
import { TsButton } from "../../../components/button/button";
import { TsModal } from "../../../components/modal/modal";
import { TsSelect } from "../../../components/select/select";
import { TechStoreTheme } from "../../../core/theme";

class MantenimientoApp extends Component {
    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.action = useService("action");
        this.theme = TechStoreTheme;

        this.state = useState({
            mantenimientos: [],
            clientes: [],
            tecnicos: [],

            loading: true,
            search: "",

            filterPrioridad: "",
            filterEstado: "",

            showCreateModal: false,
            showInfoModal: false,
            infoMantenimiento: null,
        });

        onWillStart(async () => {
            await Promise.all([
                this.loadMantenimientos(),
                this.loadClientes(),
                this.loadTecnicos(),
            ]);
        });
    }

    async loadMantenimientos() {
        this.state.loading = true;

        try {
            this.state.mantenimientos = await this.orm.call(
                "techstore.mantenimiento",
                "get_mantenimientos_data",
                []
            );
        } catch (error) {
            console.error("Error cargando mantenimientos:", error);

            this.notification.add(
                "No se pudieron cargar los mantenimientos.",
                { type: "danger" }
            );
        }

        this.state.loading = false;
    }

    async loadClientes() {
        try {
            this.state.clientes = await this.orm.call(
                "techstore.cliente",
                "get_clientes_data",
                []
            );
        } catch (error) {
            console.error("Error cargando clientes:", error);

            this.notification.add(
                "No se pudieron cargar los clientes.",
                { type: "danger" }
            );
        }
    }

    async loadTecnicos() {
        try {
            this.state.tecnicos = await this.orm.call(
                "techstore.tecnico",
                "get_tecnicos_data",
                []
            );
        } catch (error) {
            console.error("Error cargando técnicos:", error);

            this.notification.add(
                "No se pudieron cargar los técnicos.",
                { type: "danger" }
            );
        }
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

    get estadoOptions() {
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

    get filteredMantenimientos() {
        const term = this.state.search.trim().toLowerCase();
        const prioridad = this.state.filterPrioridad;
        const estado = this.state.filterEstado;

        return this.state.mantenimientos.filter((mantenimiento) => {
            const codigo = (mantenimiento.name || "").toLowerCase();
            const cliente = (mantenimiento.cliente || "").toLowerCase();
            const tecnico = (mantenimiento.tecnico || "").toLowerCase();
            const estadoValue = (mantenimiento.estado || "").toLowerCase();
            const prioridadValue = (mantenimiento.prioridad || "").toLowerCase();

            const matchesSearch =
                !term ||
                codigo.includes(term) ||
                cliente.includes(term) ||
                tecnico.includes(term) ||
                estadoValue.includes(term) ||
                prioridadValue.includes(term);

            const matchesPrioridad =
                !prioridad ||
                mantenimiento.prioridad === prioridad;

            const matchesEstado =
                !estado ||
                mantenimiento.estado === estado;

            return matchesSearch && matchesPrioridad && matchesEstado;
        });
    }

    updateSearch(value) {
        this.state.search = value;
    }

    updatePrioridadFilter(value) {
        this.state.filterPrioridad = value;
    }

    updateEstadoFilter(value) {
        this.state.filterEstado = value;
    }

    clearFilters() {
        this.state.search = "";
        this.state.filterPrioridad = "";
        this.state.filterEstado = "";
    }

    openCreateModal() {
        this.state.showCreateModal = true;
    }

    closeCreateModal() {
        this.state.showCreateModal = false;
    }

    async saveMantenimiento(values) {
        try {
            const mantenimiento = await this.orm.call(
                "techstore.mantenimiento",
                "create_mantenimiento_custom",
                [values]
            );

            this.notification.add(
                "Mantenimiento creado correctamente.",
                { type: "success" }
            );

            this.closeCreateModal();

            await this.loadMantenimientos();

            await this.openDetail(mantenimiento);

        } catch (error) {
            console.error("Error guardando mantenimiento:", error);

            this.notification.add(
                "No se pudo crear el mantenimiento. Revise los datos ingresados.",
                { type: "danger" }
            );
        }
    }

    async openDetail(mantenimiento) {
        if (!mantenimiento || !mantenimiento.id) {
            this.notification.add(
                "No existe un mantenimiento seleccionado.",
                { type: "warning" }
            );
            return;
        }

        await this.action.doAction({
            type: "ir.actions.client",
            tag: "techstore_mantenimiento_detalle_app_action",
            name: "Detalle de Mantenimiento",
            params: {
                mantenimiento_id: mantenimiento.id,
            },
        });
    }

    openInfoModal(mantenimiento) {
        this.state.infoMantenimiento = mantenimiento;
        this.state.showInfoModal = true;
    }

    closeInfoModal() {
        this.state.infoMantenimiento = null;
        this.state.showInfoModal = false;
    }
}

MantenimientoApp.template = "techstore.MantenimientoApp";

MantenimientoApp.components = {
    MantenimientoForm,
    MantenimientoList,
    MantenimientoInfo,
    TsPageHeader,
    TsButton,
    TsModal,
    TsSelect,
};

registry.category("actions").add("techstore_mantenimiento_app_action", MantenimientoApp);
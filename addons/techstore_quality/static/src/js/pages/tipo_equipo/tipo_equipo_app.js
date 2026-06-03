/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

import { TipoEquipoForm } from "./tipo_equipo_form";
import { TipoEquipoList } from "./tipo_equipo_list";

import { TsPageHeader } from "../../../components/page_header/page_header";
import { TsButton } from "../../../components/button/button";
import { TsModal } from "../../../components/modal/modal";
import { TechStoreTheme } from "../../../core/theme";

class TipoEquipoApp extends Component {
    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.theme = TechStoreTheme;

        this.state = useState({
            tiposEquipo: [],
            loading: true,
            editingTipoEquipo: null,
            showModal: false,
            search: "",
        });

        onWillStart(async () => {
            await this.loadTiposEquipo();
        });
    }

    async loadTiposEquipo() {
        this.state.loading = true;

        try {
            this.state.tiposEquipo = await this.orm.call(
                "techstore.tipo.equipo",
                "get_tipos_equipo_data",
                []
            );
        } catch (error) {
            console.error("Error cargando tipos de equipo:", error);

            this.notification.add(
                "No se pudieron cargar los tipos de equipo.",
                { type: "danger" }
            );
        }

        this.state.loading = false;
    }

    get filteredTiposEquipo() {
        const term = this.state.search.trim().toLowerCase();

        if (!term) {
            return this.state.tiposEquipo;
        }

        return this.state.tiposEquipo.filter((tipo) => {
            const nombre = (tipo.name || "").toLowerCase();
            const descripcion = (tipo.descripcion || "").toLowerCase();

            return nombre.includes(term) || descripcion.includes(term);
        });
    }

    updateSearch(value) {
        this.state.search = value;
    }

    openCreateModal() {
        this.state.editingTipoEquipo = null;
        this.state.showModal = true;
    }

    openEditModal(tipoEquipo) {
        this.state.editingTipoEquipo = {
            id: tipoEquipo.id,
            name: tipoEquipo.name,
            descripcion: tipoEquipo.descripcion,
            activo: tipoEquipo.activo,
        };

        this.state.showModal = true;
    }

    closeModal() {
        this.state.showModal = false;
        this.state.editingTipoEquipo = null;
    }

    async saveTipoEquipo(values) {
        try {
            if (this.state.editingTipoEquipo) {
                await this.orm.call(
                    "techstore.tipo.equipo",
                    "update_tipo_equipo_custom",
                    [this.state.editingTipoEquipo.id, values]
                );

                this.notification.add(
                    "Tipo de equipo actualizado correctamente.",
                    { type: "success" }
                );
            } else {
                await this.orm.call(
                    "techstore.tipo.equipo",
                    "create_tipo_equipo_custom",
                    [values]
                );

                this.notification.add(
                    "Tipo de equipo registrado correctamente.",
                    { type: "success" }
                );
            }

            this.closeModal();
            await this.loadTiposEquipo();

        } catch (error) {
            console.error("Error guardando tipo de equipo:", error);

            this.notification.add(
                "No se pudo guardar el tipo de equipo. Revise si el nombre ya existe.",
                { type: "danger" }
            );
        }
    }

    async toggleTipoEquipo(tipoEquipo) {
        try {
            await this.orm.call(
                "techstore.tipo.equipo",
                "toggle_tipo_equipo_activo_custom",
                [tipoEquipo.id]
            );

            this.notification.add(
                tipoEquipo.activo
                    ? "Tipo de equipo suspendido correctamente."
                    : "Tipo de equipo reactivado correctamente.",
                { type: "success" }
            );

            await this.loadTiposEquipo();

        } catch (error) {
            console.error("Error cambiando estado:", error);

            this.notification.add(
                "No se pudo cambiar el estado del tipo de equipo.",
                { type: "danger" }
            );
        }
    }

    get modalTitle() {
        return this.state.editingTipoEquipo
            ? "Editar Tipo de Equipo"
            : "Agregar Tipo de Equipo";
    }

    get modalSubtitle() {
        return this.state.editingTipoEquipo
            ? "Modifique los datos del tipo de equipo seleccionado."
            : "Complete el formulario para registrar un nuevo tipo de equipo.";
    }
}

TipoEquipoApp.template = "techstore.TipoEquipoApp";

TipoEquipoApp.components = {
    TipoEquipoForm,
    TipoEquipoList,
    TsPageHeader,
    TsButton,
    TsModal,
};

registry.category("actions").add("techstore_tipo_equipo_app_action", TipoEquipoApp);
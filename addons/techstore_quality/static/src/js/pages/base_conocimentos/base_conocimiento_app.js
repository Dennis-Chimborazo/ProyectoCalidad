/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

import { BaseConocimientoForm } from "./base_conocimiento_form";
import { BaseConocimientoList } from "./base_conocimiento_list";

import { TsPageHeader } from "../../../components/page_header/page_header";
import { TsButton } from "../../../components/button/button";
import { TsModal } from "../../../components/modal/modal";
import { TechStoreTheme } from "../../../core/theme";

class BaseConocimientoApp extends Component {
    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.theme = TechStoreTheme;

        this.state = useState({
            registros: [],
            tiposEquipo: [],
            loading: true,
            editingRegistro: null,
            showModal: false,
            search: "",
            equipmentTypeFilter: "",
        });

        onWillStart(async () => {
            await Promise.all([
                this.loadBaseConocimiento(),
                this.loadTiposEquipo(),
            ]);
        });
    }

    async loadBaseConocimiento() {
        this.state.loading = true;

        try {
            const equipmentTypeId = this.state.equipmentTypeFilter || null;

            this.state.registros = await this.orm.call(
                "techstore.base.conocimiento",
                "get_base_conocimiento_data",
                [equipmentTypeId]
            );
        } catch (error) {
            console.error("Error cargando base de conocimiento:", error);

            this.notification.add(
                "No se pudo cargar la base de conocimiento.",
                { type: "danger" }
            );
        }

        this.state.loading = false;
    }

    async loadTiposEquipo() {
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
    }

    get activeTiposEquipo() {
        return this.state.tiposEquipo.filter((tipo) => tipo.activo);
    }

    get filteredRegistros() {
        const term = this.state.search.trim().toLowerCase();

        if (!term) {
            return this.state.registros;
        }

        return this.state.registros.filter((registro) => {
            const titulo = (registro.error_title || "").toLowerCase();
            const tipoEquipo = (registro.equipment_type || "").toLowerCase();
            const sintomas = (registro.symptoms || "").toLowerCase();
            const causa = (registro.root_cause || "").toLowerCase();
            const solucion = (registro.solution || "").toLowerCase();
            const palabrasClave = (registro.keywords || "").toLowerCase();

            return (
                titulo.includes(term) ||
                tipoEquipo.includes(term) ||
                sintomas.includes(term) ||
                causa.includes(term) ||
                solucion.includes(term) ||
                palabrasClave.includes(term)
            );
        });
    }

    updateSearch(value) {
        this.state.search = value;
    }

    async updateEquipmentTypeFilter(value) {
        this.state.equipmentTypeFilter = value;
        await this.loadBaseConocimiento();
    }

    openCreateModal() {
        this.state.editingRegistro = null;
        this.state.showModal = true;
    }

    openEditModal(registro) {
        this.state.editingRegistro = {
            id: registro.id,
            error_title: registro.error_title,
            equipment_type_id: registro.equipment_type_id,
            symptoms: registro.symptoms,
            root_cause: registro.root_cause,
            solution: registro.solution,
            keywords: registro.keywords,
            activo: registro.activo,
        };

        this.state.showModal = true;
    }

    closeModal() {
        this.state.showModal = false;
        this.state.editingRegistro = null;
    }

    async saveBaseConocimiento(values) {
        try {
            if (this.state.editingRegistro) {
                await this.orm.call(
                    "techstore.base.conocimiento",
                    "update_base_conocimiento_custom",
                    [this.state.editingRegistro.id, values]
                );

                this.notification.add(
                    "Registro actualizado correctamente.",
                    { type: "success" }
                );
            } else {
                await this.orm.call(
                    "techstore.base.conocimiento",
                    "create_base_conocimiento_custom",
                    [values]
                );

                this.notification.add(
                    "Registro documentado correctamente.",
                    { type: "success" }
                );
            }

            this.closeModal();
            await this.loadBaseConocimiento();

        } catch (error) {
            console.error("Error guardando base de conocimiento:", error);

            this.notification.add(
                "No se pudo guardar el registro. Revise si ya existe una falla similar para ese tipo de equipo.",
                { type: "danger" }
            );
        }
    }

    async toggleBaseConocimiento(registro) {
        try {
            await this.orm.call(
                "techstore.base.conocimiento",
                "toggle_base_conocimiento_activo_custom",
                [registro.id]
            );

            this.notification.add(
                registro.activo
                    ? "Registro suspendido correctamente."
                    : "Registro reactivado correctamente.",
                { type: "success" }
            );

            await this.loadBaseConocimiento();

        } catch (error) {
            console.error("Error cambiando estado:", error);

            this.notification.add(
                "No se pudo cambiar el estado del registro.",
                { type: "danger" }
            );
        }
    }

    get modalTitle() {
        return this.state.editingRegistro
            ? "Editar Falla Documentada"
            : "Agregar Falla Documentada";
    }

    get modalSubtitle() {
        return this.state.editingRegistro
            ? "Modifique la información técnica de la falla seleccionada."
            : "Complete la información para documentar una falla frecuente.";
    }
}

BaseConocimientoApp.template = "techstore.BaseConocimientoApp";

BaseConocimientoApp.components = {
    BaseConocimientoForm,
    BaseConocimientoList,
    TsPageHeader,
    TsButton,
    TsModal,
};

registry.category("actions").add("techstore_base_conocimiento_app_action", BaseConocimientoApp);
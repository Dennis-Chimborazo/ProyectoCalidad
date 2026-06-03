/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

import { TecnicoForm } from "./tecnico_form";
import { TecnicoList } from "./tecnico_list";

import { TsPageHeader } from "../../../components/page_header/page_header";
import { TsButton } from "../../../components/button/button";
import { TsModal } from "../../../components/modal/modal";
import { TechStoreTheme } from "../../../core/theme";

class TecnicoApp extends Component {
    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.theme = TechStoreTheme;

        this.state = useState({
            tecnicos: [],
            loading: true,
            editingTecnico: null,
            showModal: false,
            search: "",
        });

        onWillStart(async () => {
            await this.loadTecnicos();
        });
    }

    async loadTecnicos() {
        this.state.loading = true;

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

        this.state.loading = false;
    }

    get filteredTecnicos() {
        const term = this.state.search.trim().toLowerCase();

        if (!term) {
            return this.state.tecnicos;
        }

        return this.state.tecnicos.filter((tecnico) => {
            const nombre = (tecnico.name || "").toLowerCase();
            const cedula = (tecnico.cedula || "").toLowerCase();
            const email = (tecnico.email || "").toLowerCase();
            const especialidad = (tecnico.especialidad || "").toLowerCase();

            return (
                nombre.includes(term) ||
                cedula.includes(term) ||
                email.includes(term) ||
                especialidad.includes(term)
            );
        });
    }

    updateSearch(value) {
        this.state.search = value;
    }

    openCreateModal() {
        this.state.editingTecnico = null;
        this.state.showModal = true;
    }

    openEditModal(tecnico) {
        this.state.editingTecnico = {
            id: tecnico.id,
            name: tecnico.name,
            cedula: tecnico.cedula,
            email: tecnico.email,
            telefono: tecnico.telefono,
            especialidad: tecnico.especialidad,
            nivel_experiencia: tecnico.nivel_experiencia,
            activo: tecnico.activo,
        };

        this.state.showModal = true;
    }

    closeModal() {
        this.state.showModal = false;
        this.state.editingTecnico = null;
    }

    async saveTecnico(values) {
        try {
            if (this.state.editingTecnico) {
                await this.orm.call(
                    "techstore.tecnico",
                    "update_tecnico_custom",
                    [this.state.editingTecnico.id, values]
                );

                this.notification.add(
                    "Técnico actualizado correctamente.",
                    { type: "success" }
                );
            } else {
                await this.orm.call(
                    "techstore.tecnico",
                    "create_tecnico_custom",
                    [values]
                );

                this.notification.add(
                    "Técnico registrado correctamente.",
                    { type: "success" }
                );
            }

            this.closeModal();
            await this.loadTecnicos();

        } catch (error) {
            console.error("Error guardando técnico:", error);

            this.notification.add(
                "No se pudo guardar el técnico. Revise si la cédula o correo ya existen.",
                { type: "danger" }
            );
        }
    }

    async toggleTecnico(tecnico) {
        try {
            await this.orm.call(
                "techstore.tecnico",
                "toggle_tecnico_activo_custom",
                [tecnico.id]
            );

            this.notification.add(
                tecnico.activo
                    ? "Técnico suspendido correctamente."
                    : "Técnico reactivado correctamente.",
                { type: "success" }
            );

            await this.loadTecnicos();

        } catch (error) {
            console.error("Error cambiando estado:", error);

            this.notification.add(
                "No se pudo cambiar el estado del técnico.",
                { type: "danger" }
            );
        }
    }

    get modalTitle() {
        return this.state.editingTecnico ? "Editar Técnico" : "Agregar Técnico";
    }

    get modalSubtitle() {
        return this.state.editingTecnico
            ? "Modifique los datos del técnico seleccionado."
            : "Complete el formulario para registrar un nuevo técnico.";
    }
}

TecnicoApp.template = "techstore.TecnicoApp";

TecnicoApp.components = {
    TecnicoForm,
    TecnicoList,
    TsPageHeader,
    TsButton,
    TsModal,
};

registry.category("actions").add("techstore_tecnico_app_action", TecnicoApp);
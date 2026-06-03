/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

import { ClienteForm } from "./cliente_form";
import { ClienteList } from "./cliente_list";

import { TsPageHeader } from "../../../components/page_header/page_header";
import { TsButton } from "../../../components/button/button";
import { TsModal } from "../../../components/modal/modal";
import { TsSelect } from "../../../components/select/select";
import { TechStoreTheme } from "../../../core/theme";

class ClienteApp extends Component {
    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.theme = TechStoreTheme;

        this.state = useState({
            clientes: [],
            loading: true,
            editingCliente: null,
            showModal: false,
            search: "",
            filterTipoCliente: "",
        });

        onWillStart(async () => {
            await this.loadClientes();
        });
    }

    async loadClientes() {
        this.state.loading = true;

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

        this.state.loading = false;
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

    get filteredClientes() {
        const term = this.state.search.trim().toLowerCase();
        const tipoCliente = this.state.filterTipoCliente;

        return this.state.clientes.filter((cliente) => {
            const nombre = (cliente.name || "").toLowerCase();
            const tipo = (cliente.tipo_cliente || "").toLowerCase();
            const tipoLabel = (cliente.tipo_cliente_label || "").toLowerCase();
            const cedula = (cliente.cedula || "").toLowerCase();
            const email = (cliente.email || "").toLowerCase();
            const telefono = (cliente.telefono || "").toLowerCase();

            const matchesSearch =
                !term ||
                nombre.includes(term) ||
                tipo.includes(term) ||
                tipoLabel.includes(term) ||
                cedula.includes(term) ||
                email.includes(term) ||
                telefono.includes(term);

            const matchesTipo =
                !tipoCliente ||
                cliente.tipo_cliente === tipoCliente;

            return matchesSearch && matchesTipo;
        });
    }

    updateSearch(value) {
        this.state.search = value;
    }

    updateTipoClienteFilter(value) {
        this.state.filterTipoCliente = value;
    }

    openCreateModal() {
        this.state.editingCliente = null;
        this.state.showModal = true;
    }

    openEditModal(cliente) {
        this.state.editingCliente = {
            id: cliente.id,
            name: cliente.name,
            tipo_cliente: cliente.tipo_cliente || "particular",
            cedula: cliente.cedula,
            email: cliente.email,
            telefono: cliente.telefono,
            activo: cliente.activo,
        };

        this.state.showModal = true;
    }

    closeModal() {
        this.state.showModal = false;
        this.state.editingCliente = null;
    }

    async saveCliente(values) {
        try {
            if (this.state.editingCliente) {
                await this.orm.call(
                    "techstore.cliente",
                    "update_cliente_custom",
                    [this.state.editingCliente.id, values]
                );

                this.notification.add(
                    "Cliente actualizado correctamente.",
                    { type: "success" }
                );
            } else {
                await this.orm.call(
                    "techstore.cliente",
                    "create_cliente_custom",
                    [values]
                );

                this.notification.add(
                    "Cliente registrado correctamente.",
                    { type: "success" }
                );
            }

            this.closeModal();
            await this.loadClientes();

        } catch (error) {
            console.error("Error guardando cliente:", error);

            this.notification.add(
                "No se pudo guardar el cliente. Revise si la cédula o correo ya existen.",
                { type: "danger" }
            );
        }
    }

    async toggleCliente(cliente) {
        try {
            await this.orm.call(
                "techstore.cliente",
                "toggle_cliente_activo_custom",
                [cliente.id]
            );

            this.notification.add(
                cliente.activo
                    ? "Cliente suspendido correctamente."
                    : "Cliente reactivado correctamente.",
                { type: "success" }
            );

            await this.loadClientes();

        } catch (error) {
            console.error("Error cambiando estado:", error);

            this.notification.add(
                "No se pudo cambiar el estado del cliente.",
                { type: "danger" }
            );
        }
    }

    get modalTitle() {
        return this.state.editingCliente ? "Editar Cliente" : "Agregar Cliente";
    }

    get modalSubtitle() {
        return this.state.editingCliente
            ? "Modifique los datos del cliente seleccionado."
            : "Complete el formulario para registrar un nuevo cliente.";
    }
}

ClienteApp.template = "techstore.ClienteApp";

ClienteApp.components = {
    ClienteForm,
    ClienteList,
    TsPageHeader,
    TsButton,
    TsModal,
    TsSelect,
};

registry.category("actions").add("techstore_cliente_app_action", ClienteApp);
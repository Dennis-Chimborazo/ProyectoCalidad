/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

import { VentaForm } from "./venta_form";
import { VentaList } from "./venta_list";
import { VentaInfo } from "./venta_info";

import { TsPageHeader } from "../../../components/page_header/page_header";
import { TsButton } from "../../../components/button/button";
import { TsModal } from "../../../components/modal/modal";
import { TechStoreTheme } from "../../../core/theme";

class VentaApp extends Component {
    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.theme = TechStoreTheme;

        this.state = useState({
            ventas: [],
            clientes: [],
            productos: [],
            loading: true,
            showModal: false,
            showInfoModal: false,
            editingVenta: null,
            selectedVenta: null,
            search: "",
        });

        onWillStart(async () => {
            await this.loadData();
        });
    }

    async loadData() {
        this.state.loading = true;

        try {
            const ventas = await this.orm.call(
                "techstore.venta",
                "get_ventas_data",
                []
            );

            const catalogos = await this.orm.call(
                "techstore.venta",
                "get_venta_catalogos",
                []
            );

            this.state.ventas = ventas || [];
            this.state.clientes = catalogos.clientes || [];
            this.state.productos = catalogos.productos || [];

        } catch (error) {
            console.error("Error cargando ventas:", error);

            this.notification.add(
                "No se pudieron cargar las ventas.",
                { type: "danger" }
            );
        }

        this.state.loading = false;
    }

    get filteredVentas() {
        const term = this.state.search.trim().toLowerCase();

        if (!term) {
            return this.state.ventas;
        }

        return this.state.ventas.filter((venta) => {
            const referencia = (venta.name || "").toLowerCase();
            const cliente = (venta.cliente_name || "").toLowerCase();
            const cedula = (venta.cliente_cedula || "").toLowerCase();
            const productos = (venta.productos_resumen || "").toLowerCase();

            return (
                referencia.includes(term) ||
                cliente.includes(term) ||
                cedula.includes(term) ||
                productos.includes(term)
            );
        });
    }

    updateSearch(value) {
        this.state.search = value;
    }

    openCreateModal() {
        this.state.editingVenta = null;
        this.state.showModal = true;
    }

    openEditModal(venta) {
        this.state.editingVenta = venta;
        this.state.showModal = true;
    }

    closeModal() {
        this.state.showModal = false;
        this.state.editingVenta = null;
    }

    openInfoModal(venta) {
        this.state.selectedVenta = venta;
        this.state.showInfoModal = true;
    }

    closeInfoModal() {
        this.state.selectedVenta = null;
        this.state.showInfoModal = false;
    }

    async saveVenta(values) {
        try {
            if (this.state.editingVenta) {
                await this.orm.call(
                    "techstore.venta",
                    "update_venta_custom",
                    [this.state.editingVenta.id, values]
                );

                this.notification.add(
                    "Factura actualizada correctamente.",
                    { type: "success" }
                );
            } else {
                await this.orm.call(
                    "techstore.venta",
                    "create_venta_custom",
                    [values]
                );

                this.notification.add(
                    "Venta generada correctamente.",
                    { type: "success" }
                );
            }

            this.closeModal();
            await this.loadData();

            return true;

        } catch (error) {
            console.error("Error guardando venta:", error);

            this.notification.add(
                "No se pudo guardar la venta. Revise cliente, productos, stock, cantidades y descuento.",
                { type: "danger" }
            );

            return false;
        }
    }

    async deleteVenta(venta) {
        const confirmar = window.confirm(
            `¿Desea eliminar la venta ${venta.name}? El stock será restaurado.`
        );

        if (!confirmar) {
            return;
        }

        try {
            await this.orm.call(
                "techstore.venta",
                "delete_venta_custom",
                [venta.id]
            );

            this.notification.add(
                "Venta eliminada y stock restaurado correctamente.",
                { type: "success" }
            );

            await this.loadData();

        } catch (error) {
            console.error("Error eliminando venta:", error);

            this.notification.add(
                "No se pudo eliminar la venta.",
                { type: "danger" }
            );
        }
    }

    get modalTitle() {
        return this.state.editingVenta ? "Editar Factura" : "Generar Venta";
    }

    get modalSubtitle() {
        return this.state.editingVenta
            ? "Modifique cliente, productos, cantidades y descuento de la factura."
            : "Busque el cliente, agregue productos al detalle y confirme la venta.";
    }

    get infoModalTitle() {
        return this.state.selectedVenta
            ? `Detalle de venta`
            : "Detalle de venta";
    }

    get infoModalSubtitle() {
        return "Visualización completa de la factura generada.";
    }
}

VentaApp.template = "techstore.VentaApp";

VentaApp.components = {
    VentaForm,
    VentaList,
    VentaInfo,
    TsPageHeader,
    TsButton,
    TsModal,
};

registry.category("actions").add("techstore_venta_app_action", VentaApp);
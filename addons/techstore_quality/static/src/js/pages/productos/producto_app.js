/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

import { ProductoForm } from "./producto_form";
import { ProductoList } from "./producto_list";

import { TsPageHeader } from "../../../components/page_header/page_header";
import { TsButton } from "../../../components/button/button";
import { TsModal } from "../../../components/modal/modal";
import { TechStoreTheme } from "../../../core/theme";

class ProductoApp extends Component {
    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.theme = TechStoreTheme;

        this.state = useState({
            productos: [],
            loading: true,
            editingProducto: null,
            showModal: false,
            search: "",
        });

        onWillStart(async () => {
            await this.loadProductos();
        });
    }

    async loadProductos() {
        this.state.loading = true;

        try {
            this.state.productos = await this.orm.call(
                "techstore.producto",
                "get_productos_data",
                []
            );
        } catch (error) {
            console.error("Error cargando productos:", error);

            this.notification.add(
                "No se pudieron cargar los productos.",
                { type: "danger" }
            );
        }

        this.state.loading = false;
    }

    get filteredProductos() {
        const term = this.state.search.trim().toLowerCase();

        if (!term) {
            return this.state.productos;
        }

        return this.state.productos.filter((producto) => {
            const nombre = (producto.name || "").toLowerCase();
            const codigo = (producto.codigo || "").toLowerCase();

            return nombre.includes(term) || codigo.includes(term);
        });
    }

    updateSearch(value) {
        this.state.search = value;
    }

    openCreateModal() {
        this.state.editingProducto = null;
        this.state.showModal = true;
    }

    openEditModal(producto) {
        this.state.editingProducto = {
            id: producto.id,
            name: producto.name,
            codigo: producto.codigo,
            precio_unitario: producto.precio_unitario,
            stock_disponible: producto.stock_disponible,
            activo: producto.activo,
        };

        this.state.showModal = true;
    }

    closeModal() {
        this.state.showModal = false;
        this.state.editingProducto = null;
    }

    async saveProducto(values) {
        try {
            if (this.state.editingProducto) {
                await this.orm.call(
                    "techstore.producto",
                    "update_producto_custom",
                    [this.state.editingProducto.id, values]
                );

                this.notification.add(
                    "Producto actualizado correctamente.",
                    { type: "success" }
                );
            } else {
                await this.orm.call(
                    "techstore.producto",
                    "create_producto_custom",
                    [values]
                );

                this.notification.add(
                    "Producto registrado correctamente.",
                    { type: "success" }
                );
            }

            this.closeModal();
            await this.loadProductos();

        } catch (error) {
            console.error("Error guardando producto:", error);

            this.notification.add(
                "No se pudo guardar el producto. Revise código, nombre, precio y stock.",
                { type: "danger" }
            );
        }
    }

    async toggleProducto(producto) {
        try {
            await this.orm.call(
                "techstore.producto",
                "toggle_producto_activo_custom",
                [producto.id]
            );

            this.notification.add(
                producto.activo
                    ? "Producto desactivado correctamente."
                    : "Producto reactivado correctamente.",
                { type: "success" }
            );

            await this.loadProductos();

        } catch (error) {
            console.error("Error cambiando estado:", error);

            this.notification.add(
                "No se pudo cambiar el estado del producto.",
                { type: "danger" }
            );
        }
    }

    get modalTitle() {
        return this.state.editingProducto ? "Editar Producto" : "Agregar Producto";
    }

    get modalSubtitle() {
        return this.state.editingProducto
            ? "Modifique los datos del producto seleccionado."
            : "Complete el formulario para registrar un nuevo producto.";
    }
}

ProductoApp.template = "techstore.ProductoApp";

ProductoApp.components = {
    ProductoForm,
    ProductoList,
    TsPageHeader,
    TsButton,
    TsModal,
};

registry.category("actions").add("techstore_producto_app_action", ProductoApp);

console.log("✅ techstore_producto_app_action registrado correctamente");
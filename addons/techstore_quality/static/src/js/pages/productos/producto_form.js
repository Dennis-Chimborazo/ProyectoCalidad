/** @odoo-module **/

import { Component, useState, onWillUpdateProps } from "@odoo/owl";
import { TechStoreTheme } from "../../../core/theme";

import { TsInput } from "../../../components/input/input";
import { TsButton } from "../../../components/button/button";

export class ProductoForm extends Component {
    setup() {
        this.theme = TechStoreTheme;

        this.state = useState({
            form: {
                name: "",
                codigo: "",
                precio_unitario: "",
                stock_disponible: 10,
                activo: true,
            },
            error: "",
        });

        onWillUpdateProps((nextProps) => {
            this.setForm(nextProps.producto);
        });

        this.setForm(this.props.producto);
    }

    setForm(producto) {
        if (producto) {
            this.state.form.name = producto.name || "";
            this.state.form.codigo = producto.codigo || "";
            this.state.form.precio_unitario = producto.precio_unitario || "";
            this.state.form.stock_disponible = producto.stock_disponible || 0;
            this.state.form.activo = producto.activo;
        } else {
            this.clearForm();
        }
    }

    clearForm() {
        this.state.form.name = "";
        this.state.form.codigo = "";
        this.state.form.precio_unitario = "";
        this.state.form.stock_disponible = 10;
        this.state.form.activo = true;
        this.state.error = "";
    }

    updateField(field, value) {
        this.state.form[field] = value;
    }

    async saveProducto() {
        this.state.error = "";

        const name = String(this.state.form.name || "").trim();
        const codigo = String(this.state.form.codigo || "").trim().toUpperCase();
        const precio = Number(this.state.form.precio_unitario);
        const stock = Number(this.state.form.stock_disponible);

        if (!name || name.length < 3) {
            this.state.error = "El nombre debe tener al menos 3 caracteres.";
            return;
        }

        if (!codigo || codigo.length < 3) {
            this.state.error = "El código debe tener al menos 3 caracteres.";
            return;
        }

        if (!/^[A-Z0-9-]+$/.test(codigo)) {
            this.state.error = "El código solo puede contener letras, números y guiones.";
            return;
        }

        if (!precio || precio <= 0) {
            this.state.error = "El precio unitario debe ser mayor a 0.";
            return;
        }

        if (!Number.isInteger(stock) || stock < 0) {
            this.state.error = "El stock debe ser un número entero mayor o igual a 0.";
            return;
        }

        await this.props.onSave({
            name: name,
            codigo: codigo,
            precio_unitario: precio,
            stock_disponible: stock,
            activo: Boolean(this.state.form.activo),
        });
    }

    cancelEdit() {
        this.clearForm();
        this.props.onCancel();
    }

    get isEditing() {
        return Boolean(this.props.producto);
    }

    get buttonLabel() {
        return this.isEditing ? "Actualizar Producto" : "Guardar Producto";
    }
}

ProductoForm.template = "techstore.ProductoForm";

ProductoForm.components = {
    TsInput,
    TsButton,
};
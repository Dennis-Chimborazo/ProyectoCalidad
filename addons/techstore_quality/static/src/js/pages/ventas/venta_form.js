/** @odoo-module **/

import { Component, useState, onWillUpdateProps } from "@odoo/owl";
import { TechStoreTheme } from "../../../core/theme";

import { TsButton } from "../../../components/button/button";

export class VentaForm extends Component {
    setup() {
        this.theme = TechStoreTheme;

        this.state = useState({
            clienteSearch: "",
            productoSearch: "",
            clienteSeleccionado: null,
            productoSeleccionado: null,
            cantidadProducto: 1,
            descuento: 0,
            observacion: "",
            detalles: [],
            error: "",
        });

        onWillUpdateProps((nextProps) => {
            this.setVenta(nextProps.venta);
        });

        this.setVenta(this.props.venta);
    }

    setVenta(venta) {
        if (!venta) {
            this.limpiarFormulario();
            return;
        }

        const cliente = (this.props.clientes || []).find((item) => {
            return Number(item.id) === Number(venta.cliente_id);
        }) || {
            id: venta.cliente_id,
            label: venta.cliente_name,
            cedula: venta.cliente_cedula,
        };

        this.state.clienteSeleccionado = cliente;
        this.state.clienteSearch = `${cliente.label} - ${cliente.cedula || "Sin cédula"}`;
        this.state.productoSearch = "";
        this.state.productoSeleccionado = null;
        this.state.cantidadProducto = 1;
        this.state.descuento = Number(venta.descuento || 0);
        this.state.observacion = venta.observacion || "";

        this.state.detalles = (venta.detalles || []).map((detalle) => {
            return {
                producto_id: Number(detalle.producto_id),
                producto_name: detalle.producto_name,
                producto_codigo: detalle.producto_codigo,
                cantidad: Number(detalle.cantidad || 0),
                precio_unitario: Number(detalle.precio_unitario || 0),
                stock_disponible: Number(detalle.stock_actual || 0) + Number(detalle.cantidad || 0),
                subtotal: Number(detalle.cantidad || 0) * Number(detalle.precio_unitario || 0),
            };
        });

        this.state.error = "";
    }

    formatMoney(value) {
        return "$ " + Number(value || 0).toFixed(2);
    }

    updateClienteSearch(value) {
        this.state.clienteSearch = value;
    }

    updateProductoSearch(value) {
        this.state.productoSearch = value;
    }

    updateCantidad(value) {
        this.state.cantidadProducto = value;
    }

    updateDescuento(value) {
        this.state.descuento = value;
    }

    updateObservacion(value) {
        this.state.observacion = value;
    }

    get clientesFiltrados() {
        const term = this.state.clienteSearch.trim().toLowerCase();

        if (!term) {
            return [];
        }

        return (this.props.clientes || [])
            .filter((cliente) => {
                const nombre = (cliente.label || "").toLowerCase();
                const cedula = (cliente.cedula || "").toLowerCase();

                return nombre.includes(term) || cedula.includes(term);
            })
            .slice(0, 8);
    }

    seleccionarCliente(cliente) {
        this.state.clienteSeleccionado = cliente;
        this.state.clienteSearch = `${cliente.label} - ${cliente.cedula || "Sin cédula"}`;
        this.state.error = "";
    }

    limpiarCliente() {
        this.state.clienteSeleccionado = null;
        this.state.clienteSearch = "";
    }

    get productosFiltrados() {
        const term = this.state.productoSearch.trim().toLowerCase();

        if (!term) {
            return [];
        }

        return (this.props.productos || [])
            .filter((producto) => {
                const nombre = (producto.label || "").toLowerCase();
                const codigo = (producto.codigo || "").toLowerCase();

                return nombre.includes(term) || codigo.includes(term);
            })
            .slice(0, 8);
    }

    seleccionarProducto(producto) {
        this.state.productoSeleccionado = producto;
        this.state.productoSearch = `${producto.label} | ${producto.codigo}`;
        this.state.error = "";
    }

    limpiarProducto() {
        this.state.productoSeleccionado = null;
        this.state.productoSearch = "";
        this.state.cantidadProducto = 1;
    }

    agregarDetalle() {
        this.state.error = "";

        const producto = this.state.productoSeleccionado;
        const cantidad = Number(this.state.cantidadProducto || 0);

        if (!producto) {
            this.state.error = "Debe seleccionar un producto.";
            return;
        }

        if (!Number.isInteger(cantidad) || cantidad <= 0) {
            this.state.error = "La cantidad debe ser un número entero mayor a 0.";
            return;
        }

        if (cantidad > Number(producto.stock_disponible || 0)) {
            this.state.error = `Stock insuficiente. Disponible: ${producto.stock_disponible}.`;
            return;
        }

        const detalleExistente = this.state.detalles.find((item) => {
            return Number(item.producto_id) === Number(producto.id);
        });

        if (detalleExistente) {
            const nuevaCantidad = Number(detalleExistente.cantidad) + cantidad;

            if (nuevaCantidad > Number(detalleExistente.stock_disponible || 0)) {
                this.state.error = `No puede superar el stock disponible de ${detalleExistente.stock_disponible}.`;
                return;
            }

            detalleExistente.cantidad = nuevaCantidad;
            detalleExistente.subtotal = nuevaCantidad * Number(detalleExistente.precio_unitario || 0);

        } else {
            this.state.detalles.push({
                producto_id: Number(producto.id),
                producto_name: producto.label,
                producto_codigo: producto.codigo,
                cantidad: cantidad,
                precio_unitario: Number(producto.precio_unitario || 0),
                stock_disponible: Number(producto.stock_disponible || 0),
                subtotal: cantidad * Number(producto.precio_unitario || 0),
            });
        }

        this.limpiarProducto();
    }

    quitarDetalle(productoId) {
        this.state.detalles = this.state.detalles.filter((item) => {
            return Number(item.producto_id) !== Number(productoId);
        });
    }

    aumentarCantidad(productoId) {
        const detalle = this.state.detalles.find((item) => {
            return Number(item.producto_id) === Number(productoId);
        });

        if (!detalle) {
            return;
        }

        if (detalle.cantidad + 1 > detalle.stock_disponible) {
            this.state.error = `No puede superar el stock disponible de ${detalle.stock_disponible}.`;
            return;
        }

        detalle.cantidad += 1;
        detalle.subtotal = detalle.cantidad * detalle.precio_unitario;
        this.state.error = "";
    }

    disminuirCantidad(productoId) {
        const detalle = this.state.detalles.find((item) => {
            return Number(item.producto_id) === Number(productoId);
        });

        if (!detalle) {
            return;
        }

        if (detalle.cantidad <= 1) {
            this.quitarDetalle(productoId);
            return;
        }

        detalle.cantidad -= 1;
        detalle.subtotal = detalle.cantidad * detalle.precio_unitario;
        this.state.error = "";
    }

    get subtotalBruto() {
        return this.state.detalles.reduce((total, item) => {
            return total + Number(item.subtotal || 0);
        }, 0);
    }

    get descuento() {
        return Number(this.state.descuento || 0);
    }

    get subtotalFinal() {
        const value = this.subtotalBruto - this.descuento;
        return value > 0 ? value : 0;
    }

    get iva() {
        return this.subtotalFinal * 0.15;
    }

    get total() {
        return this.subtotalFinal + this.iva;
    }

    get buttonLabel() {
        return this.props.venta ? "Actualizar Factura" : "Generar Venta";
    }

    validarVenta() {
        if (!this.state.clienteSeleccionado) {
            return "Debe seleccionar un cliente.";
        }

        if (!this.state.detalles.length) {
            return "Debe agregar al menos un producto al detalle.";
        }

        if (this.descuento < 0) {
            return "El descuento no puede ser negativo.";
        }

        if (this.descuento > this.subtotalBruto) {
            return "El descuento no puede ser mayor al subtotal.";
        }

        for (const detalle of this.state.detalles) {
            if (!detalle.producto_id) {
                return "Existe un detalle sin producto.";
            }

            if (!Number.isInteger(Number(detalle.cantidad)) || Number(detalle.cantidad) <= 0) {
                return `La cantidad de ${detalle.producto_name} no es válida.`;
            }

            if (Number(detalle.cantidad) > Number(detalle.stock_disponible)) {
                return `La cantidad de ${detalle.producto_name} supera el stock disponible.`;
            }

            if (Number(detalle.precio_unitario) <= 0) {
                return `El precio de ${detalle.producto_name} no es válido.`;
            }
        }

        return "";
    }

    async guardarVenta() {
        this.state.error = "";

        const error = this.validarVenta();

        if (error) {
            this.state.error = error;
            return;
        }

        const guardado = await this.props.onSave({
            cliente_id: Number(this.state.clienteSeleccionado.id),
            descuento: this.descuento,
            observacion: this.state.observacion || "",
            detalles: this.state.detalles.map((detalle) => {
                return {
                    producto_id: Number(detalle.producto_id),
                    cantidad: Number(detalle.cantidad),
                };
            }),
        });

        if (guardado === false) {
            this.state.error = "No se pudo guardar la venta. Revise los datos ingresados.";
            return;
        }

        this.limpiarFormulario();
    }

    limpiarFormulario() {
        this.state.clienteSearch = "";
        this.state.productoSearch = "";
        this.state.clienteSeleccionado = null;
        this.state.productoSeleccionado = null;
        this.state.cantidadProducto = 1;
        this.state.descuento = 0;
        this.state.observacion = "";
        this.state.detalles = [];
        this.state.error = "";
    }

    cancelar() {
        this.limpiarFormulario();
        this.props.onCancel();
    }
}

VentaForm.template = "techstore.VentaForm";

VentaForm.components = {
    TsButton,
};
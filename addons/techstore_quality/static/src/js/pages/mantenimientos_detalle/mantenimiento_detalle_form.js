/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TsButton } from "../../../components/button/button";

export class MantenimientoDetalleForm extends Component {
    static template = "techstore.MantenimientoDetalleForm";

    static components = {
        TsButton,
    };

    static props = {
        mantenimientoId: { type: Number },
        tiposEquipo: { type: Array },
        equiposMantenimiento: { type: Array, optional: true },
        onSaved: { type: Function },
        onCancel: { type: Function },
    };

    setup() {
        this.state = useState({
            error: "",
            warning: "",

            formEquipo: {
                name: "",
                tipo_equipo_id: "",
                marca: "",
                modelo: "",
                numero_serie: "",
                color: "",
                descripcion: "",
                falla_reportada: "",
                solucion: "",
            },

            formDetalle: {
                name: "",
                valor: "",
            },

            detalles: [],
        });
    }

    get tiposEquipoActivos() {
        return (this.props.tiposEquipo || []).filter((tipo) => {
            return tipo.activo !== false;
        });
    }

    get serialesAsignados() {
        const seriales = new Set();

        (this.props.equiposMantenimiento || []).forEach((item) => {
            if (item.numero_serie) {
                seriales.add(item.numero_serie.trim().toUpperCase());
            }
        });

        return seriales;
    }

    updateEquipoField(field, value) {
        this.state.formEquipo[field] = value;

        if (field === "numero_serie") {
            this.validarSerie(value);
        }
    }

    updateDetalleField(field, value) {
        this.state.formDetalle[field] = value;
    }

    validarSerie(value) {
        const serial = String(value || "").trim().toUpperCase();

        this.state.warning = "";

        if (!serial) {
            return;
        }

        if (this.serialesAsignados.has(serial)) {
            this.state.warning = "Este equipo ya está agregado a este mantenimiento.";
        }
    }

    agregarDetalle() {
        this.state.error = "";

        const name = String(this.state.formDetalle.name || "").trim();
        const valor = String(this.state.formDetalle.valor || "").trim();

        if (!name || name.length < 2) {
            this.state.error = "La característica debe tener al menos 2 caracteres.";
            return;
        }

        if (!valor) {
            this.state.error = "El valor de la característica no puede estar vacío.";
            return;
        }

        const existe = this.state.detalles.some((detalle) => {
            return (
                detalle.name.toLowerCase() === name.toLowerCase() &&
                detalle.valor.toLowerCase() === valor.toLowerCase()
            );
        });

        if (existe) {
            this.state.error = "Esta característica ya fue agregada.";
            return;
        }

        this.state.detalles.push({
            local_id: Date.now() + Math.random(),
            name,
            valor,
        });

        this.state.formDetalle.name = "";
        this.state.formDetalle.valor = "";
    }

    quitarDetalle(localId) {
        this.state.detalles = this.state.detalles.filter((detalle) => {
            return detalle.local_id !== localId;
        });
    }

    validate() {
        const name = String(this.state.formEquipo.name || "").trim();
        const tipoEquipoId = this.state.formEquipo.tipo_equipo_id;
        const numeroSerie = String(this.state.formEquipo.numero_serie || "").trim().toUpperCase();
        const fallaReportada = String(this.state.formEquipo.falla_reportada || "").trim();

        if (!name || name.length < 3) {
            throw new Error("Ingrese el nombre del equipo.");
        }

        if (!tipoEquipoId) {
            throw new Error("Seleccione el tipo de equipo.");
        }

        if (!numeroSerie || numeroSerie.length < 3) {
            throw new Error("El número de serie debe tener al menos 3 caracteres.");
        }

        if (this.serialesAsignados.has(numeroSerie)) {
            throw new Error("Este equipo ya está agregado a este mantenimiento.");
        }

        if (!fallaReportada || fallaReportada.length < 5) {
            throw new Error("Ingrese la falla reportada del equipo.");
        }

        if (!this.state.detalles.length) {
            throw new Error("Agregue al menos una característica del equipo.");
        }
    }

    async guardar() {
    try {
        this.state.error = "";

        this.validate();

        const numeroSerie = String(
            this.state.formEquipo.numero_serie || ""
        ).trim().toUpperCase();

        await this.props.onSaved({
            name: String(this.state.formEquipo.name || "").trim(),
            tipo_equipo_id: Number(this.state.formEquipo.tipo_equipo_id),
            marca: this.state.formEquipo.marca || false,
            modelo: this.state.formEquipo.modelo || false,
            numero_serie: numeroSerie,
            color: this.state.formEquipo.color || false,
            descripcion: this.state.formEquipo.descripcion || false,
            falla_reportada: this.state.formEquipo.falla_reportada || false,
            solucion: this.state.formEquipo.solucion || false,
            detalles: this.state.detalles.map((detalle) => {
                return {
                    name: detalle.name,
                    valor: detalle.valor,
                };
            }),
        });

    } catch (error) {
        console.error(error);

        this.state.error = error.message || "No se pudo guardar el equipo.";
    }
}

    cancelar() {
        this.props.onCancel();
    }
}
/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TsButton } from "../../../components/button/button";

export class MantenimientoSolucion extends Component {
    static template = "techstore.MantenimientoSolucion";

    static components = {
        TsButton,
    };

    static props = {
        item: { type: Object },
        baseConocimiento: { type: Array },
        fallasSeleccionadas: { type: Array },
        onSave: { type: Function },
        onCancel: { type: Function },
    };

    setup() {
        this.state = useState({
            error: "",
            search: "",
            solucion: this.props.item.solucion || "",
            estado_equipo: this.props.item.estado_equipo || "en_proceso",
            selectedBaseIds: this.getInitialSelectedBaseIds(),
        });
    }

    getInitialSelectedBaseIds() {
        return (this.props.fallasSeleccionadas || []).map((falla) => {
            return falla.base_conocimiento_id;
        });
    }

    get baseFiltrada() {
        const term = this.state.search.trim().toLowerCase();

        let data = this.props.baseConocimiento || [];

        if (term) {
            data = data.filter((item) => {
                const text = [
                    item.error_title,
                    item.symptoms,
                    item.root_cause,
                    item.solution,
                    item.keywords,
                ].join(" ").toLowerCase();

                return text.includes(term);
            });
        }

        return data;
    }

    updateField(field, value) {
        this.state[field] = value;
    }

    isSelected(baseId) {
        return this.state.selectedBaseIds.includes(baseId);
    }

    toggleBase(baseId) {
        if (this.isSelected(baseId)) {
            this.state.selectedBaseIds = this.state.selectedBaseIds.filter((id) => {
                return id !== baseId;
            });
            return;
        }

        this.state.selectedBaseIds.push(baseId);
    }

    async guardar() {
        try {
            this.state.error = "";

            await this.props.onSave({
                mantenimiento_equipo_id: this.props.item.id,
                solucion: this.state.solucion || false,
                estado_equipo: this.state.estado_equipo,
                base_conocimiento_ids: this.state.selectedBaseIds,
            });

        } catch (error) {
            console.error(error);
            this.state.error = error.message || "No se pudo guardar la solución.";
        }
    }

    cancelar() {
        this.props.onCancel();
    }
}
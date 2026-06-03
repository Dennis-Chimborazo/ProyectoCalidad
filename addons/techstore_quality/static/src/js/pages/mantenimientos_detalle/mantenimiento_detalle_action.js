/** @odoo-module **/

import { registry } from "@web/core/registry";
import { MantenimientoDetalleApp } from "./mantenimiento_detalle_app";

registry.category("actions").add(
    "techstore_mantenimiento_detalle_app_action",
    MantenimientoDetalleApp
);
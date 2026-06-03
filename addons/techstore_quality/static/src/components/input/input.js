/** @odoo-module **/

import { Component } from "@odoo/owl";
import { TechStoreTheme } from "../../core/theme";

export class TsInput extends Component {
    setup() {
        this.theme = TechStoreTheme;
    }
}

TsInput.template = "techstore.TsInput";
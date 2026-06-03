/** @odoo-module **/

import { Component } from "@odoo/owl";
import { TechStoreTheme } from "../../core/theme";

export class TsSelect extends Component {
    setup() {
        this.theme = TechStoreTheme;
    }

    get options() {
        return this.props.options || [];
    }
}

TsSelect.template = "techstore.TsSelect";
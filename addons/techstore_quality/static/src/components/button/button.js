/** @odoo-module **/

import { Component } from "@odoo/owl";
import { TechStoreTheme } from "../../core/theme";

export class TsButton extends Component {
    setup() {
        this.theme = TechStoreTheme;
    }

    get buttonClass() {
        const variant = this.props.variant || "primary";

        if (variant === "secondary") {
            return this.theme.classes.buttonSecondary;
        }

        if (variant === "danger") {
            return this.theme.classes.buttonDanger;
        }

        return this.theme.classes.buttonPrimary;
    }
}

TsButton.template = "techstore.TsButton";
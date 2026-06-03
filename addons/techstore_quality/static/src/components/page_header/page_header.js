/** @odoo-module **/

import { Component } from "@odoo/owl";
import { TechStoreTheme } from "../../core/theme";
import { TechStoreAnimations } from "../../core/animations";

export class TsPageHeader extends Component {
    setup() {
        this.theme = TechStoreTheme;
        this.animations = TechStoreAnimations;
    }

    get headerClass() {
        return `${this.theme.classes.header} ${this.animations.fadeIn}`;
    }
}

TsPageHeader.template = "techstore.TsPageHeader";
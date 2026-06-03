/** @odoo-module **/

import { Component } from "@odoo/owl";
import { TechStoreTheme } from "../../core/theme";
import { TechStoreAnimations } from "../../core/animations";

export class TsCard extends Component {
    setup() {
        this.theme = TechStoreTheme;
        this.animations = TechStoreAnimations;
    }

    get cardClass() {
        return `${this.theme.classes.card} ${this.animations.slideUp}`;
    }
}

TsCard.template = "techstore.TsCard";
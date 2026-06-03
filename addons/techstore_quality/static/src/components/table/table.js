/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TechStoreTheme } from "../../core/theme";

export class TsTable extends Component {
    setup() {
        this.theme = TechStoreTheme;

        this.state = useState({
            currentPage: 1,
            pageSize: this.props.pageSize || 10,
        });
    }

    get columns() {
        return this.props.columns || [];
    }

    get rows() {
        return this.props.rows || [];
    }

    get actions() {
        return this.props.actions || [];
    }

    get hasActions() {
        return this.actions.length > 0;
    }

    get totalRows() {
        return this.rows.length;
    }

    get totalPages() {
        return Math.max(1, Math.ceil(this.totalRows / this.state.pageSize));
    }

    get currentPage() {
        if (this.state.currentPage > this.totalPages) {
            this.state.currentPage = this.totalPages;
        }

        return this.state.currentPage;
    }

    get startIndex() {
        return (this.currentPage - 1) * this.state.pageSize;
    }

    get endIndex() {
        return Math.min(this.startIndex + this.state.pageSize, this.totalRows);
    }

    get paginatedRows() {
        return this.rows.slice(this.startIndex, this.endIndex);
    }

    get showingFrom() {
        if (!this.totalRows) {
            return 0;
        }

        return this.startIndex + 1;
    }

    get showingTo() {
        return this.endIndex;
    }

    nextPage() {
        if (this.state.currentPage < this.totalPages) {
            this.state.currentPage++;
        }
    }

    previousPage() {
        if (this.state.currentPage > 1) {
            this.state.currentPage--;
        }
    }

    goToFirstPage() {
        this.state.currentPage = 1;
    }

    goToLastPage() {
        this.state.currentPage = this.totalPages;
    }

    getCellValue(row, col) {
        const value = row[col.key];

        if (value === undefined || value === null || value === false) {
            return "";
        }

        if (col.type === "money") {
            return "$ " + Number(value).toFixed(2);
        }

        return value;
    }

    getBooleanBadgeLabel(row, col) {
        const value = Boolean(row[col.key]);

        if (col.trueLabel || col.falseLabel) {
            return value ? col.trueLabel : col.falseLabel;
        }

        return value ? "Activo" : "Inactivo";
    }

    getBooleanBadgeClass(row, col) {
        const value = Boolean(row[col.key]);

        return value
            ? this.theme.classes.badgeSuccess
            : this.theme.classes.badgeDanger;
    }

    isActionVisible(action, row) {
        if (!action.visible) {
            return true;
        }

        return action.visible(row);
    }

    getActionLabel(action, row) {
        if (typeof action.label === "function") {
            return action.label(row);
        }

        return action.label;
    }

    getActionVariant(action, row) {
        if (typeof action.variant === "function") {
            return action.variant(row);
        }

        return action.variant || "primary";
    }

    getDynamicActionClass(action, row) {
        const variant = this.getActionVariant(action, row);

        if (variant === "secondary") {
            return this.theme.classes.buttonSecondary + " ts-btn-sm";
        }

        if (variant === "danger") {
            return this.theme.classes.buttonDanger + " ts-btn-sm";
        }

        return this.theme.classes.buttonPrimary + " ts-btn-sm";
    }

    getStatusBadgeLabel(row, col) {
    const value = row[col.key];

    if (value === "aceptable") {
        return "Aceptable";
    }

    if (value === "observado") {
        return "Observado";
    }

    if (value === "pendiente") {
        return "Pendiente";
    }

    return value || "Sin estado";
}

getStatusBadgeClass(row, col) {
    const value = row[col.key];

    if (value === "aceptable") {
        return this.theme.classes.badgeSuccess;
    }

    if (value === "observado") {
        return this.theme.classes.badgeDanger;
    }

    if (value === "pendiente") {
        return this.theme.classes.badgeWarning;
    }

    return this.theme.classes.badgeInfo;
}
}

TsTable.template = "techstore.TsTable";
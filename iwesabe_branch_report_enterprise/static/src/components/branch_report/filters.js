/** @odoo-module **/

import { registry } from "@web/core/registry";
import {
    Many2ManyTagsField,
    many2ManyTagsField,
} from "@web/views/fields/many2many_tags/many2many_tags_field";

export class Many2ManyTagsBranch extends Many2ManyTagsField {
    static template = "iwesabe_branch.Many2ManyTagsBranch";

    getTagProps(record) {
        return {
            ...super.getTagProps(record),
            text: record.data.display_name,
        };
    }
}

export const fieldMany2ManyTagsBranch = {
    ...many2ManyTagsField,
    component: Many2ManyTagsBranch,
    relatedFields: (fieldInfo) => [
        ...many2ManyTagsField.relatedFields(fieldInfo),
        { name: "display_name", type: "char" },
    ],
};

registry.category("fields").add(
    "many2many_tags_branch",
    fieldMany2ManyTagsBranch
);

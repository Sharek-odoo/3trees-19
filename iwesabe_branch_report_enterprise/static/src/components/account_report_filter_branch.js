import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { AccountReportFilters } from "@account_reports/components/account_report/filters/filters";

patch(AccountReportFilters.prototype, {
    custom_events: {
    'branch_filter_changed': function(ev) {
        console.log("BRANCH JS EVENT FIRED");
        console.log("Received branch_ids:", ev.data.branch_ids);

        this.report_options.branch_ids = ev.data.branch_ids;
        return this.reload().then(() => {
            this.$searchview_buttons.find('.account_branches_filter').click();
        });
    },
},


    get filterExtraOptionsData() {
        return {
            ...super.filterExtraOptionsData,
            branch: {
                name: _t("Branch"),
                group: "account_user",
                show: this.controller.filters.filter_branch,   // backend field
                multi: true,  // لأنه Many2many
                model: "res.branch",
                fieldNames: ["name"],
            },
        };
    },

    get selectedExtraOptions() {
        let selected = super.selectedExtraOptions;

        if (this.controller.filters.filter_branch) {
            const branches = this.controller.cachedFilterOptions.branch_ids || [];

            if (branches.length) {
                const branchNames = branches.map(b => b.name).join(", ");
                selected = selected ? `${selected}, ${branchNames}` : branchNames;
            }
        }
        return selected;
    },
});

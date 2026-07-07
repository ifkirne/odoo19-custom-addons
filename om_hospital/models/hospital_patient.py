from odoo import api, fields, models

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = "Hospital Patient"

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', default='male')
    active = fields.Boolean(string='Active', default=True)
































    # _order = "code, placeholder_code"
    # _check_company_auto = True
    # _check_company_domain = models.check_companies_domain_parent_of
    #
    # @api.constrains('account_type', 'reconcile')
    # def _check_reconcile(self):
    #     for account in self:
    #         if account.account_type in ('asset_receivable', 'liability_payable') and not account.reconcile:
    #             raise ValidationError(_('You cannot have a receivable/payable account that is not reconcilable. (account code: %s)', account.code))
    #
    # name = fields.Char(string="Account Name", required=True, index='trigram', tracking=True, translate=True)
    # description = fields.Text(translate=True)
    # currency_id = fields.Many2one('res.currency', string='Account Currency', tracking=True,
    #     help="Forces all journal items in this account to have a specific currency (i.e. bank journals). If no currency is set, entries can use any currency.")
    # company_currency_id = fields.Many2one('res.currency', compute='_compute_company_currency_id')
    # company_fiscal_country_code = fields.Char(compute='_compute_company_fiscal_country_code')
    # code = fields.Char(string="Code", size=64, tracking=True, compute='_compute_code', search='_search_code', inverse='_inverse_code')
    # code_store = fields.Char(company_dependent=True)
    # placeholder_code = fields.Char(string="Display code", compute='_compute_placeholder_code', search='_search_placeholder_code')
    # active = fields.Boolean(default=True, tracking=True)
    # used = fields.Boolean(compute='_compute_used', search='_search_used')
    # account_type = fields.Selection(
    #     selection=[
    #         ("asset_receivable", "Receivable"),
    #         ("asset_cash", "Bank and Cash"),
    #         ("asset_current", "Current Assets"),
    #         ("asset_non_current", "Non-current Assets"),
    #         ("asset_prepayments", "Prepayments"),
    #         ("asset_fixed", "Fixed Assets"),
    #         ("liability_payable", "Payable"),
    #         ("liability_credit_card", "Credit Card"),
    #         ("liability_current", "Current Liabilities"),
    #         ("liability_non_current", "Non-current Liabilities"),
    #         ("equity", "Equity"),
    #         ("equity_unaffected", "Current Year Earnings"),
    #         ("income", "Income"),
    #         ("income_other", "Other Income"),
    #         ("expense", "Expenses"),
    #         ("expense_other", "Other Expenses"),
    #         ("expense_depreciation", "Depreciation"),
    #         ("expense_direct_cost", "Cost of Revenue"),
    #         ("off_balance", "Off-Balance Sheet"),
    #     ],
    #     string="Type", tracking=True,
    #     required=True,
    #     compute='_compute_account_type', store=True, readonly=False, precompute=True, index=True,
    #     help="Account Type is used for information purpose, to generate country-specific legal reports, and set the rules to close a fiscal year and generate opening entries."
    # )
    # include_initial_balance = fields.Boolean(string="Bring Accounts Balance Forward",
    #     help="Used in reports to know if we should consider journal items from the beginning of time instead of from the fiscal year only. Account types that should be reset to zero at each new fiscal year (like expenses, revenue..) should not have this option set.",
    #     compute="_compute_include_initial_balance",
    #     search="_search_include_initial_balance",
    # )
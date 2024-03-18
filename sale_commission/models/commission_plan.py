from odoo import fields, models, api

class CommissionPlan(models.Model):
    _name = 'commission.plan'
    _description = 'commission plan'

    commission_plan = fields.Char(required=True)
    date_from = fields.Date()
    date_to = fields.Date()
    company = fields.Char()
    target = fields.Float(string="Target", compute="_compute_total_target",store=True, readonly=True)
    product_ids = fields.Many2many('product.product')
    sales_team_id = fields.Many2one('crm.team')
    salesperson_id = fields.Many2one('res.users')
    target_ids = fields.One2many('sale.commission.period', 'commission_plan_ids')
    state = fields.Selection([('draft','Draft'),('approved','Approved'),('done','Done'),('cancel','Cancel')], default='draft')
    commissions_ids = fields.One2many('commission.plan.method', 'commission_plan_id', string="Commissions")

    def state_approve(self):
        for record in self:
            self.state = 'approved'

    def state_cancel(self):
        for record in self:
            self.state = 'cancel'

    @api.depends('target_ids.target_amount')
    def _compute_total_target(self):
        for record in self:
            record.target = sum(record.target_ids.mapped('target_amount'))


    @api.depends('salesperson_id')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.salesperson_id.name}({record.sales_team_id.name})"

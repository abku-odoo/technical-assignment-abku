from odoo import fields, models, api

class CommissionPlanmethod(models.Model):
    _name = 'commission.plan.method'
    _description = 'Sales Commissions plans from the logic'

    min_achievement = fields.Float(string="Min. Achievement")
    commission_rate = fields.Float(string="Commission")
    commission_plan_id = fields.Many2one('commission.plan')


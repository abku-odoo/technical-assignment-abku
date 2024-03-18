# -*- coding: utf-8 -*-
#Part of Odoo. See LICENSE file for full copyright and licensing details
from odoo import fields, models, api
from odoo.exceptions import ValidationError

class SalesCommissionsPlansReport(models.Model):
    _name = "sale.commission.plans.report"
    _description = "Sale Commission Plan Reports"

    commission_plan_id = fields.Many2one('commission.plan', string="Commission Plan")
    target_id = fields.Many2one('sale.commission.period', string="Target Quarter")
    achieved_amount = fields.Float(default=0, compute='_compute_achieved_amount', store=True)
    target_amount = fields.Float(compute='_compute_tree_values')
    salesperson_id = fields.Many2one('res.users', string="Salesperson", compute='_compute_tree_values')
    sales_team_id = fields.Many2one('crm.team', string="Sales Team", compute='_compute_tree_values')
    desired_commission_rate = fields.Float(string="Commission Rate",compute='_compute_desired_commission_rate')

    def _compute_achieved_amount(self):
        for record in self:
            orders = self.env['sale.order.line'].search([
                ('salesman_id.id', '=', record.commission_plan_id.salesperson_id.id),
                ('order_id.date_order', '>=', record.commission_plan_id.date_from),
                ('order_id.date_order', '<=', record.commission_plan_id.date_to),
                ])
            amt = 0
            for order in orders:
                if order.product_id.id in record.commission_plan_id.product_ids.ids:
                    amt += order.price_subtotal
            self.achieved_amount = amt

    @api.depends('commission_plan_id')
    def _compute_tree_values(self):
        for record in self:
            record.target_amount = record.commission_plan_id.target
            record.salesperson_id = record.commission_plan_id.salesperson_id
            record.sales_team_id = record.commission_plan_id.sales_team_id

    @api.depends('commission_plan_id', 'achieved_amount')
    def _compute_desired_commission_rate(self):
        for record in self:
            record.desired_commission_rate = 0
            if record.commission_plan_id:
                achievement_percent = (record.achieved_amount / record.target_amount) * 100 if record.target_amount != 0 else 0
                desired_rate = 0
                for commission in record.commission_plan_id.commissions_ids:
                    if commission.min_achievement <= achievement_percent:
                        desired_rate = commission.commission_rate
                    else:
                        break
                record.desired_commission_rate = desired_rate
            record._compute_achieved_amount()
            
            
         
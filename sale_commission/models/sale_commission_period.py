from odoo import fields, models, api
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class SaleCommissionPeriod(models.Model):
    _name = 'sale.commission.period'
    _rec_name = "quarter"
    
    commission_plan_ids =  fields.Many2one('commission.plan')
    quarter = fields.Selection([('q1','Q1'),('q2','Q2'),('q3',"Q3"),('q4',"Q4")])
    date_from = fields.Date()
    date_to = fields.Date(string="Date To", compute='_compute_date_to', store=True)
    year = fields.Char(string="Year", compute='_compute_date_to', store=True)
    target_amount = fields.Float()

    @api.depends('date_from')
    def _compute_date_to(self):
        for record in self:
            if record.date_from:
                record.date_to = record.date_from + relativedelta(days=90)
                record.year = str(record.date_from.year)
            else:
                record.date_to = False
from odoo import models, api, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_sale_commission = fields.Boolean(string="Sales Commission")
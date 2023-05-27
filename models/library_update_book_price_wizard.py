from odoo import models, fields, api

class UpdateBookPriceWizard(models.TransientModel):
    _name = 'library.update.book.price.wizard'
    _description = 'Update Book Price Wizard'

    new_price = fields.Float(string='New Price', required=True)

    def update_book_prices(self):
        active_ids = self.env.context.get('active_ids', [])
        books = self.env['library.book'].browse(active_ids)
        books.write({'price': self.new_price})
        return {'type': 'ir.actions.act_window_close'}



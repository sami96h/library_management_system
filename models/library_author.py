from odoo import api,fields, models
from datetime import datetime, timedelta
from odoo.exceptions import UserError, AccessError
import logging


_logger = logging.getLogger(__name__)

class libraryAuthor(models.Model):
    _name = "library.author"

    name = fields.Char(required=True)
    birth_date = fields.Date( "Birth Date",copy=False,default=lambda self: fields.Datetime.now())
    book_ids = fields.Many2many('library.book')
    total_books = fields.Integer(compute="_calculate_total_books")

    @api.depends('book_ids')
    def _calculate_total_books(self):
        
        for record in self:
            if record.book_ids:
                record.total_books = len(record.book_ids)
            else:
               record.total_books = 0


    def action_related_books(self):
        self.ensure_one()
        _logger.info('********xxxxxxxxxxxxxxx*******xxxxxxxxxxx*'+str(self.book_ids.ids))
        return {
            'name':("Related Books"),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form,kanban',
            'res_model': 'library.book',
            'domain': [('id', 'in', self.book_ids.ids)]
            }

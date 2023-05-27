from odoo import api,fields, models
from odoo.exceptions import UserError, AccessError,ValidationError

class libraryBook(models.Model):
    _name = "library.book.copy"

    name = fields.Char(required=True)
    book_id = fields.Many2one('library.book')
    reservation_ids = fields.One2many('library.reservation','copy_id')
    status = fields.Selection(selection=[('available', 'Available'),('borrowed', 'Borrowed')],copy= False,default='available')


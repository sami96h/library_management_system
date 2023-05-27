from odoo import api,fields, models
from odoo.exceptions import UserError, AccessError,ValidationError

class libraryBook(models.Model):
    _name = "library.book"

    name = fields.Char(required=True)
    copy_ids =  fields.One2many('library.book.copy','book_id')
    isbn = fields.Char(required=True)
    author_ids = fields.Many2many('library.author')
    publication_date = fields.Date("Publication Date",copy=False,default=lambda self: fields.Datetime.now())
    price = fields.Float("Price",required=True)
    related_authors_count = fields.Integer(compute='_compute_related_authors_count')
    amount = fields.Integer('Total books',compute='_calculate_total_copies',default=0)
    in_stock = fields.Integer('Available Books',compute='_calculate_available_copies',default=0)
    reservation_ids = fields.One2many('library.reservation', compute='_compute_reservation_ids')



    @api.depends('copy_ids')
    def _calculate_total_copies(self):
        for book in self:
            
            book.amount = len(book.copy_ids)

    @api.depends('copy_ids')
    def _calculate_available_copies(self):
        for book in self:
            available_copies = book.copy_ids.filtered(lambda copy: copy.status == 'available')
            book.in_stock = len(available_copies)



    @api.depends('copy_ids.reservation_ids')
    def _compute_reservation_ids(self):
        for book in self:
            reservations = book.copy_ids.mapped('reservation_ids')
            book.reservation_ids = reservations

    @api.onchange('isbn')
    def onchange_isbn(self):
        if self.isbn:
            existing_records = self.search_count([('isbn', '=', self.isbn)])
            if existing_records > 0:
                raise ValidationError('The Isbn must be unique.')

    def action_related_authors(self):
        self.ensure_one()
        return {
            'name':("Related Authors"),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form,kanban',
            'res_model': 'library.author',
            'domain': [('id', 'in', self.author_ids.ids)]
            }

    @api.depends('author_ids')
    def _compute_related_authors_count(self):
        for book in self:
            book.related_authors_count = len(book.author_ids)

    def open_reservation_form(self):
        available_copy = self.copy_ids.filtered(lambda copy: copy.status == 'available')
        if available_copy:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Create Reservation',
                'res_model': 'library.reservation',
                'view_mode': 'form',
                'target': 'new',
                'context': {'default_copy_id': available_copy[0].id},
            }
        else:
            raise UserError("No available copies for reservation.")
from odoo import api,fields, models
from odoo.exceptions import UserError, AccessError,ValidationError
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

class libraryReservation(models.Model):
    _name = "library.reservation"

    copy_id = fields.Many2one('library.book.copy')
    date_from = fields.Date( "Reservation Date",copy=False,default=lambda self: fields.Datetime.now())
    borrowing_period = fields.Integer('Borrowing Period (days)',compute='_calculate_borrowing_period')
    return_date = fields.Date( "Return Date",copy=False,default=lambda self: fields.Datetime.now())
    partner_id = fields.Many2one('res.partner',required=True)
    price = fields.Float(required=True)
    status = fields.Selection(selection=[('draft', 'Draft'),('accepted', 'Accepted'), ('refused','Refused'),('late','Late'),('closed','Closed')],copy= False,default='draft')
    fees = fields.Float(default=0)
    #compute='_calculate_fees',
    @api.depends('date_from','return_date')
    def _calculate_borrowing_period(self):
        for record in self:
            record.borrowing_period = (record.return_date - record.date_from).days

    def accept_reservation(self):

        for record in self:
            if record.copy_id.status != 'available' :
                raise UserError('The copy is not available yet.')
               
            record.status = 'accepted'
            record.copy_id.status = 'borrowed'
        return True

    
    def refuse_reservation(self):

        for record in self:
               
            record.status = 'refused'
            
        return True

    @api.model
    def create(self,vals):
        
        current_datetime = datetime.now()



        #  _logger.info('****************'+str(datetime.strptime(vals['date_from'], '%Y-%m-%d') > datetime.strptime(vals['return_date'], '%Y-%m-%d')))
        if current_datetime.date() > datetime.strptime(vals['date_from'], '%Y-%m-%d').date():
            raise UserError('The borrowing date must be set to a future date, later than the current day.')
 
        if datetime.strptime(vals['date_from'], '%Y-%m-%d') > datetime.strptime(vals['return_date'], '%Y-%m-%d'):
            raise UserError('The return date should be later than the borrowing date. Please select a valid return date.')
        
        book_copy = self.env['library.book.copy'].browse(vals['copy_id'])
        reservations = book_copy.reservation_ids
                                                                                                                                                                                                                                                                                                                        
        for reservation in reservations:
            # _logger.info('****************'+str(reservations.date_from)+str(vals['date_from']))

            if  (datetime.strptime(str(reservation.date_from), '%Y-%m-%d') <= datetime.strptime(vals['date_from'], '%Y-%m-%d') and datetime.strptime(vals['date_from'], '%Y-%m-%d') <= datetime.strptime(str(reservation.return_date), '%Y-%m-%d')) or (datetime.strptime(str(reservation.date_from), '%Y-%m-%d') <= datetime.strptime(vals['return_date'], '%Y-%m-%d') and datetime.strptime(vals['return_date'], '%Y-%m-%d') <= datetime.strptime(str(reservation.return_date), '%Y-%m-%d')) :
                if reservation.status == 'accepted':
                    raise UserError('The selected time slot is already reserved for this copy. Please choose another time slot.')

        # property = self.env['estate.property'].browse(vals['property_id'])
        # offers = property.offer_ids

        # for offer in offers:
        #     if  offer.price > vals['price']:
        #         raise UserError('An offer with higher price already existed !')

        # property.state = 'offer_received'
        return super().create(vals)

    @api.depends('return_date')
    def _calculate_fees(self):
        return
        # current_datetime = datetime.now()

        # for reservation in self:
        #     returnDate = datetime.strptime(str(reservation.return_date), '%Y-%m-%d').date()
        #     if current_datetime.date() > returnDate :
        #         reservation.status = 'late'
        #         reservation.fees = (current_datetime.date() - returnDate).days



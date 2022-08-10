# -*- coding: utf-8 -*-
import datetime
import email
from odoo.addons.website.controllers.main import Website
from odoo import http
from odoo.http import request

from odoo import fields


class Main(http.Controller):
    # Add a controller that serves the list of books
    @http.route('/books', type='http', auth="user",
                website=True)
    def library_books(self):
        return request.render(
            'my_library.books', {
                'books': request.env['library.book'].search([]),
            })

# A new route for book details
    @http.route('/books/<model("library.book"):book>',
                type='http', auth="user", website=True)
    def library_book_detail(self, book):
        return request.render(
            'my_library.book_detail', {
                'book': book,
            })

    @http.route('/my_library/books', type='http',
                auth='none')
    def books(self):
        books = request.env['library.book'].sudo().search([])
        html_result = '<html><body><ul>'
        for book in books:
            html_result += "<li> %s </li>" % book.name
        html_result += '</ul></body></html>'
        return request.make_response(
            html_result, headers=[
                ('Last-modified', email.utils.formatdate(
                    (fields.Datetime.from_string(
                        request.env['library.book'].sudo().search([], order='write_date desc', limit=1)
                            .write_date) -
                     datetime.datetime(1970, 1, 1)
                     ).total_seconds(),
                    usegmt=True)),
            ])

    # A path that shows all the books
    @http.route('/my_library/all-books', type='http',
                auth='none')
    def all_books(self):
        books = request.env['library.book'].sudo().search([])
        html_result = '<html><body><ul>'
        for book in books:
            html_result += "<li> %s </li>" % book.name
        html_result += '</ul></body></html>'
        return html_result

    # A path that shows all the books and indicates which were written by the current
    # user, if any
    @http.route('/my_library/all-books/mark-mine', type='http',
                auth='public')
    def all_books_mark_mine(self):
        books = request.env['library.book'].sudo().search([])
        html_result = '<html><body><ul>'
        for book in books:
            if request.env.user.partner_id.id in book.author_ids.ids:
                html_result += "<li> <b>%s</b> </li>" % book.name
            else:
                html_result += "<li> %s </li>" % book.name
        html_result += '</ul></body></html>'
        return html_result

    # A path that shows the current user's books
    @http.route('/my_library/all-books/mine', type='http',
                auth='user')
    def all_books_mine(self):
        books = request.env['library.book'].search([
            ('author_ids', 'in', request.env.user.partner_id.ids),
        ])
        html_result = '<html><body><ul>'
        for book in books:
            html_result += "<li> %s </li>" % book.name
        html_result += '</ul></body></html>'
        return html_result

    # A path that expects a book's ID as a parameter
    @http.route('/my_library/book_details', type='http',
                auth='none')
    def book_details(self, book_id):
        record = request.env['library.book'].sudo().browse(int(book_id))
        return u'<html><body><h1>%s</h1>Authors: %s' % (
            record.name, u', '.join(record.author_ids.mapped('name')) or 'none',)

    # A path where we can pass the book's ID in the path
    @http.route("/my_library/book_details/<model('library.book'):book>",
                type='http', auth='none')
    def book_details_in_path(self, book):
        return self.book_details(book.id)

    # show an image on the page
    @http.route('/demo_page', type='http', auth='none')
    def books(self):
        image_url = '/my_library/static/src/img/ilya-pavlov-OqtafYT5kTw-unsplash.jpg'
        html_result = """<html><body><img src="%s"/></body></html>""" % image_url
        return html_result

    # json
    @http.route('/my_library/books/json', type='json',
                auth='none')
    def books_json(self):
        records = request.env['library.book'].sudo().search([])
        return records.read(['name'])

        curl - i - X
        POST - H
        "Content-Type: application/json" - d
        "{}"
        localhost: 8069 / my_library / books / json

        # Override the handler in a file called controllers/main.py
        class WebsiteInfo(Website):
            @http.route('/my/')
            def website_info(self):
                result = super(WebsiteInfo, self).website_info()
                result.qcontext['apps'] = result.qcontext['apps'].filtered(
                    lambda x: x.name != 'website')

        return result
        response.is_qweb
        response.render()

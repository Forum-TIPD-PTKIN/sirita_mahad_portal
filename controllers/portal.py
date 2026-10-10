# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

class MahasantriPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id

        if 'permit_count' in counters:
            values['permit_count'] = request.env['mahad.permit'].search_count([
                ('student_id', '=', partner.id)
            ]) if 'mahad.permit' in request.env else 0

        if 'talim_count' in counters:
            values['talim_count'] = request.env['mahad.talim.record'].search_count([
                ('student_id', '=', partner.id)
            ]) if 'mahad.talim.record' in request.env else 0

        if 'penalty_count' in counters:
            values['penalty_count'] = request.env['mahad.penalty.record'].search_count([
                ('student_id', '=', partner.id)
            ]) if 'mahad.penalty.record' in request.env else 0

        if 'syahadah_count' in counters:
            values['syahadah_count'] = request.env['mahad.syahadah'].search_count([
                ('student_id', '=', partner.id)
            ]) if 'mahad.syahadah' in request.env else 0

        return values

    @http.route(['/my/permits'], type='http', auth="user", website=True)
    def portal_my_permits(self, **kw):
        partner = request.env.user.partner_id
        permits = request.env['mahad.permit'].search([
            ('student_id', '=', partner.id)
        ], order="create_date desc") if 'mahad.permit' in request.env else []
        
        values = self._prepare_portal_layout_values()
        values.update({
            'permits': permits,
            'page_name': 'permit_list',
        })
        return request.render("sirita_mahad_portal.portal_my_permits", values)

    @http.route(['/my/talim'], type='http', auth="user", website=True)
    def portal_my_talim(self, **kw):
        partner = request.env.user.partner_id
        talim_records = request.env['mahad.talim.record'].search([
            ('student_id', '=', partner.id)
        ], order="date desc") if 'mahad.talim.record' in request.env else []

        values = self._prepare_portal_layout_values()
        values.update({
            'talim_records': talim_records,
            'page_name': 'talim_list',
        })
        return request.render("sirita_mahad_portal.portal_my_talim", values)

    @http.route(['/my/penalties'], type='http', auth="user", website=True)
    def portal_my_penalties(self, **kw):
        partner = request.env.user.partner_id
        penalties = request.env['mahad.penalty.record'].search([
            ('student_id', '=', partner.id)
        ], order="date desc") if 'mahad.penalty.record' in request.env else []

        values = self._prepare_portal_layout_values()
        values.update({
            'penalties': penalties,
            'page_name': 'penalty_list',
        })
        return request.render("sirita_mahad_portal.portal_my_penalties", values)

    @http.route(['/my/syahadah'], type='http', auth="user", website=True)
    def portal_my_syahadah(self, **kw):
        partner = request.env.user.partner_id
        syahadah_records = request.env['mahad.syahadah'].search([
            ('student_id', '=', partner.id)
        ], order="create_date desc") if 'mahad.syahadah' in request.env else []

        values = self._prepare_portal_layout_values()
        values.update({
            'syahadah_records': syahadah_records,
            'page_name': 'syahadah_list',
        })
        return request.render("sirita_mahad_portal.portal_my_syahadah", values)

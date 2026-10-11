from urllib.parse import quote_plus
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
            'success_msg': kw.get('success_msg'),
            'error_msg': kw.get('error_msg'),
        })
        return request.render("sirita_mahad_portal.portal_my_permits", values)

    @http.route(['/my/permits/new'], type='http', auth="user", website=True)
    def portal_my_permits_new(self, **kw):
        values = self._prepare_portal_layout_values()
        values.update({
            'page_name': 'permit_form',
            'error_msg': kw.get('error_msg'),
        })
        return request.render("sirita_mahad_portal.portal_my_permits_new", values)

    @http.route(['/my/permits/submit'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def portal_my_permits_submit(self, **post):
        partner = request.env.user.partner_id
        permit_type = post.get('permit_type')
        reason = post.get('reason')
        destination = post.get('destination')
        departure_time = post.get('departure_time')
        expected_return_time = post.get('expected_return_time')

        if not (permit_type and reason and destination and departure_time and expected_return_time):
            return request.redirect('/my/permits/new?error_msg=Harap+lengkapi+seluruh+isian+formulir+perizinan.')

        try:
            request.env['mahad.permit'].sudo().create({
                'student_id': partner.id,
                'permit_type': permit_type,
                'reason': reason,
                'destination': destination,
                'departure_time': departure_time.replace('T', ' '),
                'expected_return_time': expected_return_time.replace('T', ' '),
                'state': 'draft',
            })
            return request.redirect('/my/permits?success_msg=Pengajuan+perizinan+berhasil+dikirim.')
        except Exception as e:
            return request.redirect(f'/my/permits/new?error_msg={quote_plus(str(e))}')

    @http.route(['/my/talim'], type='http', auth="user", website=True)
    def portal_my_talim(self, **kw):
        partner = request.env.user.partner_id
        talim_records = request.env['mahad.talim.record'].search([
            ('student_id', '=', partner.id)
        ], order="date desc") if 'mahad.talim.record' in request.env else []

        classes = request.env['mahad.talim.class'].search([
            ('student_ids', 'in', [partner.id])
        ]) if 'mahad.talim.class' in request.env else []

        # Hitung statistik sederhana
        ziyadah_count = len([r for r in talim_records if r.category == 'ziyadah'])
        mumtaz_count = len([r for r in talim_records if r.grade_status == 'mumtaz'])

        values = self._prepare_portal_layout_values()
        values.update({
            'talim_records': talim_records,
            'classes': classes,
            'ziyadah_count': ziyadah_count,
            'mumtaz_count': mumtaz_count,
            'page_name': 'talim_list',
            'success_msg': kw.get('success_msg'),
            'error_msg': kw.get('error_msg'),
        })
        return request.render("sirita_mahad_portal.portal_my_talim", values)

    @http.route(['/my/talim/submit'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def portal_my_talim_submit(self, **post):
        partner = request.env.user.partner_id
        class_id = post.get('class_id')
        category = post.get('category')
        surah_juz_topic = post.get('surah_juz_topic')
        notes = post.get('notes')

        if not (class_id and category and surah_juz_topic):
            return request.redirect('/my/talim?error_msg=Harap+isi+lengkapi+kelas+dan+target+setoran.')

        try:
            request.env['mahad.talim.record'].sudo().create({
                'student_id': partner.id,
                'class_id': int(class_id),
                'category': category,
                'surah_juz_topic': surah_juz_topic,
                'notes': f"[Mandiri Portal] {notes}" if notes else "[Mandiri Portal] Pengajuan Janji Setoran",
                'grade_status': 'jayyid',
            })
            return request.redirect('/my/talim?success_msg=Janji+setoran+hafalan+berhasil+diajukan.')
        except Exception as e:
            return request.redirect(f'/my/talim?error_msg={quote_plus(str(e))}')

    @http.route(['/my/invoices'], type='http', auth="user", website=True)
    def portal_my_invoices(self, **kw):
        partner = request.env.user.partner_id
        invoices = request.env['hostel.rent.invoice'].search([
            ('student_id', '=', partner.id)
        ], order="period_start desc") if 'hostel.rent.invoice' in request.env else []

        unpaid_count = len([i for i in invoices if i.state in ('draft', 'invoiced', 'overdue')])
        paid_count = len([i for i in invoices if i.state == 'paid'])

        values = self._prepare_portal_layout_values()
        values.update({
            'invoices': invoices,
            'unpaid_count': unpaid_count,
            'paid_count': paid_count,
            'page_name': 'invoice_list',
            'success_msg': kw.get('success_msg'),
            'error_msg': kw.get('error_msg'),
        })
        return request.render("sirita_mahad_portal.portal_my_invoices", values)

    @http.route(['/my/invoices/upload_proof'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def portal_my_invoices_upload_proof(self, **post):
        partner = request.env.user.partner_id
        invoice_id = post.get('invoice_id')
        notes = post.get('notes')

        if not invoice_id:
            return request.redirect('/my/invoices?error_msg=Tagihan+tidak+valid.')

        try:
            inv = request.env['hostel.rent.invoice'].sudo().browse(int(invoice_id))
            if inv and inv.student_id.id == partner.id:
                # Catat bukti bayar ke chatter / notes
                inv.sudo().message_post(
                    body=f"<b>Konfirmasi Bukti Transfer Mahasantri (Portal):</b><br/>{notes or 'Konfirmasi pembayaran via transfer bank.'}",
                    subject="Konfirmasi Pembayaran Portal"
                )
                return request.redirect('/my/invoices?success_msg=Konfirmasi+bukti+pembayaran+berhasil+dikirim+ke+pengelola.')
            return request.redirect('/my/invoices?error_msg=Data+tagihan+tidak+ditemukan.')
        except Exception as e:
            return request.redirect(f'/my/invoices?error_msg={quote_plus(str(e))}')

    @http.route(['/my/penalties'], type='http', auth="user", website=True)
    def portal_my_penalties(self, **kw):
        partner = request.env.user.partner_id
        penalties = request.env['mahad.penalty.record'].search([
            ('student_id', '=', partner.id)
        ], order="date desc") if 'mahad.penalty.record' in request.env else []

        total_points = sum(p.points for p in penalties if p.state in ('confirmed', 'completed'))
        sp_status = partner.sp_status or 'aman'

        values = self._prepare_portal_layout_values()
        values.update({
            'penalties': penalties,
            'total_points': total_points,
            'sp_status': sp_status,
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

    @http.route(['/syahadah/print/<int:syahadah_id>'], type='http', auth="user", website=True)
    def portal_my_syahadah_print(self, syahadah_id=None, **kw):
        partner = request.env.user.partner_id
        syahadah = request.env['mahad.syahadah'].sudo().browse(syahadah_id)
        if not syahadah or (syahadah.student_id.id != partner.id and not request.env.user.has_group('base.group_user')):
            return request.redirect('/my/syahadah')

        report = request.env.ref('sirita_mahad_pembinaan.action_report_mahad_syahadah', raise_if_not_found=False)
        if report:
            pdf_content, _ = report.sudo()._render_qweb_pdf([syahadah.id])
            pdfhttpheaders = [
                ('Content-Type', 'application/pdf'),
                ('Content-Length', len(pdf_content)),
                ('Content-Disposition', f'attachment; filename="Syahadah_{syahadah.name.replace("/", "_")}.pdf"')
            ]
            return request.make_response(pdf_content, headers=pdfhttpheaders)
        return request.redirect('/my/syahadah')

    @http.route(['/my/complaints'], type='http', auth="user", website=True)
    def portal_my_complaints(self, **kw):
        partner = request.env.user.partner_id
        complaints = request.env['hostel.complaint'].sudo().search([
            ('student_id', '=', partner.id)
        ], order="create_date desc") if 'hostel.complaint' in request.env else []

        values = self._prepare_portal_layout_values()
        values.update({
            'complaints': complaints,
            'page_name': 'complaint_list',
            'success_msg': kw.get('success_msg'),
            'error_msg': kw.get('error_msg'),
        })
        return request.render("sirita_mahad_portal.portal_my_complaints", values)

    @http.route(['/my/complaints/new'], type='http', auth="user", website=True)
    def portal_my_complaints_new(self, **kw):
        partner = request.env.user.partner_id
        # Dapatkan kontrak kamar aktif
        contract = request.env['hostel.contract'].sudo().search([
            ('student_id', '=', partner.id),
            ('state', '=', 'active')
        ], limit=1) if 'hostel.contract' in request.env else None

        values = self._prepare_portal_layout_values()
        values.update({
            'contract': contract,
            'page_name': 'complaint_form',
            'error_msg': kw.get('error_msg'),
        })
        return request.render("sirita_mahad_portal.portal_my_complaints_new", values)

    @http.route(['/my/complaints/submit'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def portal_my_complaints_submit(self, **post):
        partner = request.env.user.partner_id
        category = post.get('category', 'facilities')
        subject = post.get('subject')
        description = post.get('description')
        priority = post.get('priority', 'medium')
        building_id = post.get('building_id')
        room_id = post.get('room_id')

        if not (subject and description):
            return request.redirect('/my/complaints/new?error_msg=Harap+isi+judul+dan+uraian+keluhan+kerusakan.')

        try:
            complaint = request.env['hostel.complaint'].sudo().create({
                'student_id': partner.id,
                'category': category,
                'subject': subject,
                'description': description,
                'priority': priority,
                'building_id': int(building_id) if building_id else False,
                'room_id': int(room_id) if room_id else False,
                'state': 'submitted',
            })
            return request.redirect('/my/complaints?success_msg=Pengaduan+kerusakan+berhasil+dikirim+ke+pengelola.')
        except Exception as e:
            return request.redirect(f'/my/complaints/new?error_msg={quote_plus(str(e))}')

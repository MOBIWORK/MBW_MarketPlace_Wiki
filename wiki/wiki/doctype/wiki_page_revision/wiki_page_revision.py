# Copyright (c) 2020, Frappe and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import md_to_html, pretty_date
from wiki.api import get_language


class WikiPageRevision(Document):
    pass


@frappe.whitelist(allow_guest=True)
def get_revisions(wiki_page_name, lang=None):
    if not lang and frappe.session.user != "Guest":
        lang = get_language()
    lang = lang or 'vi'
    frappe.local.lang = lang
    revisions = frappe.db.get_all(
        "Wiki Page Revision",
        {"wiki_page": wiki_page_name},
        ["content", "creation", "owner", "raised_by", "raised_by_username"],
    )

    for revision in revisions:
        revision.author = revision.raised_by_username or revision.raised_by or revision.owner
        revision.content = md_to_html(revision.content)
        revision.revision_time = revision.author + ' ' + \
            _('edited') + ' ' + pretty_date(revision.creation)
        del revision.raised_by_username
        del revision.raised_by
        del revision.creation
        del revision.owner

    return revisions

# Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt


import frappe


def after_install(force=False):
	# create the wiki homepage
	page = frappe.new_doc("Wiki Page")
	page.title = "Home"
	page.route = "wiki/home"
	page.content = "Welcome to the homepage of your wiki!"
	page.published = True
	page.insert()

	# create the wiki space
	space = frappe.new_doc("Wiki Space")
	space.route = "wiki"
	space.insert()

	# create the wiki sidebar
	sidebar = frappe.new_doc("Wiki Group Item")
	sidebar.wiki_page = page.name
	sidebar.parent_label = "Wiki"
	sidebar.parent = space.name
	sidebar.parenttype = "Wiki Space"
	sidebar.parentfield = "wiki_sidebars"
	sidebar.insert()

def add_default_translate():
    translations = [
        {"source_text": "My Drafts", "translated_text": "Bản thảo của tôi", "language": "vi"},
        {"source_text": "Contributions", "translated_text": "Đóng góp", "language": "vi"},
    ]

    for entry in translations:
        if not frappe.db.exists("Translation", {"source_text": entry["source_text"], "language": entry["language"]}):
            doc = frappe.new_doc("Translation")
            doc.source_text = entry.get('source_text')
            doc.translated_text = entry.get('translated_text')
            doc.language = entry.get('language')
            doc.insert()

    frappe.db.commit()

def add_wiki_page():
    
    if frappe.db.exists("Wiki Page", {"route": "wiki/home"}):
        frappe.msgprint("🔹 Wiki Page đã tồn tại, bỏ qua.")
        return

    # Tạo Wiki Page
    page = frappe.new_doc("Wiki Page")
    page.title = "Home"
    page.route = "wiki/home"
    page.content = "Welcome to the homepage of your wiki!"
    page.published = True
    page.insert()

    space = frappe.get_value("Wiki Space", {"route": "wiki"})
    if not space:
        space = frappe.new_doc("Wiki Space")
        space.route = "wiki"
        space.insert()
    else:
        space = frappe.get_doc("Wiki Space", space)

    if not frappe.db.exists("Wiki Group Item", {"wiki_page": page.name}):
        sidebar = frappe.new_doc("Wiki Group Item")
        sidebar.wiki_page = page.name
        sidebar.parent_label = "Wiki"
        sidebar.parent = space.name
        sidebar.parenttype = "Wiki Space"
        sidebar.parentfield = "wiki_sidebars"
        sidebar.insert()

    frappe.db.commit()
# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes import _
from webnotes.utils import cint

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_update(self):
		webnotes.conn.set_default("auto_accounting_for_stock", self.doc.auto_accounting_for_stock)
		
		if self.doc.auto_accounting_for_stock:
			for wh in webnotes.conn.sql("select name from `tabWarehouse` where docstatus < 2"):
				wh_bean = webnotes.bean("Warehouse", wh[0])
				wh_bean.save()
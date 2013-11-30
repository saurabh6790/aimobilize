# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd.
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.utils import nowdate, nowtime
from accounts.utils import get_fiscal_year

def execute():
	webnotes.conn.auto_commit_on_many_writes = 1
	item_map = {}
	for item in webnotes.conn.sql("""select * from tabItem""", as_dict=1):
		item_map.setdefault(item.name, item)
	
	warehouse_map = get_warehosue_map()
	naming_series = "STE"
	
	for company, default_expense_account, cost_center in webnotes.conn.sql("select name, default_expense_account, cost_center from tabCompany"):
		stock_entry = [{
			"doctype": "Stock Entry",
			"naming_series": naming_series,
			"posting_date": nowdate(),
			"posting_time": nowtime(),
			"purpose": "Material Transfer",
			"company": company,
			"remarks": "Material Transfer to activate perpetual inventory",
			"fiscal_year": get_fiscal_year(nowdate())[0]
		}]
		stock_entry_details = []
		for bin in webnotes.conn.sql("""select * from tabBin bin where ifnull(item_code, '')!='' 
				and ifnull(warehouse, '') in (%s) and ifnull(actual_qty, 0) != 0
				and (select company from tabWarehouse where name=bin.warehouse)=%s""" %
				(', '.join(['%s']*len(warehouse_map)), '%s'), 
				(warehouse_map.keys() + [company]), as_dict=1):
			item_details = item_map[bin.item_code]
			# new_warehouse = warehouse_map[bin.warehouse].get("fixed_asset_warehouse") \
			# 	if cstr(item_details.is_asset_item) == "Yes" \
			# 	else warehouse_map[bin.warehouse].get("current_asset_warehouse")
			
			# for vence
			new_warehouse = warehouse_map[bin.warehouse].get("current_asset_warehouse") or \
				warehouse_map[bin.warehouse].get("fixed_asset_warehouse")
				
			if item_details.has_serial_no == "Yes":
				serial_no = "\n".join([d[0] for d in webnotes.conn.sql("""select name 
					from `tabSerial No` where item_code = %s and warehouse = %s 
					and status in ('Available', 'Sales Returned')""", 
					(bin.item_code, bin.warehouse))])
			else:
				serial_no = None
			
			stock_entry_details.append({
				"doctype": "Stock Entry Detail",
				"parentfield": "mtn_details",
				"s_warehouse": bin.warehouse,
				"t_warehouse": new_warehouse,
				"item_code": bin.item_code,
				"item_name": item_details.item_name,
				"description": item_details.description,
				"qty": bin.actual_qty,
				"transfer_qty": bin.actual_qty,
				"uom": item_details.stock_uom,
				"stock_uom": item_details.stock_uom,
				"conversion_factor": 1,
				"expense_account": default_expense_account,
				"cost_center": cost_center,
				"serial_no": serial_no
			})

		se = []
		for i, details in enumerate(stock_entry_details):
			se.append(details)
			if (i+1)%200==0:
				webnotes.bean(stock_entry + se).insert()
				se = []
		if len(se) > 1:
			webnotes.bean(stock_entry + se).insert()
			
	webnotes.conn.auto_commit_on_many_writes = 0
		
def get_warehosue_map():
	return {
		"Warehouse-VE-1-VEN": {
			"current_asset_warehouse": "AD-VE-MAIN-PND-1 - VEN",
			"fixed_asset_warehouse": ""
		},
		"Warehouse-VE-1-VCARE": {
			"current_asset_warehouse": "AD-VC-MAIN-PND-1 - VCARE",
			"fixed_asset_warehouse": ""
		},
		"Warehouse-VE-1-VS": {
			"current_asset_warehouse": "AD-VS-MAIN-PND-1 - VSL",
			"fixed_asset_warehouse": ""
		},
		"Warehouse-VE-1-Sollatek": {
			"current_asset_warehouse": "AD-SL-MAIN-PND-1 - SOL",
			"fixed_asset_warehouse": ""
		},
		"Warehouse-VE-1-KLOUD": {
			"current_asset_warehouse": "AD-KL-MAIN-PND-1 - KLOUDIP",
			"fixed_asset_warehouse": ""
		},
		"Stores - IEL": {
			"current_asset_warehouse": "AD-IE-MAIN-PND-1 - IEL",
			"fixed_asset_warehouse": ""
		},
		"Warehouse-VE-MODERAWILA_VEN": {
			"current_asset_warehouse": "AD-VE-MODW-PND-4 - VEN",
			"fixed_asset_warehouse": ""
		},
		"Z-OLD-Warehouse-VE-2-VEN - VEN": {
			"current_asset_warehouse": "AD-VE-MAIN-CMB-2 - VEN",
			"fixed_asset_warehouse": ""
		},
		"Warehouse-VE-2-VCARE": {
			"current_asset_warehouse": "AD-VC-MAIN-CMB-2 - VCARE",
			"fixed_asset_warehouse": ""
		},
		"Z-OLD-Warehouse-VE-2-VS - VSL": {
			"current_asset_warehouse": "AD-VS-MAIN-CMB-2 - VSL",
			"fixed_asset_warehouse": ""
		},
		"Warehouse-VE-2-Sollatek": {
			"current_asset_warehouse": "AD-SL-MAIN-CMB-2 - SOL",
			"fixed_asset_warehouse": ""
		},
		"Warehouse-VE-2 - IEL": {
			"current_asset_warehouse": "AD-IE-MAIN-CMB-2 - IEL",
			"fixed_asset_warehouse": ""
		},
		"Warehouse-VE-2-KLOUD": {
			"current_asset_warehouse": "AD-KL-MAIN-CMB-2 - KLOUDIP",
			"fixed_asset_warehouse": ""
		},
		"Unity Plaza Showroom - IEL": {
			"current_asset_warehouse": "AD-IE-UNPL-CMB-3 - IEL",
			"fixed_asset_warehouse": ""
		},
		"Unity Plaza Showroom - SOL": {
			"current_asset_warehouse": "AD-SL-UNPL-CMB-3 - SOL",
			"fixed_asset_warehouse": ""
		},
		"Unity Plaza Showroom - VEN": {
			"current_asset_warehouse": "AD-VE-UNPL-CMB-3 - VEN",
			"fixed_asset_warehouse": ""
		},
		"Display - VS": {
			"current_asset_warehouse": "AD-VS-DSPL-CMB-2  - VSL",
			"fixed_asset_warehouse": ""
		},
		"Display - VEN": {
			"current_asset_warehouse": "AD-VE-DSPL-CMB-2 - VEN",
			"fixed_asset_warehouse": ""
		},
		"Display - SOL": {
			"current_asset_warehouse": "DD-SL-DSPL-CMB-2 - SOL",
			"fixed_asset_warehouse": ""
		},
		"Stocks in Advance - CMB Technician-1-VCARE": {
			"current_asset_warehouse": "BD-VC-TEC-1-CMB-2 - VCARE",
			"fixed_asset_warehouse": ""
		},
		"Stocks in Advance - CMB Technician-2-VCARE": {
			"current_asset_warehouse": "BD-VC-TEC-2-CMB-2 - VCARE",
			"fixed_asset_warehouse": ""
		},
		"Stocks in Advance - PND Technician-1-VCARE": {
			"current_asset_warehouse": "BD-VC-TEC-1-PND-1 - VCARE",
			"fixed_asset_warehouse": ""
		},
		"Stocks in Advance - PND Technician-2-VCARE": {
			"current_asset_warehouse": "BD-VC-TEC-2-PND-1 - VCARE",
			"fixed_asset_warehouse": ""
		},
		"Stocks in Advance - PND Technician-3-VCARE": {
			"current_asset_warehouse": "BD-VC-TEC-3-PND-1 - VCARE",
			"fixed_asset_warehouse": ""
		},
		"Stocks in Advance - PND Technician-4-VCARE": {
			"current_asset_warehouse": "BD-VC-TEC-4-PND-1 - VCARE",
			"fixed_asset_warehouse": ""
		},
		"Rejected Items Warehouse - VSL": {
			"current_asset_warehouse": "ED-VS-REJT-COMN - VSL",
			"fixed_asset_warehouse": ""
		},
		"Rejected Items Warehouse - VCARE": {
			"current_asset_warehouse": "ED-VC-REJT-COMN - VCARE",
			"fixed_asset_warehouse": ""
		},
		"Rejected Items Warehouse - KLOUD": {
			"current_asset_warehouse": "ED-KL-REJT-COMN - KLOUDIP",
			"fixed_asset_warehouse": ""
		},
		"Rejected Items Warehouse - VENCE": {
			"current_asset_warehouse": "ED-VE-REJT-COMN - VEN",
			"fixed_asset_warehouse": ""
		},
		"Rejected Items Warehouse -CMB-VCARE": {
			"current_asset_warehouse": "ED-VC-REJT-CMB-2 - VCARE",
			"fixed_asset_warehouse": ""
		},
		"Rejected/Lost Items Warehouse - SOL": {
			"current_asset_warehouse": "ED-SL-REJT-COMN - SOL",
			"fixed_asset_warehouse": ""
		},
		"Standby Issued to Customer Site - VCARE": {
			"current_asset_warehouse": "DE-VC-STBY-SITE - VCARE",
			"fixed_asset_warehouse": ""
		},
		"Standby Store-VE-2-VCARE": {
			"current_asset_warehouse": "DE-VC-STBY-CMB-2 - VCARE",
			"fixed_asset_warehouse": ""
		},
		"Standby Store-VE-1-VCARE": {
			"current_asset_warehouse": "DE-VC-STBY-PND-1 - VCARE",
			"fixed_asset_warehouse": ""
		},
		"Standby Store-VE-1-VENCE-PRE MODELS": {
			"current_asset_warehouse": "DE-VE-STBY-PREM - VEN",
			"fixed_asset_warehouse": ""
		},
		"Store - Merchandize Issued to UDAYA-KLOUDIP": {
			"current_asset_warehouse": "DG-KL-ISSD-UDAYA - KLOUDIP",
			"fixed_asset_warehouse": ""
		},
		"Store - Merchandize Issued to UDAYA-VCARE": {
			"current_asset_warehouse": "DG-VC-ISSD-UDAYA - VCARE",
			"fixed_asset_warehouse": ""
		},
		"Store - Merchandize Issued to YASINTHA-VSL": {
			"current_asset_warehouse": "DG-VS-ISSD-YASIN - VSL",
			"fixed_asset_warehouse": ""
		},
		"Store - Merchandize Issued to YASINTHA-VENCE": {
			"current_asset_warehouse": "DG-VE-ISSD-YASIN - VEN",
			"fixed_asset_warehouse": ""
		},
		"Store - Merchandize Issued to YASINTHA-KLOUDIP": {
			"current_asset_warehouse": "DG-KL-ISSD-YASIN - KLOUDIP",
			"fixed_asset_warehouse": ""
		},
		"Store - Merchandize Issued to UDAYA-VSL": {
			"current_asset_warehouse": "DG-VS-ISSD-UDAYA - VSL",
			"fixed_asset_warehouse": ""
		},
		"Store - Merchandize Used for Spares-CMB-VEN": {
			"current_asset_warehouse": "DG-VE-SPAR-CMB-2 - VEN",
			"fixed_asset_warehouse": ""
		},
		"Warehouse Already Issued Spares - VCARE": {
			"current_asset_warehouse": "DG-VE-SPAR-COMN - VEN",
			"fixed_asset_warehouse": ""
		},
		"TRC Samples for Testing": {
			"current_asset_warehouse": "DG-VE-ISSD-TRCSL - VEN",
			"fixed_asset_warehouse": ""
		},
		"Work In Progress - VCARE": {
			"current_asset_warehouse": "FG-VC-WRKP-COMN - VCARE",
			"fixed_asset_warehouse": ""
		},
		"Work In Progress - IEL": {
			"current_asset_warehouse": "FG-IE-WRKP-COMN - IEL",
			"fixed_asset_warehouse": ""
		},
		"Fixed Assets - SOL": {
			"current_asset_warehouse": "",
			"fixed_asset_warehouse": "FD-SL-FIXA-CMB-2 - SOL"
		},
		"Fixed Assets - VCARE": {
			"current_asset_warehouse": "",
			"fixed_asset_warehouse": "FD-VC-FIXA-CMB-2 - VCARE"
		},
		"Fixed Assets - VEN": {
			"current_asset_warehouse": "",
			"fixed_asset_warehouse": "FD-VE-FIXA-CMB-2 - VEN"
		},
		"Fixed Assets - VSL": {
			"current_asset_warehouse": "",
			"fixed_asset_warehouse": "FD-VS-FIXA-CMB-2 - VSL"
		},
		"Fixed Assets - KLOUDIP": {
			"current_asset_warehouse": "",
			"fixed_asset_warehouse": "FD-KL-FIXA-CMB-2 - KLOUDIP"
		}}
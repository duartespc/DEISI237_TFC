import xmltodict
import io

def getItem(d):
	item = {}
	item["LineNumber"] = d["LineNumber"]
	item["ProductCode"] = d["ProductCode"]
	item["ProductDescription"] = d["ProductDescription"]
	item["Quantity"] = d["Quantity"]
	item["UnitOfMeasure"] = d["UnitOfMeasure"]
	item["UnitPrice"] = d["UnitPrice"]
	item["TaxPointDate"] = d["TaxPointDate"]
	item["Description"] = d["Description"]
	if "CreditAmount" in d:
		item["CreditAmount"] = d["CreditAmount"]
	else:
		item["CreditAmount"] = 0
	
	if "DebitAmount" in d:
		item["DebitAmount"] = d["DebitAmount"]
	else:
		item["DebitAmount"] = 0

	item["SettlementAmount"] = d["SettlementAmount"]
	item["Tax"] = {}
	item["Tax"]["TaxType"] = d["Tax"]["TaxType"]
	item["Tax"]["TaxCountryRegion"] = d["Tax"]["TaxCountryRegion"]
	item["Tax"]["TaxCode"] = d["Tax"]["TaxCode"]
	item["Tax"]["TaxPercentage"] = d["Tax"]["TaxPercentage"]
	return item

def getInvoice(invoiceDict, clientList):
	invoice = {}
	invoice["InvoiceNo"] = invoiceDict["InvoiceNo"]
	invoice["ATCUD"] = invoiceDict["ATCUD"]
	invoice["DocumentStatus"] = {}
	invoice["DocumentStatus"]["InvoiceStatus"] = invoiceDict["DocumentStatus"]["InvoiceStatus"] 
	invoice["DocumentStatus"]["InvoiceStatusDate"] = invoiceDict["DocumentStatus"]["InvoiceStatusDate"] 
	invoice["DocumentStatus"]["SourceID"] = invoiceDict["DocumentStatus"]["SourceID"] 
	invoice["DocumentStatus"]["SourceBilling"] = invoiceDict["DocumentStatus"]["SourceBilling"]
	invoice["Hash"] = invoiceDict["Hash"]
	invoice["HashControl"] = invoiceDict["HashControl"]
	invoice["InvoiceDate"] = invoiceDict["InvoiceDate"]
	invoice["InvoiceType"] = invoiceDict["InvoiceType"]
	invoice["SpecialRegimes"] = {}
	invoice["SpecialRegimes"]["SelfBillingIndicator"] = invoiceDict["SpecialRegimes"]["SelfBillingIndicator"]
	invoice["SpecialRegimes"]["CashVATSchemeIndicator"] = invoiceDict["SpecialRegimes"]["CashVATSchemeIndicator"] 
	invoice["SpecialRegimes"]["ThirdPartiesBillingIndicator"] = invoiceDict["SpecialRegimes"]["ThirdPartiesBillingIndicator"] 
	invoice["SourceID"] = invoiceDict["SourceID"]
	invoice["SystemEntryDate"] = invoiceDict["SystemEntryDate"]
	invoice["CustomerID"] = invoiceDict["CustomerID"]
	invoice["DocumentTotals"] = {}
	invoice["DocumentTotals"]["TaxPayable"] = invoiceDict["DocumentTotals"]["TaxPayable"]
	invoice["DocumentTotals"]["NetTotal"] = invoiceDict["DocumentTotals"]["NetTotal"]
	invoice["DocumentTotals"]["GrossTotal"] = invoiceDict["DocumentTotals"]["GrossTotal"]

	c = list(filter(lambda person: person['CustomerID'] == invoice["CustomerID"], clientList))

	invoice["Client"] = c[0]

	return invoice
	

def getClients(d):
	clients = []
	for client in d:
		c = {}
		c["CustomerID"] = client["CustomerID"]
		c["AccountID"] = client["AccountID"]
		c["CustomerTaxID"] = client["CustomerTaxID"]
		c["CompanyName"] = client["CompanyName"]
		c["BillingAddress"] = {}
		c["BillingAddress"] ["AddressDetail"] = client["BillingAddress"]["AddressDetail"]
		c["BillingAddress"] ["City"] = client["BillingAddress"]["City"]
		c["BillingAddress"] ["PostalCode"] = client["BillingAddress"]["PostalCode"]
		c["BillingAddress"] ["Country"] = client["BillingAddress"]["Country"]
		c["SelfBillingIndicator"] = client["SelfBillingIndicator"]
		clients.append(c)

	return clients

def getInvoices(InvoicesDict, clients):
	invoicelist = [] 
	for invoiceDict in InvoicesDict["Invoice"]:
		# discard canceled invoices
		if invoiceDict["DocumentStatus"]["InvoiceStatus"] != "N":
			continue

		# get the invoice header details
		invoice = getInvoice(invoiceDict, clients)

		# get the list of items
		invoice["items"] = []
		if isinstance(invoiceDict["Line"], list):
			for itemx in invoiceDict["Line"]:
				item = getItem(itemx)
				item["InvoiceNo"] = invoice["InvoiceNo"]
				invoice["items"].append(item)
		else:
			itemx = invoiceDict["Line"]
			item = getItem(itemx)
			item["InvoiceNo"] = invoice["InvoiceNo"]
			invoice["items"].append(item)

		invoicelist.append(invoice)
	return invoicelist


def getProducts(invoices):
	products = []
	# export products
	for i in invoices:
		if  i['InvoiceType'] != "FS":
			continue

		for it in i["items"]:
			p = {}
			p["ProductCode"] = it["ProductCode"]
			p["ProductDescription"] = it["ProductDescription"]
			p["UnitPrice"] = it["UnitPrice"]
			p["UnitOfMeasure"] = it["UnitOfMeasure"]
			p["Quantity"] = it["Quantity"]
			p["TaxPercentage"] = float(it["Tax"]["TaxPercentage"])
			
			prd = list(filter(lambda prd: prd['ProductCode'] == p["ProductCode"], products))

			if prd:
				prd[0]["Quantity"] += p["Quantity"]
			else:
				products.append(p)

	return products

def getSaft(filename):
	with io.open(filename, 'r', encoding='windows-1252') as xml_obj:
		#coverting the xml data to Python dictionary
		my_dict = xmltodict.parse(xml_obj.read())
		#closing the file
		xml_obj.close()

		Saft = {}

	Saft["NumberOfEntries"] = int(my_dict["AuditFile"]["SourceDocuments"]["SalesInvoices"]["NumberOfEntries"])
	Saft["TotalDebit"] = float(my_dict["AuditFile"]["SourceDocuments"]["SalesInvoices"]["TotalDebit"])
	Saft["TotalCredit"] = float(my_dict["AuditFile"]["SourceDocuments"]["SalesInvoices"]["TotalCredit"])
	Saft["clients"] = getClients(my_dict["AuditFile"]["MasterFiles"]["Customer"])
	Saft["invoices"] = getInvoices(my_dict["AuditFile"]["SourceDocuments"]["SalesInvoices"], Saft["clients"])
	Saft["products"] = getProducts(Saft["invoices"])

	return Saft





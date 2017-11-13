HEADERS = {
    'content-type': 'text/xml; charset=utf-8',
    'SOAPAction': 'SystemGetNodesStats'
}

BODY = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
        <s:Body>
            <ns67:SystemGetNodesStatsReq xmlns:ns67="SystemGetNodesStats" Cmd="Start" OpV="01.00.00">
            </ns67:SystemGetNodesStatsReq>
        </s:Body>
    </s:Envelope>"""

HEADERS = {
    'content-type': 'text/xml; charset=utf-8',
    'SOAPAction': 'JobGetParams'
}

BODY = """<soapenv:Envelope
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:job="JobGetParams">
        <soapenv:Body>
            <job:JobGetParamsReq Cmd="Start" OpV="01.00.00" JId="JobID"/>
        </soapenv:Body>
    </soapenv:Envelope>"""

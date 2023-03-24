


"""Platform for sensor integration."""
from __future__ import annotations

from datetime import timedelta,datetime
from distutils.command.config import config
import logging
from multiprocessing import Event
import voluptuous
import json


from barcode.writer import SVGWriter
import barcode
EAN = barcode.get_barcode_class('itf')
barcode.PROVIDED_BARCODES
import requests
from homeassistant import const
from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant import util
from homeassistant.helpers import config_validation
_LOGGER = logging.getLogger(__name__)


DEFAULT_NAME = 'Cemig'
UPDATE_FREQUENCY = timedelta(minutes=60)




def setup_platform(
    hass,
    config,
    add_entities,
    discovery_info
):
    """Set up the Copasa sensors."""
  
    add_entities([InvoiceSensor(config)])


class InvoiceSensor(SensorEntity):
    """Representation of a Cemig sensor."""

    def __init__(self,config):
        """Initialize a new Cemig sensor."""
        self._attr_name = "Cemig"
        
        

       


    @property
    def icon(self):
        """Return icon."""
        return "mdi:bank"


    @util.Throttle(UPDATE_FREQUENCY)
    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
       
        self.invoice_details = get_bills()
        
            


    @property
    def extra_state_attributes(self):
        """Return device specific state attributes."""
        self._attributes = {
            "invoice_details": self.invoice_details,
           

        }
        return  self._attributes


def get_cookie():
    url = 'https://www.atendimento.cemig.com.br/portal/api/redirect'
    headers = {
        'Content-Length': '1833',
        'Host': 'www.atendimento.cemig.com.br',
        'Origin': 'https://atende.cemig.com.br',

    }

    cookies ={
     '__Secure-next-auth.session-token':'eyJhbGciOiJIUzUxMiJ9.eyJkYXRhIjp7InVzZXIiOnsiYmFzZUFjY2Vzc0NoYW5uZWxJZCI6IlJldGFpbCIsImRvY3VtZW50IjoiMDk5LjU4Ny44MDYtNDAiLCJlbWFpbCI6Imxlb25hcmRvYWNicEBnbWFpbC5jb20iLCJpZCI6IjE5ODc3NzE3LWM0Y2EtNDQ0Ny05N2IzLTMxZWZmZWIwYjAzNCIsIm5hbWUiOiJMZW9uYXJkbyBkZSBPbGl2ZWlyYSBQaW1lbnRlbCIsInBob25lIjoiKDM3KTk5MTA4LTg1MjQiLCJwcm9maWxlUGhvdG8iOm51bGx9LCJwcm90b2NvbCI6eyJlbWFpbCI6Imxlb25hcmRvb2xpdmVpcmFwaW1lbnRlbEBob3RtYWlsLmNvbSIsImZpY3RpY2lvdXMiOmZhbHNlLCJwcm90b2NvbCI6IjI2ODU2NzcwMDciLCJwcm90b2NvbElkIjoiNDY0RTM4RjI3NDAzMUVEREIyQ0Q3NEU5MEM2RjE2RkMiLCJzZWdtZW50IjoiVmFyZWpvIiwidHlwZSI6IlBGIiwidXNlckJ1c2luZXNzUGFydG5lciI6IjcyMDAxNDMyMjUiLCJzaXRlQnVzaW5lc3NQYXJ0bmVyIjoiNzIwMDE0MzIyNSJ9LCJjb2V4aXN0ZW5jZSI6dHJ1ZSwibWVzc2FnZUZpbmFsU2VydmljZSI6IiIsInRva2VuIjp7ImFjY2Vzc1Rva2VuIjoiZXlKaGJHY2lPaUpTVXpJMU5pSXNJblI1Y0NJZ09pQWlTbGRVSWl3aWEybGtJaUE2SUNKYU5ETktWa0ZaVFhsRGVtVnBabE54VEdOVVdHSXRRMnBWUldvMGVGWmZiMkU1VEVKalZreHNjMDlSSW4wLmV5SmxlSEFpT2pFMk56azJPRGN4TWpRc0ltbGhkQ0k2TVRZM09UWTNPVGt5TkN3aWFuUnBJam9pTTJFeVpEWXlNVGd0WlRrNU5TMDBNelZqTFRrMk9EVXRaRE5qWlRJeVlUSTRNVGc0SWl3aWFYTnpJam9pYUhSMGNEb3ZMMk5sYldsbkxXdGxlV05zYjJGckxtUmxabUYxYkhRdWMzWmpMbU5zZFhOMFpYSXViRzlqWVd3Nk9EQTRNQzlyWlhsamJHOWhheTloZFhSb0wzSmxZV3h0Y3k5alpXMXBaeTF3Y205a0lpd2lZWFZrSWpvaVlXTmpiM1Z1ZENJc0luTjFZaUk2SWpFNU9EYzNOekUzTFdNMFkyRXRORFEwTnkwNU4ySXpMVE14WldabVpXSXdZakF6TkNJc0luUjVjQ0k2SWtKbFlYSmxjaUlzSW1GNmNDSTZJbU5sYldsbkxYQnliMlF0YzJWeWRtbGpaU0lzSW5ObGMzTnBiMjVmYzNSaGRHVWlPaUpsTmpobE5EUmhPQzB5T1RKbUxUUmxNVE10WVRVeE55MWlNakF5WlRFeU5qUTFNellpTENKaFkzSWlPaUl4SWl3aVlXeHNiM2RsWkMxdmNtbG5hVzV6SWpwYklpOHFJbDBzSW5KbFlXeHRYMkZqWTJWemN5STZleUp5YjJ4bGN5STZXeUp2Wm1ac2FXNWxYMkZqWTJWemN5SXNJblZ0WVY5aGRYUm9iM0pwZW1GMGFXOXVJaXdpWkdWbVlYVnNkQzF5YjJ4bGN5MWpaVzFwWnlKZGZTd2ljbVZ6YjNWeVkyVmZZV05qWlhOeklqcDdJbUZqWTI5MWJuUWlPbnNpY205c1pYTWlPbHNpYldGdVlXZGxMV0ZqWTI5MWJuUWlMQ0p0WVc1aFoyVXRZV05qYjNWdWRDMXNhVzVyY3lJc0luWnBaWGN0Y0hKdlptbHNaU0pkZlgwc0luTmpiM0JsSWpvaWNISnZabWxzWlNCbGJXRnBiQ0lzSW5OcFpDSTZJbVUyT0dVME5HRTRMVEk1TW1ZdE5HVXhNeTFoTlRFM0xXSXlNREpsTVRJMk5EVXpOaUlzSW1WdFlXbHNYM1psY21sbWFXVmtJanBtWVd4elpTd2lkWE5sY2w5aWRYTnBibVZ6YzE5d1lYSjBibVZ5SWpvaU56SXdNREUwTXpJeU5TSXNJbTVoYldVaU9pSk1aVzl1WVhKa2J5QmtaU0JQYkdsMlpXbHlZU0JRYVcxbGJuUmxiQ0lzSW5CeVpXWmxjbkpsWkY5MWMyVnlibUZ0WlNJNklqTTJNamczTURnaUxDSm5hWFpsYmw5dVlXMWxJam9pVEdWdmJtRnlaRzhpTENKbVlXMXBiSGxmYm1GdFpTSTZJbVJsSUU5c2FYWmxhWEpoSUZCcGJXVnVkR1ZzSWl3aVpXMWhhV3dpT2lKc1pXOXVZWEprYjJGalluQkFaMjFoYVd3dVkyOXRJbjAuVDlnSVRyakhzZ25mNmtPemEtalNHcVNaQ0Jqc3A2Zkdwb05Yb0tMX094SFVLeHhoQTBGSks1MGFsSmlYdFJhaGVvZDBJSFk0RTRsUVh4aDVJTGVJRkl6M2N2eUhmTFVGVDk1aEg2VnhjUXVCQWRfb1dreHRtMHlEVHpBZHZ0VjhpOGtnemVGb01EQkstR2F2OFdMVlZBci1HY1U0dHNwSEEzdzVpQ2ZuR1ZqNm5INmkyNTUycFhaT3lyd0FKT3VYeU5kUTV4TzR0ajZmclB0cXAxTTFqRkVrUDY2RFJDVTNIbXlPR19KNkg0SzI3aWdwU0FVLVRxMzExOXg3aTRoSWd3c1pIdGdHZHdzbEczVVduWGZJYndhd1h1T2NkYkxnZ2xHQ0pNdEN0NFEta1dtckV1aWtGcGNza1JNZnRBS1QydGVYYXpaSF9IaVhaY2Z1a2VyRGhRIn0sImV4dHJhcyI6eyJzaXRlTnVtYmVyIjoiMzAxMjI2NDA2MyIsImNvbnRyYWN0IjoiNTAxMjgwNTY0MyIsImNvbnRyYWN0QWNjb3VudCI6IjAwODAzOTI0OTQ4MCJ9fSwicHJvdmlkZXIiOnsiaWQiOiJjcmVkZW50aWFscyIsIm5hbWUiOiJjcmVkZW50aWFscyJ9LCJpYXQiOjE2Nzk2Nzk5ODQsImV4cCI6MTY4MjI3MTk4NH0.2Cl4V7dkB5eHJTkX4wXQPjpRBZQypN8lexklJ8uYi6XlBlpY_V95Z3MqESuT6EXKDGVP8NwdhL31yfKe3cH5fg',
     'OptanonAlertBoxClosed':'2022-09-28T15:14:34.737Z',
     '_ga_WQ0B2G17B0': 'GS1.1.1664378066.1.1.1664378486.0.0.0',
     '_ga':'GA1.3.2019388251.1664378067',
     'OptanonConsent':'isIABGlobal=false&datestamp=Wed+Sep+28+2022+12%3A21%3A31+GMT-0300+(Hor%C3%A1rio+Padr%C3%A3o+de+Bras%C3%ADlia)&version=6.36.0&hosts=&consentId=6947143c-9173-4df4-a343-62f0ca7a8f98&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=BR%3BMG&AwaitingReconsent=false; _hjSessionUser_2262372=eyJpZCI6IjhhZDQ3ZmZiLTRkZTQtNTEzMC1iNTA1LTY5MjkxYjYwMmNkZCIsImNyZWF0ZWQiOjE2NjQzNzgwNjkzNTAsImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.3.1077189169.1679567710'}

    data = {
    'accessToken': 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJaNDNKVkFZTXlDemVpZlNxTGNUWGItQ2pVRWo0eFZfb2E5TEJjVkxsc09RIn0.eyJleHAiOjE2Nzk2ODcyNzgsImlhdCI6MTY3OTY4MDA3OCwianRpIjoiOTEzYjNiMGEtNDEyNS00ZWI3LTg0YmYtOWFkMTY2M2Y0NmY5IiwiaXNzIjoiaHR0cDovL2NlbWlnLWtleWNsb2FrLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWw6ODA4MC9rZXljbG9hay9hdXRoL3JlYWxtcy9jZW1pZy1wcm9kIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6IjE5ODc3NzE3LWM0Y2EtNDQ0Ny05N2IzLTMxZWZmZWIwYjAzNCIsInR5cCI6IkJlYXJlciIsImF6cCI6ImNlbWlnLXByb2Qtc2VydmljZSIsInNlc3Npb25fc3RhdGUiOiI5NTkyM2M2My0wNTM1LTRkN2UtOWI3ZC0yNTcwMjJkY2FjOWUiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIi8qIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIiwiZGVmYXVsdC1yb2xlcy1jZW1pZyJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoicHJvZmlsZSBlbWFpbCIsInNpZCI6Ijk1OTIzYzYzLTA1MzUtNGQ3ZS05YjdkLTI1NzAyMmRjYWM5ZSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwidXNlcl9idXNpbmVzc19wYXJ0bmVyIjoiNzIwMDE0MzIyNSIsIm5hbWUiOiJMZW9uYXJkbyBkZSBPbGl2ZWlyYSBQaW1lbnRlbCIsInByZWZlcnJlZF91c2VybmFtZSI6IjM2Mjg3MDgiLCJnaXZlbl9uYW1lIjoiTGVvbmFyZG8iLCJmYW1pbHlfbmFtZSI6ImRlIE9saXZlaXJhIFBpbWVudGVsIiwiZW1haWwiOiJsZW9uYXJkb2FjYnBAZ21haWwuY29tIn0.dIkU8KqNNV_AWm0w5GxPZl8W3N3Swu5MGbjjGeoD_xb5kvWlQbVYmaVKUWzwdu-CllogbGq4exnleZwXLAxQrY0GR44rfXr514tOC0TL2GeMVzb1w4-8GyuAtcWwcdFvEXrAyUemxjU_4gqXDLcHP9y47EL0TSvdMk3AwB6_ZLfvdhZKdBt3Kv_xL7LceepxwqyTx7Sk4NzqB0bKBDU87b8OwoNZo95mS6tbw25gybeKyThAgoryjZ7HlOh51D9yOdydsnibtsfHwSRBZLDP5G3nsT-YXw5wazbiXSOdfgyTKmp7DuuwyihJUW7eRHMQbLiLModnxTuJWZqfDU3B5g',
    'protocol': '2685629275',
    'protocolId': '464E38F274031EDDB2CB389E9C4015E9',
    'possuiDebitos': '',
    'siteBusinessPartner': '7200143225',
    'siteNumber': '3012264063',
    'contract': '5012805643',
    'contractAccount': '008039249480',
    'messageFinalService': '',
    'ExecutedServiceId': '0',
    'ExecutedServiceName': ''
    }

    response = requests.post(url,cookies=cookies, headers=headers, data=data,allow_redirects=False)
    headers = response.headers['Set-Cookie']
    cookies = headers.split('; ')
    cookies= cookies[0].replace('__Secure-next-auth.session-token=','')
    return cookies


def get_token():
    cookies = get_cookie()
    url = 'https://www.atendimento.cemig.com.br/portal/api/auth/session'

    headers = {
        'Host': 'www.atendimento.cemig.com.br',
        'Referer': 'https://www.atendimento.cemig.com.br/portal/home',
    }

    cookies = {
        '__Secure-next-auth.session-token': cookies
    }

    response = requests.get(url, headers=headers, cookies=cookies)

    headers = response.headers.get('Set-Cookie')
    cookies = headers.split(', ')

    for cookie in cookies:
        # Separar o nome e valor do cookie
        name_value = cookie.split(',')[0].split('=')
        name = name_value[0]
        value = name_value[1]

        # Inicializar o dicionário para armazenar as informações do cookie
        cookie_dict = {'name': name, 'value': value}

        if '__Secure-next-auth.session-token' in name:
            session_token = cookie_dict['value']
            accessToken = session_token
    invoice_details = json.loads(response.text)
    data= invoice_details['data']

    return data


def get_bills():

    url = "https://www.atendimento.cemig.com.br/graphql"
    token = get_token()
    protocol = token['protocol']['protocol']
    accessToken= token['token']['accessToken']
    protocolId =token['protocol']['protocolId']
    userBusinessPartner = token['protocol']['userBusinessPartner']
    siteBusinessPartner = token['protocol']['siteBusinessPartner']
    
    headers = CaseInsensitiveDict()
    headers["Host"] = "www.atendimento.cemig.com.br"
    headers["User-Business-Partner"] = userBusinessPartner
    headers["Protocol-Type"] = "PF"
    headers["Authorization"] = f"Bearer {accessToken}"
    headers["Protocol-Id"] = protocolId
    headers["Content-Type"] = "application/json"
    headers["Protocol"] = protocol
    headers["Channel"] = "AGV"
    headers["Site-Business-Partner"] = siteBusinessPartner
    headers["Referer"] = "https://www.atendimento.cemig.com.br/portal/bills/duplicate-bill/details"

    data = '{"operationName":"BillsDetails","variables":{"billsDetailsInput":{"siteId":"a7ca84d5-5d88-f72b-f21f-5dd569050e79","billIdentifier":"666015428493"}},"query":"query BillsDetails($billsDetailsInput: BillDetailsInputDTO!) { billDetails(input: $billsDetailsInput) { bills { value consumption barCode pix compostion { description value percentValue } billIdentifier dueDate referenceMonth comparativeBoard { period readingType billableDays installment fine otherValues streetLighting dailyConsumption monthlyConsumption icms compensations fees restitutions class billableDaysThreeMonths installmentThreeMonths fineThreeMonths otherValuesThreeMonths streetLightingThreeMonths dailyConsumptionThreeMonths monthlyConsumptionThreeMonths icmsThreeMonths compensationsThreeMonths feesThreeMonths restitutionsMonths classThreeMonths } billingData { price description quantity amount } comparativeInfos { description value valueLastThreeMonths comparative classComparative { actual previous } details { monthYearReference text } } } } }"}'

    response = requests.post(url, headers=headers, data=data)
    invoice_details = json.loads(response.content)
 
   
    
    total = invoice_details['data']['billDetails']['bills'][0]['value']
    price = invoice_details['data']['billDetails']['bills'][0]['billingData'][0]['price']
    billIdentifier =  invoice_details['data']['billDetails']['bills'][0]['billIdentifier']
    consumption = invoice_details['data']['billDetails']['bills'][0]['consumption']
    pix = invoice_details['data']['billDetails']['bills'][0]['pix']
    dueDate = invoice_details['data']['billDetails']['bills'][0]['dueDate']
    referenceMonth = invoice_details['data']['billDetails']['bills'][0]['referenceMonth']
    result={'billIdentifier':billIdentifier,'total':total,'price':price,'consumption':consumption,'pix':pix,'dueDate':dueDate,'referenceMonth':referenceMonth}
    
    return result

      
    
    







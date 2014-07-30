import sys
import netrc
import logging
from datetime import datetime
from tempfile import NamedTemporaryFile
from subprocess import check_call, PIPE

import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_date

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)


class PayCheckRecords(object):

    ROOT_URL = "https://www.paycheckrecords.com"

    def __init__(self):
        self.session = requests.Session()

    def login(self, user, password):
        response = self.session.get(self.ROOT_URL + "/login.jsp")
        assert response.status_code == 200
        soup = BeautifulSoup(response.text)

        data = {
            'userStrId': user,
            'password': password,
            'loginNow': "1",
            'employeeSiteLogin': "1",
            'ProfileExclude': "password",
            'Login.x': "20",
            'Login.y': "6",
            'hss': "1",
        }

        response = self.session.post(
            self.ROOT_URL + "/login/iamLogin.jsp",
            data,
            allow_redirects=False
        )
        assert response.status_code == 302
        assert response.headers['location'] == self.ROOT_URL + "/default.jsp"


    def get_paycheck_list(self, start_date, end_date):
        data = {
            'startDate': start_date.strftime("%m/%d/%Y"),
            'endDate': end_date.strftime("%m/%d/%Y"),
        }
        response = self.session.post(self.ROOT_URL + "/in/paychecks.jsp", data)
        assert "Log Out" in response.text
        soup = BeautifulSoup(response.text)

        report = soup.find('table', {'class': 'report'})
        trs = report.find_all('tr')
        header = trs[0]
        for tr in trs[1:]:
            paycheck = {}
            tds = tr.find_all('td')
            paycheck['date'] = parse_date(tds[0].text.strip())
            paycheck['total'] = tds[1].text
            paycheck['net'] = tds[2].text
            printer_html_path = tds[0].a['href']
            paycheck['url'] = self.ROOT_URL + printer_html_path
            yield paycheck


def to_pdf(html, pdfpath):
    """Convert html text to a PDF file"""
    html_file = NamedTemporaryFile(suffix='.html')
    html_file.write(html)
    html_file.flush()
    check_call(['wkhtmltopdf', html_file.name, pdfpath], stderr=PIPE)
    html_file.close()


def download_paychecks(pcr, paychecks):
    """Use the existing pcr session to download the paychecks as PDFs"""
    for paycheck in paychecks:
        logger.debug("downloading %r", paycheck)
        response = pcr.session.get(paycheck['url'])
        pdfpath = "paycheck_%s.pdf" % paycheck['date'].strftime("%Y-%m-%d")
        to_pdf(response.text, pdfpath)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    logging.basicConfig()
    try:
        start_date = parse_date(argv[1])
        end_date = parse_date(argv[2])
    except IndexError:
        year = datetime.now().year
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
    user, _ , password = netrc.netrc().authenticators("paycheckrecords.com")
    pcr = PayCheckRecords()
    pcr.login(user, password)
    paychecks = pcr.get_paycheck_list(start_date, end_date)
    download_paychecks(pcr, paychecks)


if __name__ == '__main__':
    sys.exit(main())

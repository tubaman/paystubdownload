# paystubdownload

This a little script to download paystubs from
[https://www.paycheckrecords.com](https://www.paycheckrecords.com).
You can use pip to install all the dependencies and you'll also need
wkhtmltopdf.  Here are the steps to get it working on Debian-based Linux:
   * mkvirtualenv paystubdownload
   * working paystubdownload
   * pip install -r requirements.txt
   * sudo apt-get install wkhtmltopdf
   * python downloadpaystubs.py

## TODO
   * split out the scraper into it's own library

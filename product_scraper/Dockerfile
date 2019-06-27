FROM python:3
COPY . product_scraper
RUN pip install -r product_scraper/requirements.txt
WORKDIR "product_scraper"
CMD ["nohup", "python", "scraper.py", "&", ">/dev/null"]
FROM python:3.7.3
COPY . product_api
RUN pip install -r product_api/requirements.txt
WORKDIR "product_api"
CMD ["./start.sh"]
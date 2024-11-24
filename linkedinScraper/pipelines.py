# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, inspect
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import CloseSpider
import logging

class LinkedinscraperPipeline:

    settings = get_project_settings()
    meta = MetaData()


    def open_spider(self, spider):
        logging.debug("open_spider -- spider is opened")
        sql_connection_string = self.settings.get("SQL_CONNECTION_STRING")
        table_name = self.settings.get("TABLE_NAME")
        if table_name is None:
            table_name = "linkedin_profiles"
        if sql_connection_string is None:
            sql_connection_string = "sqlite:///linkedin.db"
        self.conn = create_engine(sql_connection_string)
        try:
            self.conn.connect()
        except:
            raise CloseSpider("Unable to connect to database")
        logging.debug(f"open_spider -- {table_name} {sql_connection_string}")
        self.tbl = Table(
            table_name, self.meta,
            Column("Id", Integer, primary_key=True, autoincrement=True),
            Column("Date", String),
            Column("Time", String),
            Column("Name", String),
            Column("Designation", String),
            Column("Organisation", String),
            Column("Description", String),
            Column("ProfileUrl", String),
            Column("Query", String),
            Column("Page", Integer),
        )
        if not inspect(self.conn).has_table(table_name):
            logging.debug("Table does not exists creating table")
            self.meta.create_all(self.conn)

    def process_item(self, item, spider):
        self.conn.execute(self.tbl.insert(item))
        # logging.debug(f"inserted {item}")
        return item

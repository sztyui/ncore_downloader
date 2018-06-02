#!/usr/bin/env python3
# -*- coding=iso-8859-2 -*-

# SQL Connection Interface

import os
import sqlite3
import datetime


sample = {'link': 'https://ncore.cc/torrents.php?action=details&id=2162131', 'cim': 'Szulejmán S04E28', 'datum': datetime.datetime(2017, 8, 30, 23, 32, 45)}

class DB(object):
	"SQLlite3 database implementation."
	
	__database__ = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ncore_download.db")
	__table_name = "utolso"
	def __init__(self):
		"Database initialization."
		already = True if os.path.isfile(self.__database__) else False

		self.__conn__ = sqlite3.connect(self.__database__)
		cur = self.__conn__.cursor()

		if not already:
			cur.execute("CREATE TABLE {0} (name text, date text, link text)".format(self.__table_name))
			self.__conn__.commit()

	@staticmethod
	def __field_check(**kwargs):
		if not "link" in kwargs:
			raise AttributeError("Nincsen link mezo.")
		if not "cim" in kwargs:
			raise AttributeError("Nincs cim mezo.")
		if not "datum" in kwargs:
			raise AttributeError("Nincs datum mezo.")

	def add(self, *args, **kwargs):
		"Add something to the database.\
		Structure: {cim, datum, link}"
		self.__field_check(**kwargs)	# Mezok ellenorzese.
		cur = self.__conn__.cursor()
		cur.execute("INSERT INTO {tabname} VALUES ('{cim}', '{date}', '{link}')".format(
				tabname=self.__table_name,
				cim=kwargs.get("cim"),
				date=kwargs.get("datum").isoformat(),
				link=kwargs.get("link")
			))

	def commit(self):
		self.__conn__.commit()

	def __del__(self):
		if self.__conn__:
			self.__conn__.rollback()
			self.__conn__.close()

	def contains(self, *args, **kwargs):
		self.__field_check(**kwargs)
		cursor = self.__conn__.cursor()
		val = cursor.execute(
			"SELECT * FROM {tabname} WHERE link = '{link}'".format(
					tabname=self.__table_name,
					link=kwargs.get("link")
				)).fetchone()
		if not val is None:
			return True
		else: return False
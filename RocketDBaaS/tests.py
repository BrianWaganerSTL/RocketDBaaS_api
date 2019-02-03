from unittest import TestCase

from RocketDBaaS.settings import uiUrl, MINION_PORT, LOGGING, DATABASES, SECRET_KEY, emailFromPostgres, emailCcPostgres, replyToPostgres, emailFromMongo, emailCcMongo, replyToMongo


class TestSetting(TestCase):

  def test_uiUrl(self):
    self.assertTrue((uiUrl != None and uiUrl != ''), msg='uiUrl must be set in settings_local.py file')

  def test_MINION_PORT(self):
    self.assertTrue((MINION_PORT != None and MINION_PORT != ''), msg='MINION_PORT must be set in settings_local.py file')

  def test_LOGGING(self):
    self.assertTrue((LOGGING != None and LOGGING != ''), msg='LOGGING must be set in settings_local.py file')

  def test_DATABASES(self):
    self.assertTrue((DATABASES != None and DATABASES != ''), msg='DATABASES must be set in settings_local.py file')

  def test_SECRET_KEY(self):
    self.assertTrue((SECRET_KEY != None and SECRET_KEY != ''), msg='SECRET_KEY must be set in settings_local.py file')

  def test_emailFromPostgres(self):
    self.assertTrue((emailFromPostgres != None and emailFromPostgres != ''), msg='emailFromPostgres must be set in settings_local.py file')

  def test_emailCcPostgres(self):
    self.assertTrue((emailCcPostgres != None and emailCcPostgres != ''), msg='emailCcPostgres must be set in settings_local.py file')

  def test_replyToPostgres(self):
    self.assertTrue((replyToPostgres != None and replyToPostgres != ''), msg='replyToPostgres must be set in settings_local.py file')

  def test_emailFromMongo(self):
    self.assertTrue((emailFromMongo != None and emailFromMongo != ''), msg='emailFromMongo must be set in settings_local.py file')

  def test_emailCcMongo(self):
    self.assertTrue((emailCcMongo != None and emailCcMongo != ''), msg='emailCcMongo must be set in settings_local.py file')

  def test_replyToMongo(self):
    self.assertTrue((replyToMongo != None and replyToMongo != ''), msg='replyToMongo must be set in settings_local.py file')

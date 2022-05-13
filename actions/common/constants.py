from typing import Text

class Constant:
    def __init__(self):
        self.drupal_base_url = "http://ec2-3-112-43-170.ap-northeast-1.compute.amazonaws.com"
        self.drupal_basic_auth_username = "admin"
        self.drupal_basic_auth_password = "P@ssw0rd!"

        self.bpm_base_url = "http://ec2-3-112-43-170.ap-northeast-1.compute.amazonaws.com:7080"
        self.bpm_basic_auth_username = "admin"
        self.bpm_basic_auth_password = "test"

    def get_drupal_base_url(self) -> Text:
        return self.drupal_base_url

    def get_drupal_basic_auth_username(self) -> Text:
        return self.drupal_basic_auth_username

    def get_drupal_basic_auth_password(self) -> Text:
        return self.drupal_basic_auth_password

    def get_bpm_base_url(self) -> Text:
        return self.bpm_base_url

    def get_bpm_basic_auth_username(self) -> Text:
        return self.bpm_basic_auth_username

    def get_bpm_basic_auth_password(self) -> Text:
        return self.bpm_basic_auth_password

    def get_datetime_format_YYYYMMDD_1(self) -> Text:
        return '%Y-%m-%d'
from argparse import Action
import datetime
import logging
import re

from typing import Dict, Text, Any, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict

from rasa_sdk.forms import FormAction
import requests

from actions.service.irgl_service import IrglService
from actions.common.constants import Constant

logger = logging.getLogger(__name__)
irglService = IrglService()
const = Constant()



class AskForSlotAction_Country(Action):
    def name(self) -> Text:
        return "action_ask_ac_country"

    def get_country(self):
        r = requests.get('http://localhost:5555/country')

        resp_dict = r.json()
        print(f"receipt method: {resp_dict}")
        return resp_dict

    def run( self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        data = []
        res = self.get_country()
        for k, v in res.items():  data.append( {"title": v, "payload":  k} )
        print(data)

        message={"payload":"quickReplies","data":data}
        dispatcher.utter_message(text="居住国を選択してください",json_message=message)

        return []


class AskForSlotAction(Action):
    def name(self) -> Text:
        return "action_ask_ac_receipt_method"

    def get_receipts(self):
        r = requests.get('http://localhost:5555/receipt_types')

        # print(f"statusCode: {r.status_code}")
        # print(r.text)
        resp_dict = r.json()
        print(f"receipt method: {resp_dict}")
        # for key in resp_dict:  print(f"{key}: {resp_dict[key]}")
        return resp_dict


    def run( self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        data = []
        res = self.get_receipts()
        for k, v in res.items():  data.append( {"title": v, "payload":  k} )
        print(data)

        # data= [ { "title":"chip1", "payload":"chip1_payload" }, { "title":"chip2", "payload":"chip2_payload" }, { "title":"chip3", "payload":"chip3_payload" } ]
        message={"payload":"quickReplies","data":data}
        dispatcher.utter_message(text="受取手段を選択して下さい",json_message=message)

        return []


class ValidateAcForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_ac_form"
    
    def check(self, email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, email)):
            print(f"Valid Email: {email}")
            return True
        else:
            print("Invalid Email: {email}")
            return False


    def validate_ac_mail(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict, ) -> Dict[Text, Any]:
        """Validate `mail` value."""

        # If the name is super short, it might be wrong.
        print(f"mail address = {slot_value} length = {len(slot_value)}")
        logger.debug(">>>>> check mail addr input")

        if not self.check(slot_value):
            dispatcher.utter_message(text=f"メールアドレスが正しくないです")
            return {"ac_mail": None}
        else:
            return {"ac_mail": slot_value}


class ValidateAuthForm(FormValidationAction):
    """Example of a form validation action."""

    def name(self) -> Text:
        return "validate_auth_form"

    @staticmethod
    def is_int(string: Text) -> bool:
        try:
            int(string)
            return True
        except ValueError:   return False

    def validate_auth_name(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict,) -> Dict[Text, Any]:

        print(f">>>>> check user name input. auth name: {slot_value}")
        p = re.compile('[\u30A1-\u30FF]+')
        res = p.fullmatch(slot_value)

        if  not res:
            dispatcher.utter_message(text=f"入力不正：全角カタカナ")
            return {"auth_name": None}
        else:
            return {"auth_name": slot_value}

    def validate_auth_numpeople(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any],) -> Dict[Text, Any]:
        """Validate num_people value."""

        if self.is_int(value) and int(value) > 0:
            return {"auth_numpeople": value}
        else:
            dispatcher.utter_message(response="utter_wrong_auth_numpeople")
            return {"auth_numpeople": None}

    def validate_auth_fnumber(self, slot_value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict,) -> Dict[Text, Any]:

        if len(slot_value) <= 2:
            dispatcher.utter_message(response="utter_wrong_auth_fnumber")
            return {"auth_fnumber": None}
        else:
            return {"auth_fnumber": slot_value}

    def validate_auth_fdate(self, slot_value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict,) -> Dict[Text, Any]:
        pattern = r'[12]\d{3}[/\-年](0?[1-9]|1[0-2])[/\-月](0?[1-9]|[12][0-9]|3[01])日?$'
        
        print(slot_value)
        print(type(slot_value))
        print(f">>>>>>>>>>")
        prog = re.compile(pattern)
        result = prog.match(slot_value)
        
        if result: print(result.group())

        if not result:
            dispatcher.utter_message(response="搭乗日の入力が不正です")
            return {"auth_fdate": None}
        else:
            return {"auth_fdate": slot_value}

    def validate_auth_applyid(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict,) -> Dict[Text, Any]:

        if len(slot_value) <= 2:
            dispatcher.utter_message(response="utter_wrong_auth_applyid")
            return {"auth_applyid": None}
        else:
            return {"auth_applyid": slot_value}



class irglReimburseApplyForm(FormAction):

    def name(self) -> Text:
        return "irgl_reimburse_apply_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        logger.debug("============debug required_slots is running")

        irgl_required_slots = [
            "irgl_slot_flight_dep_date",       # 出発日付
            "irgl_slot_flight_code",           # 空港便番号
            "irgl_slot_passenger_seat_number", # 搭乗者座席番号
            "irgl_slot_passenger_name",        # 搭乗者名
            "irgl_slot_reimburse_item",        # 補償内容
            "irgl_slot_voucher_confirm",       # 証憑確認
            ]

        return irgl_required_slots

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            # 出発日付
            "irgl_slot_flight_dep_date": [ 
                self.from_entity(entity="cmn_entity_date", intent=["irgl_reimburse_apply_info"]),
            ],
            # 空港便番号
            "irgl_slot_flight_code": [ 
                self.from_entity(entity="irgl_entity_flight_code", intent=["irgl_reimburse_apply_info"]),
            ],
            # 搭乗者座席番号
            "irgl_slot_passenger_seat_number": [ 
                self.from_entity(entity="irgl_entity_flight_seat_number", intent=["irgl_reimburse_apply_info"]),
            ],
            # 搭乗者名
             "irgl_slot_passenger_name": [
                self.from_text(),
            ],
            # 補償内容
            "irgl_slot_reimburse_item": [ 
                self.from_entity(entity="cmn_entity_number", intent=["irgl_reimburse_apply_info"]),
            ],
            # 証憑確認
            "irgl_slot_voucher_confirm": [ 
                self.from_entity(entity="cmn_entity_number", intent=["irgl_reimburse_apply_info"]),
            ],
        }


    def dataTimeStrAddZero(dataStr: Text, formateStr: Text) -> Text:
        dt = datetime.datetime.strptime(dataStr,formateStr)
        return dt.strftime(formateStr)

    def validate_irgl_slot_flight_dep_date(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        formatedValue = self.dataTimeStrAddZero(value, const.get_datetime_format_YYYYMMDD_1())
        return{"irgl_slot_flight_dep_date": formatedValue}

    def validate_irgl_slot_flight_code(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        
        departureDate = tracker.get_slot('irgl_slot_flight_dep_date')
        irglEventInfo = irglService.get_irgl_event_info(flightCode=value, departureDate=departureDate)

        # IRGL事象が存在しない場合
        if not irglEventInfo:
            dispatcher.utter_message(template="utter_common_wrong_irgl_info")
            return{
                "irgl_slot_flight_dep_date": None,
                "irgl_slot_flight_code": None
            }
        # IRGL事象が存在の場合
        else:
            return{"irgl_slot_flight_code": value, "irgl_slot_event_type": irglEventInfo['field_irgl_event_type']}

    def validate_irgl_slot_passenger_name(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        departureDate = tracker.get_slot('irgl_slot_flight_dep_date')
        flightCode = tracker.get_slot('irgl_slot_flight_code')
        seatNumber = tracker.get_slot('irgl_slot_passenger_seat_number')
        irglPassengerInfo = irglService.get_irgl_passenger_info(flightCode=flightCode, 
            departureDate=departureDate, seatNumber=seatNumber, passengerName=value)

        # IRGL搭乗者情報が存在しない場合
        if not irglPassengerInfo:
            dispatcher.utter_message(template="utter_common_wrong_irgl_info")
            return{
                "irgl_slot_passenger_seat_number": None,
                "irgl_slot_passenger_name": None
            }
        # IRGL搭乗者情報がが存在の場合
        else:
            dispatcher.utter_message(template="utter_response_irgl_reimburse_target_ok")
            return{"irgl_slot_passenger_name": value}

    def validate_irgl_slot_reimburse_item( self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any],) -> Dict[Text, Any]:

        convertedValue = None
        if int(value) == 1:
           convertedValue = "交通費／宿泊費"
        elif int(value) == 2:
            convertedValue = "飲食費"
        elif int(value) == 3:
            convertedValue = "その他"

        return{"irgl_slot_reimburse_item": convertedValue}

    def validate_irgl_slot_voucher_confirm(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any],) -> Dict[Text, Any]:

        convertedValue = None
        if int(value) == 1:
            convertedValue = "あり"
        elif int(value) == 2:
            convertedValue = "なし"

        if not convertedValue:
            return{"irgl_slot_voucher_confirm": None}

        # IRGL補償申請審査
        reviewResult = irglService.review_apply_info(
            flightCode=tracker.get_slot('irgl_slot_flight_code'),
            departureDate=tracker.get_slot('irgl_slot_flight_dep_date'),
            seatNumber=tracker.get_slot('irgl_slot_passenger_seat_number'),
            reimburseItem=tracker.get_slot('irgl_slot_reimburse_item'),
            voucherConfirm=convertedValue,
        )

        return{
            "irgl_slot_voucher_confirm": convertedValue, 
            "irgl_slot_reimburse_review_result": reviewResult['review_result'],
            "irgl_slot_reimburse_amount": reviewResult['amount']
            }

    def submit( self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any],) -> List[Dict]:
        reviewResult = tracker.get_slot('irgl_slot_reimburse_review_result')

        if reviewResult == 'NG':
            dispatcher.utter_message(template="utter_response_irgl_reimburse_apply_result_ng")
        elif reviewResult == 'OK':
            dispatcher.utter_message(template="utter_response_irgl_reimburse_apply_result_ok", 
                reimburse_amount=tracker.get_slot('irgl_slot_reimburse_amount'))

        return []
      
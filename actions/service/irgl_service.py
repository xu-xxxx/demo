import json, requests
from typing import Text, Dict
from actions.common.constants import Constant

const = Constant()

class IrglService:

    def get_receipts():
        headers = {'Content-type': 'application/json'}
        r = requests.get('http://localhost:5555/receipt_types')

        print(f"statusCode: {r.status_code}")
        resp_dict = r.json()
        for key in resp_dict:  print(f"{key}: {resp_dict[key]}")
        return resp_dict

    def postData(url, data, username, password): 
        headers = {'Content-type': 'application/json'}
        response = requests.post(url=url, data=json.dumps(data), headers=headers, auth=(username, password))
        # response = requests.post(url, data)
        return response

    def getData(url, username, password):
        headers = {'Content-type': 'application/json'}
        response = requests.get(url=url,  auth=(username, password)) 
        # print ("get data sample:" + response.text

    # IRGL事象情報取得
    def get_irgl_event_info(self, flightCode: Text, departureDate: Text) -> Dict[Text, Text]:
        
        targetUrl = const.get_drupal_base_url() + "/rest/irgl_events?"
        targetUrl = targetUrl + "flight_code=" + flightCode + "&"
        targetUrl = targetUrl + "departure_date=" + departureDate + "&"
        response = self.getData(targetUrl, const.get_drupal_basic_auth_username(), const.get_drupal_basic_auth_password())
        # print(json.loads(response.text))

        result = None
        if len(json.loads(response.text)) > 0:
            result = json.loads(response.text)[0]
        return result

    # IRGL搭乗者情報取得
    def get_irgl_passenger_info(self, flightCode: Text, departureDate: Text, 
        seatNumber: Text, passengerName: Text) -> Dict[Text, Text]:

        targetUrl = const.get_drupal_base_url() + "/rest/irgl_passenger_info?"
        targetUrl = targetUrl + "flight_code=" + flightCode + "&"
        targetUrl = targetUrl + "departure_date=" + departureDate + "&"
        targetUrl = targetUrl + "seat_number=" + seatNumber + "&"
        targetUrl = targetUrl + "name_kana=" + passengerName + "&"
        response = self.getData(targetUrl,const.get_drupal_basic_auth_username(), const.get_drupal_basic_auth_password())
        # print(json.loads(response.text))

        result = None
        if len(json.loads(response.text)) > 0:
            result = json.loads(response.text)[0]
        return result

    # IRGL補償申請審査
    def review_apply_info(self, flightCode: Text, departureDate: Text, 
        seatNumber: Text, reimburseItem: Text, voucherConfirm: Text) -> Dict[Text, Text]:

        targetUrl = const.get_bpm_base_url() + "/flowable-task/process-api/runtime/process-instances"
        requestData = {
            "processDefinitionKey":"IRGL_demo_process",
            "variables": [
                { "name": "departureDate", "value": departureDate},
                { "name": "flightCode", "value": flightCode},
                { "name": "seatNumber", "value": seatNumber},
                { "name": "compensationType", "value": reimburseItem},
                { "name": "receipt", "value": voucherConfirm},
            ]
        }

        response = self.postData(targetUrl, requestData, const.get_bpm_basic_auth_username(), const.get_bpm_basic_auth_password())

        # print(json.loads(response.text)["variables"])
        result = {}
        for itemVar in json.loads(response.text)['variables']: 
            # 審査結果
            if itemVar['name'] == "examinationResult":
                result['review_result'] = itemVar['value']

            # 補償金額
            if itemVar['name'] == "compensationAmount":
                result['amount'] = itemVar['value']

        return result


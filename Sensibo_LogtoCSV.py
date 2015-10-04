import ConfigParser
import csv
import requests
import json
import time
import datetime

_SERVER = 'https://home.sensibo.com/api/v2'

""" Reading API key from config file
the file has only 2 lines:

[SectionOne]
SensiboAPIkey: <<<key obtained from https://home.sensibo.com/me/api once you give your API name>>>
LogFile: <<<full path including file name ending with ".csv"

create such a file and update the path in the following code (read line below)
"""
Config = ConfigParser.ConfigParser()
Config.read("C:\Users\User\Documents\GitHub\sensibo-python-sdk\config.ini")
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

my_api_key = ConfigSectionMap("SectionOne") ['sensiboapikey']
log_file_path = ConfigSectionMap("SectionOne") ['logfile']

class SensiboClientAPI(object):
    def __init__(self, api_key):
        self._api_key = api_key

    def _get(self, path, ** params):
        params['apiKey'] = self._api_key
        response = requests.get(_SERVER + path, params = params)
        response.raise_for_status()
        return response.json()
    def _post(self, path, data, ** params):
        params['apiKey'] = self._api_key
        response = requests.post(_SERVER + path, params = params, data = data)
        response.raise_for_status()
        return response.json()
    def pod_uids(self):
        result = self._get("/users/me/pods")
        pod_uids = [x['id'] for x in result['result']]
        return pod_uids
    def pod_measurement(self, podUid):
        result = self._get("/pods/%s/measurements" % podUid)
        return result['result']

    def pod_ac_state(self, podUid):
        result = self._get("/pods/%s/acStates" % podUid, limit = 1, fields="status,reason,acState")
        return result['result'][0]

    def pod_change_ac_state(self, podUid, on, target_temperature, mode, fan_level):
        self._post("/pods/%s/acStates" % podUid,
                json.dumps({'acState': {"on": on, "targetTemperature": target_temperature, "mode": mode, "fanLevel": fan_level}}))


ts = time.time()
rTimefull = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
rDate = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y')
rTime = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

if __name__ == "__main__":
	client = SensiboClientAPI(my_api_key)
	pod_uids = client.pod_uids()
	currMsr = client.pod_measurement(pod_uids[0])
	#print currMsr[0]['humidity']
	#print currMsr[0]['temperature']
	#print currMsr[0]['time']['time']
	last_ac_state = client.pod_ac_state(pod_uids[0])
	#print last_ac_state['acState']['on']
	if last_ac_state['acState']['on'] :
		last_state = "ON"
	else :
		last_state ="OFF"
	#print last_state
	
	
	""" This will serve as the log file to which the data will be saved
	if the file does not exist it will be created, if it exists data will be appended.
	change the name of the file as you wish, keep it CSV for use with excel (file will be located on the same path as the script)
	"""	
	with open(log_file_path, 'ab') as csvfile:
		fieldnames = ['time', 'rtimestamp', 'rdate', 'rtime', 'temperature', 'humidity', 'status', 'reason', 'last_state', 'targetTemperature', 'mode', 'fanLevel']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', lineterminator='\n')
		writer.writerow({'time': currMsr[0]['time']['time'], 'rtimestamp': rTimefull,'rdate': rDate,'rtime': rTime, 'temperature': currMsr[0]['temperature'], 'humidity': currMsr[0]['humidity'], 'status': last_ac_state['status'], 'reason': last_ac_state['reason'], 'last_state': last_state, 'targetTemperature': last_ac_state['acState']['targetTemperature'], 'mode': last_ac_state['acState']['mode'], 'fanLevel': last_ac_state['acState']['fanLevel']})
		csvfile.close()




#   print "All pod uids:", ", ".join(pod_uids)
#   print client.pod_measurement(pod_uids[0])

#   last_ac_state = client.pod_ac_state(pod_uids[0])
	

"""
    writer.writerow({'measurement time': currMsr[0]['time']['time'], 'temperature': currMsr[0]['temperature'], 'humidity': currMsr[0]['humidity']})
"""	
#    print "Last AC change %(success)s and was caused by %(cause)s" % { 'success': 'was successful' if last_ac_state['status'] == 'Success' else 'failed', 'cause': last_ac_state['reason'] } 
#    print "and set the ac to %s" % str(last_ac_state['acState'])
#    print "Change AC state of %s" % pod_uids[0]
#    client.pod_change_ac_state(pod_uids[0], True, 23, 'cool', 'auto')
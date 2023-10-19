# Written by: Shawn Zamechek
# Documentation added by: Kai Li & Yingquan Li (6/8/21)

"""Transform.py: Transform.py takings data in the form of XML files and converts them
   to the equivalent parquet file."""

import base64
import json
import boto3
import os
import time
import csv
import sys

from xml.etree.ElementTree import XML, fromstring
import xml.etree.ElementTree as ET

#############
## Testing ##
#############

# print('Loading function')
# event = {}
# event['records'] = []
# with open('ff31cb81-d6c2-4bbf-9bae-166e39d5c500.xml') as f:
#     d = f.read()

# event['records'].append(
#     {'data': base64.b64encode(d.encode('utf-8')), 'recordId': 'foo'})

#############
#############
#############

#################
## Main Script ##
#################

# Mapping is a list of dictionaries that takes individual XML attributes and maps them to
# a Parquet column + associated data type.
MAPPING = [
    {'xpath': '.', 'attr': 'BreakType',
        'athena_column': 'breaktype', 'type': 'string'},
    {'xpath': '.', 'attr': 'Duration', 'athena_column': 'duration', 'type': 'string'},
    {'xpath': '.', 'attr': 'PageID', 'athena_column': 'pageid', 'type': 'string'},
    {'xpath': '.', 'attr': 'StationGUID',
        'athena_column': 'stationguid', 'type': 'string'},
    {'xpath': '.', 'attr': 'StationID',
        'athena_column': 'stationid', 'type': 'string'},
    {'xpath': './/Lines', 'attr': '', 'athena_column': 'Lines',
        'type': 'array', 'attrs': ['LineDateTime', 'UTCLineDateTime'], 'include_text': True},
    {'xpath': './/Lines', 'attr': '', 'athena_column': 'transcript',
        'type': 'concat'},
    {'xpath': './/ProgramInfo', 'attr': 'ProgramInfoID',
        'athena_column': 'ProgramInfoID'.lower(), 'type': 'string'},
    {'xpath': './/ProgramInfo', 'attr': 'ProgramDateTime',
        'athena_column': 'ProgramDateTime'.lower(), 'type': 'string'},
    {'xpath': './/ProgramInfo', 'attr': 'ProgramEndDateTime',
        'athena_column': 'ProgramEndDateTime'.lower(), 'type': 'string'},
    {'xpath': './/ProgramInfo/Station', 'athena_column': 'programinfostation',
        'type': 'string', 'include_text': True},
    {'xpath': './/ProgramInfo/Title', 'athena_column': 'programinfotitle',
        'type': 'string', 'include_text': True},
    {'xpath': './/ProgramInfo/Category', 'athena_column': 'programinfocategory',
        'type': 'string', 'include_text': True},
    {'xpath': './/ProgramInfo/Description', 'athena_column': 'programinfodescription',
        'type': 'string', 'include_text': True},
    {'xpath': './/ProgramInfo/CC', 'athena_column': 'programinfocc',
        'type': 'string', 'include_text': True},
    {'xpath': './/ProgramInfo/Live', 'athena_column': 'programinfolive',
        'type': 'string', 'include_text': True},
    {'xpath': './/ProgramInfo/SynNumber', 'athena_column': 'programinfosynnumber',
        'type': 'string', 'include_text': True},
    {'xpath': './/ProgramInfo/ProgramOrigin', 'athena_column': 'programinfoprogramorigin',
        'type': 'string', 'include_text': True},
    {'xpath': './/ProgramInfo/ProgramID', 'athena_column': 'programinfoprogramid',
        'type': 'string', 'include_text': True},
    {'xpath': './/ProgramInfo/ScheduleID', 'athena_column': 'programinfoscheduleid',
        'type': 'string', 'include_text': True},
    {'xpath': './/ProgramInfo/RecordDateTime',
        'athena_column': 'programinforecorddatetime', 'type': 'string', 'include_text': True},
    {'xpath': './/ProgramInfo/RoviRemotePath',
        'athena_column': 'programinforoviremotepath', 'type': 'string', 'include_text': True},
    {'xpath': './/ProgramInfo/ProgramDuration',
        'athena_column': 'programinfoprogramduration', 'type': 'string', 'include_text': True},
    {'xpath': './/ProgramInfo/ProgramGenres', 'athena_column': 'programinfoprogramgenres',
        'type': 'string', 'include_text': True},
    {'xpath': './/ProgramInfo/DateTimeUTC', 'athena_column': 'programinfodatetime',
        'type': 'string', 'include_text': True},
    {'xpath': './/ProgramInfo/AddedDateTimeUTC',
        'athena_column': 'programinfoaddeddatetimeutc', 'type': 'string', 'include_text': True},
    {'xpath': './/Market', 'attr': 'MarketID',
        'athena_column': 'MarketID'.lower(), 'type': 'string'},
    {'xpath': './/Market', 'attr': 'MarketName',
        'athena_column': 'MarketName'.lower(), 'type': 'string'},
    {'xpath': './/Market/Country', 'athena_column': 'marketcountry', 'type': 'string', 'include_text': True},
    {'xpath': './/Market/Active', 'athena_column': 'marketactive', 'type': 'string', 'include_text': True},
    {'xpath': './/Market/FilterOrder', 'athena_column': 'marketfilterorder', 'type': 'string', 'include_text': True},
    {'xpath': './/Market/State', 'athena_column': 'marketstate', 'type': 'string', 'include_text': True},
    {'xpath': './/Market/Latitude', 'athena_column': 'marketlatitude', 'type': 'string', 'include_text': True},
    {'xpath': './/Market/Longitude', 'athena_column': 'marketlongitude', 'type': 'string', 'include_text': True},
    {'xpath': './/Market/DMARank', 'athena_column': 'marketdmarank', 'type': 'string', 'include_text': True},
    {'xpath': './/Station', 'attr': 'StationID',
        'athena_column': 'StationID'.lower(), 'type': 'string'},
    {'xpath': './/Station', 'attr': 'UniqueIdentifier',
        'athena_column': 'StationUniqueIdentifier'.lower(), 'type': 'string'},
    {'xpath': './/Station/CallSign', 'athena_column': 'stationcallsign', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/StationName', 'athena_column': 'stationstationname', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/MarketID', 'athena_column': 'stationmarketid', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/Location', 'athena_column': 'stationlocation', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/GMTOffset', 'athena_column': 'stationgmtoffset', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/GMTOffsetMinutes', 'athena_column': 'stationgmtoffsetminutes', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/TextType', 'athena_column': 'stationtexttype', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/RightToLeft', 'athena_column': 'stationrighttoleft', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/PhoneticType', 'athena_column': 'stationphonetictype', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/MediaType', 'athena_column': 'stationmediatype', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/Active', 'athena_column': 'stationactive', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/SortOrder', 'athena_column': 'stationsortorder', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/IsUnicode', 'athena_column': 'stationisunicode', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/Website', 'athena_column': 'stationwebsite', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/MediaProcessType', 'athena_column': 'stationmediaprocesstype', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/MediaPurchase', 'athena_column': 'stationmediapurchase', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/PCHourOffSet', 'athena_column': 'stationpchouroffset', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/PCMinOffSet', 'athena_column': 'stationpcminoffset', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/NationalNetwork', 'athena_column': 'stationnationalnetwork', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/PrimaryLanguage', 'athena_column': 'stationprimarylanguage', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/MediaStationID', 'athena_column': 'stationmediastationid', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/TimeZoneIdentifier', 'athena_column': 'stationtimezoneidentifier', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/SiteID', 'athena_column': 'stationsiteid', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/RoviTVDataSourceID', 'athena_column': 'stationrovitvdatasourceid', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/RoviFTPRemoteDir', 'athena_column': 'stationroviftpremotedir', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/CaptureLocation', 'athena_column': 'stationcapturelocation', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/AlterTextCase', 'athena_column': 'stationaltertextcase', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/AllowMediaDownload', 'athena_column': 'stationallowmediadownload', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/CaptureSiteCode', 'athena_column': 'stationcapturesitecode', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/BackupStationID', 'athena_column': 'stationbackupstationid', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/DateAdded', 'athena_column': 'stationdateadded', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/AudioFingerprintingEnabled', 'athena_column': 'stationaudiofingerprintingenabled', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/BroadcastOwnerID', 'athena_column': 'stationbroadcastownerid', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/CaptureServer', 'athena_column': 'stationcaptureserver', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/ForSummariesUseBACK', 'athena_column': 'stationforsummariesuseback', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/EnableQA', 'athena_column': 'stationenableqa', 'type': 'string', 'include_text': True},
    {'xpath': './/Station/MarketName', 'athena_column': 'stationmarketname', 'type': 'string', 'include_text': True}
]


def applyMapping(root, mapping=MAPPING):
	"""
	Function that takes an XML file as a string and returns the associated Parquet file that
	the XML corresponds to.
	
	Parameters
	----------
	root : xml.etree.ElementTree
		The XML encoded as an ElementTree after conversion from a string.
	mapping : List
		List of dictionaries that contains all the mapping for all columns of information
		of the Parquet file.  
	Returns
	-------
	List
		A List of of dictionary values. 
	"""
    result = {}
    for item in mapping:
        element = (root.find(item['xpath']))

        # Process XML attribute if a string is discovered.
        if item['type'] == 'string':
            if 'include_text' in item and item['include_text']:
                try:
                    result[item['athena_column']] = element.text
                except:
                    print("ERROR MISSING:", item['athena_column'])
                    print(element.find('.//Station/MediaType')).text
                    result[item['athena_column']] = None
            else:
                try:
                    result[item['athena_column']] = element.attrib.get(item['attr'])
                except:
                    print("ERROR MISSING:", item['athena_column'])
                    
                    result[item['athena_column']] = None

        # Process an XML attribute if the attribute needs to be part of an array.
        elif item['type'] == 'array':
            array = []
            for child in element.getchildren():
                for attr in item['attrs']:
                    subitem = {}
                    subitem[attr] = child.get(attr)
                    if item['include_text']:
                        subitem['text'] = child.text
                    array.append(subitem)
            result[item['athena_column']] = array

        # Process XML text if the text needs to be concatinated into a string.
        elif item['type'] == 'concat':
            concat_string = ''
            for child in element.getchildren():
                concat_string += child.text + ' '
            result[item['athena_column']] = concat_string
    return [result]

def lambda_handler(event, context):
	"""
	Lambda Function that handles a data chunk coming in from AWS Kinesis Data Streams and 
	parses each XML file using the applyMapping() function.
	Parameters
	----------
	event : object
		JSON-formatted document that contains data for a Lambda function to process.
	context : object
		Provides methods and properties that provide information about the invocation, 
		function, and runtime environment. 
	Returns
	-------
	Dictionary
		A dictionary of the records that are processed is returned.
	"""
    output = []

    for record in event['records']:
        payload = base64.b64decode(record['data'])
        xmlstring = str(payload.decode('utf-8'))
        # print(xmlstring)
        root = ET.fromstring(str(xmlstring))
        parsedRecords = applyMapping(root)
        data_string = b''
        for r in parsedRecords:
            data_string += json.dumps(r).encode('utf-8') + b'\n'

        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(data_string)
        }
        output.append(output_record)

    print('Successfully processed {} records.'.format(len(event['records'])))
    return {'records': output}

# lambda_handler(root, {})
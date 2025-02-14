import urllib.parse
import httpx
import pandas as pd
from collections import defaultdict
import urllib


CLIENT = httpx.Client()

# Location district Codes
DISTRICT_CODES={
    "W":"Etobicoke-Yrk",
    "N":"North York",
    "E":"Scarborough",
    "S":"Tornoto and East York"
}


# Api urls for accounding district and required filters
API_URLS=["https://services3.arcgis.com/b9WvedVPoizGfvfD/ArcGIS/rest/services/COTGEO_IBMS_AIC_POINT/FeatureServer/0/query?where=(DISTRICT_CODE%20=%20%27W%27)%20AND%20APPLICATION_TYPE%20=%20%27C%20of%20A%27%20AND%20(%20INDATE%20BETWEEN%20TIMESTAMP%20%272025%2001%2013%2000:00:00%27%20AND%20TIMESTAMP%20%272025%2002%2012%2000:00:00%27%20)%20AND%20STATUS_GROUP%20=%20%27Open%27&resultRecordCount=1000&objectIds=&time=&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&resultType=none&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=4326&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=json&_=1739378201679",
          "https://services3.arcgis.com/b9WvedVPoizGfvfD/ArcGIS/rest/services/COTGEO_IBMS_AIC_POINT/FeatureServer/0/query?where=(DISTRICT_CODE%20=%20%27N%27)%20AND%20APPLICATION_TYPE%20=%20%27C%20of%20A%27%20AND%20(%20INDATE%20BETWEEN%20TIMESTAMP%20%272025%2001%2013%2000:00:00%27%20AND%20TIMESTAMP%20%272025%2002%2012%2000:00:00%27%20)%20AND%20STATUS_GROUP%20=%20%27Open%27&resultRecordCount=1000&objectIds=&time=&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&resultType=none&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=4326&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=json&_=1739378201681",
          "https://services3.arcgis.com/b9WvedVPoizGfvfD/ArcGIS/rest/services/COTGEO_IBMS_AIC_POINT/FeatureServer/0/query?where=(DISTRICT_CODE%20=%20%27E%27)%20AND%20APPLICATION_TYPE%20=%20%27C%20of%20A%27%20AND%20(%20INDATE%20BETWEEN%20TIMESTAMP%20%272025%2001%2013%2000:00:00%27%20AND%20TIMESTAMP%20%272025%2002%2012%2000:00:00%27%20)%20AND%20STATUS_GROUP%20=%20%27Open%27&resultRecordCount=1000&objectIds=&time=&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&resultType=none&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=4326&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=json&_=1739378201683",
          "https://services3.arcgis.com/b9WvedVPoizGfvfD/ArcGIS/rest/services/COTGEO_IBMS_AIC_POINT/FeatureServer/0/query?where=(DISTRICT_CODE%20=%20%27S%27)%20AND%20APPLICATION_TYPE%20=%20%27C%20of%20A%27%20AND%20(%20INDATE%20BETWEEN%20TIMESTAMP%20%272025%2001%2013%2000:00:00%27%20AND%20TIMESTAMP%20%272025%2002%2012%2000:00:00%27%20)%20AND%20STATUS_GROUP%20=%20%27Open%27&resultRecordCount=1000&objectIds=&time=&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&resultType=none&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=4326&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=json&_=1739378201687"
]

APPLICATION_URL="https://www.toronto.ca/city-government/planning-development/application-details/"
ATTACHMENT_URL="https://api.toronto.ca/aic/getapplicationattachments"
ATTACHMENT_DOCUMENT_URL ="https://secure.toronto.ca/AIC/getAttachment.do"
API_KEY ="AAPK5b6b3fd7e4cf45ddb306692f9be2e620e4kRB8rW6Ao1xm1UvinBtyvltYSldHldobU3Vm7EctphOIZvtQzYEMI8HzqVP5__"

EXCEL_FILE_NAME="data.xlsx"

def decoding_feature(feature):
    attributes = feature['attributes']
    STATUS = attributes['STATUS_DESC']
    # document_url = attributes['AIC_URL']
    DESCRIPTION= attributes["FOLDERDESCRIPTION"]
    FOLDERRSN = attributes['FOLDERRSN']
    PID = attributes["PROPERTYRSN"]
    FOLDERNAME = attributes['FOLDERNAME']
    return (STATUS  ,PID,FOLDERNAME, DESCRIPTION ,FOLDERRSN)
            
    
def make_post_request(pid,foldername,folderrsn):
    url_data = {
        "id":folderrsn,
        "pid":pid,
        "title":foldername
    }
    data ={
        "folderRsn":folderrsn,
        "time":""
    }
    headers={
        "mapapikey":API_KEY,
        "content_type":"application/json"
    }
    # url_query_params= urllib.parse.urlencode(url_data)
    # url = f"{APPLICATION_URL}?{data}"
    result = CLIENT.post(url=ATTACHMENT_URL,data=data,headers=headers)
    result =result.json()
    return result
    
def request_url(url):
    data =defaultdict(list)
    response = CLIENT.get(url=url)
    if response.status_code == 200:
        response= response.json()
        features = response.get("features")
        if not features:
            return data
        print("Total Locations found:-", len(features))
        for index , feature in enumerate(features):
            # print(f"Location {index} data - {feature}")
            feature_result = decoding_feature(feature=feature)
            
            
            (STATUS  ,PID,FOLDERNAME, DESCRIPTION ,FOLDERRSN) = feature_result
            attachments_result = make_post_request(PID,FOLDERNAME,FOLDERRSN)
            # for attachment in attachments_result:
            #     attachmentDesc = attachment['attachmentDesc']
            #     attachmentRsn = attachment['attachmentRsn']
            #     if attachmentDesc == "CA Application Form":
            #         data = {"attachmentRsn":attachmentRsn,"time":""}
            #         document_result = make_post_request(data,ATTACHMENT_DOCUMENT_URL)
            #         print(document_result)
                        
            
            
# for url in API_URLS:
# request_url(API_URLS[0])
    

response =CLIENT.post(url="https://www.google.com/recaptcha/api2/reload?k=6LeN_XIUAAAAAEd8X21vFtkJ3_c7uA0xpUGcrGpe")
print(response)
headers={
        "mapapikey":API_KEY,
 }
attachments_data ={
    "folderRsn":"5570170",
    "time":""
}
data={
    "attachmentRsn":"sx5hiKvIqf1yhPAwLuJtsA==",
    "time":""
}

result = CLIENT.post(url=ATTACHMENT_URL,data=attachments_data,headers=headers)
print(result.json())
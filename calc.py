import numpy as np
import requests
from datetime import datetime, timezone

def calculate(api_key,email,threshold): 
    # start = time.time()

    # import page 1 from get profiles endpoint 
    url = "https://a.klaviyo.com/api/profiles/?page[size]=100&additional-fields[profile]=predictive_analytics.historic_clv&fields[profile]=id"

    headers = {
        "accept": "application/json",
        "revision": "2023-02-22",
        "Authorization": f"Klaviyo-API-Key {api_key}"
    }

    response = requests.get(url, headers=headers)
    historicClvs = []
    userPercentile = threshold

    # define function to get clvs and add them to variable historicClvs  
    def getPageCLV(payload):
        if not payload.json()['data']:
            payload.json()['data'] = []
        for person in payload.json()['data']:
            if person["attributes"]["predictive_analytics"]["historic_clv"]:
                historicClvs.append(person["attributes"]["predictive_analytics"]["historic_clv"]) 
    
    # loop through all pages from get profiles endpoint, appending clvs from each page to the historicClvs variable
    pages_remaining = True

    while(pages_remaining):
        getPageCLV(response)
        url = response.json()["links"]["next"]
        response = requests.get(url, headers=headers)
        if not response.json()["links"]["next"]:
            pages_remaining = False

    # calculate threshold for top X% of customers
    threshold = np.percentile(historicClvs,100-userPercentile)

    # end = time.time()

    # timeInSeconds = end - start
    # numberOfProfiles = len(historicClvs)

    #display CLV threshold
    # print("It took {:.0f}".format(end - start),"seconds")
    # print(numberOfProfiles / timeInSeconds)
    print("Your top",userPercentile,"percent of customers have a historic lifetime value of ${:.2f}".format(threshold),"or more.")

    # Klaviyo flow to send results: https://www.klaviyo.com/email/flow/W64JMk/content

    url = "https://a.klaviyo.com/api/events/"

    payload = {"data": {
            "type": "event",
            "attributes": {
                "profile": {"email": email},
                "metric": {"name": "CLV results ready"},
                "properties": {
                    "CLV bin size": userPercentile,
                    "CLV threshold": threshold
                },
                "time": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            }
        }}
    headers = {
        "accept": "application/json",
        "revision": "2023-02-22",
        "content-type": "application/json",
        "Authorization": "Klaviyo-API-Key pk_7fa7c93d506aabbe3c0a034c74ab3250f8"
    }

    response = requests.post(url, json=payload, headers=headers)

    # print(response.text)


# calculate('pk_7fa7c93d506aabbe3c0a034c74ab3250f8','elise.d93@gmail.com',10)
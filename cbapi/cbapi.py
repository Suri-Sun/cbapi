import json
import requests
import numpy as np
import pandas as pd
import threading
import queue
from multiprocessing import cpu_count
from datetime import datetime, date, time, timedelta, timezone

RAPIDAPI_KEY = None


def set_key(key):
    """

    :param key: str
        Your own RAPIDAPI_KEY. Create an account on RAPIDAPI if you don't have one

    """
    global RAPIDAPI_KEY
    RAPIDAPI_KEY = key


def get_key():
    """

    :return: str
        RAPIDAPI KEY for requesting

    """
    if RAPIDAPI_KEY:
        return RAPIDAPI_KEY
    else:
        print("Please set the RAPIDAPI key first! Call set_KEY(<YOUR_RAPIDAPI_KEY>)")


def default_timestamp():
    """Get default timestamp, which is yesterday

    :return: int
        Unix timestamp of yesterday in UTC
    """
    current_date = datetime.combine(date.today(), time(0, 0, 0))
    yesterday_date = current_date - timedelta(days=1)
    yday_timestamp_utc = int(yesterday_date.replace(tzinfo=timezone.utc).timestamp())
    return yday_timestamp_utc


def trigger_api(obj_type, querystring):
    """

    :param obj_type: str
        Object of query, whether it's for organizations, or for people
        Available types are "organizations" and "people"
    :param querystring: dict
        Optional Parameters for query
    :return: json
        Data filtered by parameters

    """

    headers = {'x-rapidapi-host': "crunchbase-crunchbase-v1.p.rapidapi.com",
               'x-rapidapi-key': get_key()}

    url = "https://crunchbase-crunchbase-v1.p.rapidapi.com/odm-" + obj_type

    response = requests.request("GET", url, headers=headers, params=querystring)

    if 200 == response.status_code:
        # print("Success")
        return json.loads(response.text)
    else:
        # print("Failed")
        return None


def get_info(obj_type, querystring):
    """

    :param obj_type: str
        Object of query, whether it's for organizations, or for people
        Available types are "organizations" and "people"
    :param querystring: dict
        Optional Parameters for query
    :return: pd.DataFrame
        Data obtained

    """

    lock = threading.Lock()

    def thread_func(target, pages):
        """Append content of each page to the target pd.DataFrame

        :param target: queue.Queue
            Store the request result.
        :param pages: np.array
            page number array for query

        """
        for page in pages:
            # query each page in the given range
            querystring_temp = {**querystring, "page": str(page)}
            api_response_temp = trigger_api(obj_type, querystring_temp)

            # iterate though each organization/ person
            for item in api_response_temp["data"]["items"]:

                # Acquire properties of each item, and use its name for record index
                dict_record = item["properties"]
                if obj_type == "organizations":
                    item_name = dict_record["name"]
                    dict_record.pop("name", None)
                elif obj_type == "people":
                    item_name = dict_record["first_name"] + dict_record["last_name"]
                    dict_record.pop("first_name", None)
                    dict_record.pop("last_name", None)

                record = pd.Series(dict_record, name=item_name)  # format the record into pd.Series
                try:
                    lock.acquire()  # lock the target queue
                    target.put(record)  # put the record into the queue
                finally:
                    lock.release()  # release the lock

    # trigger API for the given type and query parameters
    api_response = trigger_api(obj_type, querystring)

    # check for item existence
    if api_response["data"]["paging"]["total_items"] == 0:
        return None

    num_of_pages = api_response["data"]["paging"]["number_of_pages"]
    current_page = api_response["data"]["paging"]["current_page"]

    # queue for storing items
    q_records = queue.Queue()

    # if number of pages is less than number of CPU cores, use that much of threads
    if num_of_pages < cpu_count():
        num_of_threads = num_of_pages
    else:
        num_of_threads = cpu_count()  # Rule of Thumb: 1 thread per CPU core

    threads = []
    lock = threading.Lock()

    # Split page ranges
    pages_partition = np.array_split(range(1, num_of_pages + 1), num_of_threads)

    for i in range(num_of_threads):
        thread = threading.Thread(target=thread_func, args=(q_records, pages_partition[i],))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # DataFrame for formatting and outputting
    properties = list(api_response["data"]["items"][0]["properties"].keys())
    df_records = pd.DataFrame(columns=properties)
    while not q_records.empty():
        df_records = df_records.append(q_records.get())

    return df_records


def get_org(since_time=default_timestamp(), query=None, name=None, domain_name=None,
            locations=None, org_types=None, page=1):
    """

    :param since_time: int
        Unix timestamp. When provided, restricts the result set to Organizations where updated_at >= the passed value
        Otherwise, use yesterday as default
    :param query: str
        Full text search of an Organization's name, aliases (i.e. previous names or "also known as"), and short description
    :param name: str
        Full text search limited to name and aliases
    :param domain_name: str
        Text search of an Organization's domain_name (e.g. www.google.com)
    :param locations: str
        Filter by location names (comma separated, AND'd together) e.g. locations=California,San Francisco
    :param org_types: str
        Filter by one or more types. Multiple types are separated by commas.
        Available types are "company", "investor", "school", and "group". Multiple organization_types are logically AND'd.
    :param page: str
        Page number of the results to retrieve
    :return: pd.DataFrame
        Organization data filtered by the params

    """

    querystring = {"updated_since": str(since_time),
                   "query": query,
                   "name": name,
                   "domain_name": domain_name,
                   "locations": locations,
                   "organization_types": org_types,
                   "page": page}

    return get_info("organizations", querystring)


def get_ppl(since_time=default_timestamp(), query=None, name=None, socials=None,
            locations=None, type=None, page=1):
    """

    :param since_time: int
        Unix timestamp. When provided, restricts the result set to Organizations where updated_at >= the passed value
        Otherwise, use yesterday as default
    :param query: str
        A full-text query of name, title, and company
    :param name: str
        A full-text query of name only
    :param socials: str
        Filter by social media identity (comma separated, AND'd together) e.g. socials=ronconway
    :param locations: str
        Filter by location names (comma separated, AND'd together) e.g. locations=California,San Francisco
    :param type: str
        Filter by type (currently, either this is empty, or is simply "investor")
    :param page: str
        Page number of the results to retrieve
    :return: pd.DataFrame
        People data filtered by the params

    """

    querystring = {"updated_since": str(since_time),
                   "query": query,
                   "name": name,
                   "socials": socials,
                   "locations": locations,
                   "type": type,
                   "page": page}

    return get_info("people", querystring)

import gtfs_realtime_pb2
import requests
from dotenv import load_dotenv
import os
from datetime import datetime

print("Starting")

# takes a url and api key and returns the response content
def read_gtfs_realtime(feed_url, api_key):

    req_headers = {"x-api-key": api_key}
    response = requests.get(feed_url, headers=req_headers)

    if response.status_code != 200:
        print(f"HTTP Response not 200, url:{response.request.url},status_code:{response.status_code}, reason:{response.reason}")
        return

    return response.content

# takes a FeedMessage and gets returns a list of stop_time_updates that stop at target
def find_stop_on_ace(feed, target_stop_id):
    out = []
    for entity in feed.entity:
        if not entity.trip_update:
            continue
        for stop_time_update in entity.trip_update.stop_time_update:
            if stop_time_update.stop_id == target_stop_id:
                out.append(stop_time_update)
    
    return out

# takes list of stop_time_updates and returns next n stops
def find_next_n_stop_times(stop_time_updates, n):
    stop_time_updates.sort(key=lambda update: update.arrival.time)
    out = [datetime.fromtimestamp(update.arrival.time) for update in stop_time_updates[:n]]
    return out




# main
load_dotenv()
MTA_API_KEY=os.getenv("MTA_API_KEY")
A_C_E_URI=os.getenv("A_C_E_URI")

proto_res = read_gtfs_realtime("https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace", MTA_API_KEY)
if not proto_res:
    print("No response from api. Exiting")
    exit(1)

feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(proto_res)

# TODO - Make it so we can just declare the station name and direction.
ace_stops = find_stop_on_ace(feed,"A44N")

upcoming_ace_stop_times = find_next_n_stop_times(ace_stops, 3)

time_to_next_stop = []

for t in upcoming_ace_stop_times:
    now = datetime.now()
    if t < now:
        continue
    delta = t - now
    time_to_next_stop.append(delta.seconds // 60)
    print(f"next train in: {time_to_next_stop[-1]}min")


print(time_to_next_stop)
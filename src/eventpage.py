# -*- coding:utf-8 -*-

from connpass import Connpass
from bs4 import BeautifulSoup
import requests

class Event():
    def __init__(self):
        self.connpass = Connpass()
        self.start = 0

    def from_date(self, date_array, count=1):
        response = self.connpass.search(ymd=date_array, count=count, start=self.start)
        self.start += response["results_returned"]
        return response["events"]
        

    def from_ids(self, event_ids, count=1):
        response = self.connpass.search(event_id=event_ids, count=count, start=self.start)
        self.start += response["results_returned"]
        return response["events"]


class Page():
    def __init__(self, url):
        r = requests.get(url)
        self.soup = BeautifulSoup(r.text, "html.parser")

    def organizers(self):
        tags = self.soup.select(".group_inner.event_owner_area > ul > li > a")
        return list(map(lambda t: t.get("href"), tags))

    def presenters(self):
        tags = self.soup.select(".event_presenters_area.clearfix > a")
        return list(map(lambda t: t.get("href"), tags))


class Profile():
    def __init__(self, url):
        r = requests.get(url)
        self.soup = BeautifulSoup(r.text, "html.parser")
    
    def twitter(self):
        tag = self.soup.select(".social_link > a")[0]
        return tag.get("href")


if __name__ == "__main__":
    events = Event().from_ids([151291])
    for event in events:
        url = event["event_url"]
        page = Page(url)

        print("-- presenters --")
        presenters = page.presenters()
        for url in presenters:
            profile = Profile(url)
            print(profile.twitter())
        
        print("-- organizers --")
        organizers = page.organizers()
        for url in organizers:
            profile = Profile(url)
            print(profile.twitter())



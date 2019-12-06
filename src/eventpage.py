from connpass import Connpass
from bs4 import BeautifulSoup
import requests
import urllib.parse


class Event():
    def __init__(self):
        self.connpass = Connpass()
        self.start = 0

    def from_date(self, date_array, count=1):
        response = self.connpass.search(
            ymd=date_array, count=count, start=self.start)
        self.start += response["results_returned"]
        return response["events"]

    def from_ids(self, event_ids, count=1):
        response = self.connpass.search(
            event_id=event_ids, count=count, start=self.start)
        self.start += response["results_returned"]
        return response["events"]


class Page():
    def __init__(self, url):
        r = requests.get(url)
        self.soup = BeautifulSoup(r.text, "html.parser")

    def twitter_filter(self, domain):
        return 'twitter' in domain if True else False

    def extract_username(self, url):
        qs = urllib.parse.urlparse(url).query
        qs_d = urllib.parse.parse_qs(qs)
        return qs_d["screen_name"][0] if "screen_name" in qs_d.keys() else None

    def tag2url(self, tags):
        urls = map(lambda t: self.extract_username(t.get("href")), tags)
        return list(filter(lambda x: x != None, urls))

    def organizers(self):
        tags = self.soup.select(".concerned_area > table > tbody")[
            0].select("td.social.text_center > a")
        return self.tag2url(tags)

    def presenters(self):
        tags = self.soup.select(".concerned_area > table > tbody")[
            1].select("td.social.text_center > a")
        return self.tag2url(tags)
    
    def attendees(self):
        tags = self.soup.select(".participation_table_area > table > tbody > tr > td.social.text_center > a")
        return self.tag2url(tags)


def participation_url(event):
    return event["event_url"] + "participation"

if __name__ == "__main__":

    events = Event().from_ids([151291])
    for event in events:
        url = participation_url(event)
        page = Page(url)

        print("-- organizers --")
        organizers = page.organizers()
        print(organizers)

        print("-- presenters --")
        presenters = page.presenters()
        print(presenters)

        print("-- attendees --")
        attendees = page.attendees()
        print(attendees)

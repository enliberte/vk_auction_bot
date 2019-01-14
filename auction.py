import vk_api
import requests
from time import sleep


class AuctionBot:
    def __init__(self, login, password, owner_id, post_id, start_bid, max_acceptable_price, interval):

        vk_session = vk_api.VkApi(login, password)
        vk_session.auth()

        self.access_token = vk_session.token['access_token']
        self.owner_id = owner_id
        self.post_id = post_id
        self.current_bid = start_bid
        self.max_acceptable_price = max_acceptable_price
        self.interval = interval

    def get_max_bid(self):
        method = 'https://api.vk.com/method/wall.getComments'
        params = {'owner_id': self.owner_id,
                  'post_id': self.post_id,
                  'access_token': self.access_token,
                  'count': 100,
                  'offset': 0,
                  'v': "5.80"}
        response = requests.get(method, params=params).json()
        bids = [int(bid['text']) for bid in response['response']['items'] if bid['text'].isdigit()]
        return max(bids)

    def make_bid(self, bid):
        method = 'https://api.vk.com/method/wall.createComment'
        params = {'owner_id': self.owner_id,
                  'post_id': self.post_id,
                  'access_token': self.access_token,
                  'v': "5.80",
                  'message': '%s' % bid}
        requests.get(method, params=params)

    def event_loop(self):
        while True:
            max_bid = self.get_max_bid()
            if max_bid <= self.max_acceptable_price:
                print(max_bid)
                if max_bid > self.current_bid:
                    self.current_bid = max_bid + 1
                    self.make_bid(self.current_bid)
            else:
                break
            sleep(self.interval)


if __name__ == '__main__':
    test_auction = AuctionBot()
    test_auction.event_loop()
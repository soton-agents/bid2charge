from models import Bid, Auction, EVUser
from django.utils import timezone

def marginal_price_vector (bidders):
	u1 = EVUser()
	u2 = EVUser()
	u3 = EVUser()
	u4 = EVUser()

	auction = Auction()
	auction.total_energy = 30
	auction.day = 1
	auction.timestamp = timezone.now()

	bids = []

	for i in range(1, 12):
		bid = Bid(user = u1, nth = i, value = 0.72, auction = auction, timestamp = timezone.now())
		bids.append(bid)

	for i in range(1, 7):
		bid = Bid(user = u2, nth = i, value = 1.66, auction = auction, timestamp = timezone.now())
		bids.append(bid)

	for i in range(1, 16):
		bid = Bid(user = u3, nth = i, value = 0.8, auction = auction, timestamp = timezone.now())
		bids.append(bid)

	for i in range(1, 6):
		bid = Bid(user = u4, nth = i, value = 1.0, auction = auction, timestamp = timezone.now())
		bids.append(bid)

	units_left = auction.total_energy
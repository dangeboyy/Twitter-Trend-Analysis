from pymongo import MongoClient
from pprint import pprint
import urllib.parse
import urllib.request
import certifi

client = MongoClient("mongodb+srv://dbAdmin:" +  urllib.parse.quote("Zombi123") + "@cluster0.xv6ij.mongodb.net/cluster0?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db=client.business

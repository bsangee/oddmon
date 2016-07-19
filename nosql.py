#AUTHOR: SANGEETHA BANAVATHI 
#MONGODB to store metric collected
import logging
import pymongo
logger = logging.getLogger("app.%s" % __name__)

class G:
    conn = None

def drop_table(client,name):
        client.drop_database(name)
        logger.info("Database %s dropped" % name)

def create_table(client, name="OST_STATS", drop = False):
        if drop:
                drop_table(client,name)

        db = client.name

        logger.info("Database %s created" % name)
        global collection
        collection = db.name
        collection
        logger.info("Collection %s created" % name)


def insert_row(metric, stats):

        doc = {}

        for target, attr in stats.iteritems():
            doc["Metric"] = metric
            doc["Target"] = target
            doc["Attributes"] = str(attr)
        collection.insert(doc)


def db_init(hosts, port, initTable=False):

    if G.conn is None:

        try:
                for host in hosts:
                        logger.warn('mongodb://'+host+":"+port)
                        client = pymongo.MongoClient('mongodb://'+host+":"+port)
                        print "Connected successfully!!!"
        except pymongo.errors.ConnectionFailure, e:
                print "Could not connect to MongoDB: %s" % e
    create_table(client, drop = initTable)

def db_close():
    if G.conn is not None:
        G.conn.close()



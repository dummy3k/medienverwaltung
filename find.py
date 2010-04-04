import amazonproduct
import sys
import ConfigParser
from optfunc import optfunc

import helper as h

def find(keywords, SearchIndex='DVD'):
    config = ConfigParser.ConfigParser()
    config.read('settings.conf')

    actors = set()
    api = amazonproduct.API(config.get('Amazon', 'AccessKeyID'),
                            config.get('Amazon', 'SecretAccessKey'))
    #~ node = api.item_search('Books', Publisher='Terminator')
    node = api.item_search(SearchIndex, Title=sys.argv[1])
    print "Idx\tASIN\t\tTitle"
    for index, item in enumerate(node.Items.Item):
        print "%s:\t%s:\t%s" % (index,
                                item.ASIN,
                                unicode(item.ItemAttributes.Title)[:70])


        #~ raw_input("Get Details...")
        details = api.item_lookup(item.ASIN, ResponseGroup='Images,ItemAttributes')
        item_detail = details.Items.Item[0]
        print item_detail.LargeImage.URL
        try:
            for sub_item in item_detail.ItemAttributes.Actor:
                print sub_item #, link_item.URL
                actors.add(str(sub_item))
        except AttributeError:
            print "Could not list actors"

        h.ipython()()
        #~ break

        print actors

if __name__ == '__main__':
    optfunc.run(find)
    #~ optfunc.main([find_dvds,])

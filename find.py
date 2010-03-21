import amazonproduct
import sys
import ConfigParser
from optfunc import optfunc

import helper as h

def find(keywords, SearchIndex='DVD'):
    config = ConfigParser.ConfigParser()
    config.read('settings.conf')

    api = amazonproduct.API(config.get('Amazon', 'AccessKeyID'),
                            config.get('Amazon', 'SecretAccessKey'))
    #~ node = api.item_search('Books', Publisher='Terminator')
    node = api.item_search(SearchIndex, Title=sys.argv[1])
    print "Idx\tASIN\t\tTitle"
    for index, item in enumerate(node.Items.Item):
        print "%s:\t%s:\t%s" % (index,
                                item.ASIN,
                                unicode(item.ItemAttributes.Title)[:70])


        details = api.item_lookup(item.ASIN)
        item_detail = details.Items.Item[0]
        for link_item in item_detail.ItemLinks.ItemLink:
            print link_item.Description #, link_item.URL
        #~ h.ipython()()
        #~ break

if __name__ == '__main__':
    optfunc.run(find)
    #~ optfunc.main([find_dvds,])

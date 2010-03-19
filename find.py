import amazonproduct
import sys
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('settings.conf')

api = amazonproduct.API(config.get('Amazon', 'AccessKeyID'),
                        config.get('Amazon', 'SecretAccessKey'))
#~ node = api.item_search('Books', Publisher='Terminator')
node = api.item_search('DVD', Title=sys.argv[1])
for index, item in enumerate(node.Items.Item):
    try:
        #~ print item.ItemAttributes.Title
        print "%s:\t%s" % (index, unicode(item.ItemAttributes.Title))
    except:
        print "NOOOOOOO"

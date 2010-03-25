import amazonproduct
import ConfigParser

import helper as h

while True:
    user_input = raw_input("ISBN:")
    print user_input
    if user_input == 'exit':
        break

    #~ user_input = "9783789132186"

    config = ConfigParser.ConfigParser()
    config.read('settings.conf')

    api = amazonproduct.API(config.get('Amazon', 'AccessKeyID'),
                            config.get('Amazon', 'SecretAccessKey'))
    #~ node = api.item_search('Books', Publisher='Terminator')
    SearchIndex='Books'
    node = api.item_lookup(user_input, IdType='ISBN', SearchIndex=SearchIndex)
    item = node.Items.Item
    #~ h.ipython()()
    print unicode(item.ItemAttributes.Title)
 


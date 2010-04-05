
print "Starting..."
try:
    node = self.api.item_lookup(",".join(asins),
                                ResponseGroup="Images,ItemAttributes")
except Exception, ex:
    print "caught exception %s: %s" % (type(ex), ex)

print "the end."

            

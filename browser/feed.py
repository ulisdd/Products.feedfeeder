from zope import interface
from zope import component
from Products.feedfeeder.interfaces.consumer import IFeedConsumer

class IUpdateFeedItems(interface.Interface):
    def update(): pass

class UpdateFeedItems(object):
    """A view for updating the feed items in a feed folder.
    """
    
    interface.implements(IUpdateFeedItems)
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
    
    def update(self):
        consumer = component.getUtility(IFeedConsumer)
        consumer.retrieveFeedItems(self.context)

    def __call__(self):
        self.update()
        self.request.response.redirect(self.context.absolute_url()
                                       +"?portal_status_message=Feed+items+updated")
class FeedFolderView(object):
    """A view for feed folders.
    """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def items(self):
        """All feed items.  Currently implemented as a generator since
        there could theoretically be tens of thousands of items.
        """
        
        listing = self.context.getFolderContents
        for index, x in enumerate(listing({'sort_on': 'getFeedItemUpdated', 
                                           'sort_order': 'descending'})):
            item = dict(updated_date = x.getFeedItemUpdated.strftime('%d-%m'),
                        url = x.getURL(),
                        title = x.Title,
                        author = x.getFeedItemAuthor,
                        )
            obj = x.getObject()
            self.extraDecoration(item, obj)
            enclosures = obj.getFolderContents()

            if (not obj.getText()) and len(enclosures) == 1:
                # only one enclosure? return item title but return link
                # to sole enclosure
                enclosure = enclosures[0]
                enc = dict(item)
                enc['url'] = enclosure.getURL()
                yield enc
            else:
                yield item

    def extraDecoration(self, item, obj):
        pass

    def item_list(self):
        return [x for x in self.items]

    def __call__(self):
        return self.index(template_id='feed-folder.html')
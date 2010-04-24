<%inherit file="/layout-default.mako"/>\

<%def name="title()">${_("Select image")}</%def>

<%def name="content()">
<p>${_("Click the image you want to attach to the medium.")}</p>

% for item in c.items:
%   if 'LargeImage' in dir(item):
<form id="signin-form" method="post" action="${h.url_for(action='query_images_post')}">
<input type="hidden" name="url" value="${unicode(item.LargeImage.URL)}">
<input type="image" src="${unicode(item.LargeImage.URL)}">
</form>

##<img src="${unicode(item.LargeImage.URL)}" />
%   endif
% endfor
##<input type="hidden" name="media_id" value="${c.media_id}" />
##<input type="submit" value="Attach to '${c.item}'" class="button"/>
</form>
</%def>

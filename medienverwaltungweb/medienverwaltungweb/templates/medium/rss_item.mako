-*- coding: utf-8 -*-
<%def name="description(item, h)">
${item.title}
% for tag in item.tags:
<a href="${h.url_for(controller='medium', action='list_gallery', tag=tag.name)}">${tag.name}</a> 
% endfor
</%def>

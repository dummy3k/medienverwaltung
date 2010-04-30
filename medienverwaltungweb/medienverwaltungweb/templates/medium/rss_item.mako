-*- coding: utf-8 -*-
<%def name="description(item, h, base_url)">
% if item.image_data:
<p>
    <a href="${base_url + h.url_for(controller='medium', action='edit', id=item.id)}">
    <img src="${base_url + h.url_for(controller='medium', action='image', id=item.id, width=120, height=120)}" />
    </a>
</p>
% endif

<p>
% for tag in item.tags:
<a href="${h.url_for(controller='medium', action='list_gallery', tag=tag.name)}">${tag.name}</a> 
% endfor
</p>
</%def>

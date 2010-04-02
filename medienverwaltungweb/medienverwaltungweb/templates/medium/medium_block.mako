<%def name="medium_block(item)">
% if item.image_data:
<div style="float:left">
    <img src="${h.url_for(controller='medium', action='image', id=item.id, page=None, type=None, tag=None, return_to=None, width=32, height=32)}">
</div>    
% endif
${item.title}<br>
% for subitem in item.tags:
<a href="${h.url_for(controller='medium', action='list', tag=subitem.name, page=None)}">
    ${subitem.name}
</a>
% endfor
</%def>

<%def name="medium_block(item)">

<div>
    % if item.image_data:
    <div style="float:left;margin:5px;">
##        %if item.tags:
        <img src="${h.url_for(controller='medium', action='image', id=item.id, page=None, type=None, tag=None, return_to=None, width=32, height=32)}">
##        % else:
##        <img src="${h.url_for(controller='medium', action='image', id=item.id, page=None, type=None, tag=None, return_to=None, width=16, height=16)}">
##        % endif
    </div>
    % endif
    <div style="float:left;margin:5px;">
    <a href="${h.url_for(controller='medium', action='edit', id=item.id, page=None)}">
    ${item.title}</a><br>
    
    % for subitem in item.tags:
    <a href="${h.url_for(controller='medium', action='list', tag=subitem.name, page=None)}">
        ${subitem.name}
    </a>
    % endfor
    </div>
</div>

##% if item.image_data:
##<table style="margin-bottom:0;"><tr>
##    <td>
##        <img src="${h.url_for(controller='medium', action='image', id=item.id, page=None, type=None, tag=None, return_to=None, width=32, height=32)}">
##    </td>
##    <td>
##% endif
##    ${item.title}<br>
##    % for subitem in item.tags:
##    <a href="${h.url_for(controller='medium', action='list', tag=subitem.name, page=None)}">
##        ${subitem.name}
##    </a>
##    % endfor
##% if item.image_data:
##    </td>
##</tr></table>
##% endif


##<div>
##    % if item.image_data:
##    ##<div style="float:left">
##    ##    <img src="${h.url_for(controller='medium', action='image', id=item.id, page=None, type=None, tag=None, return_to=None, width=32, height=32)}">
##    ##</div>    
##    <img src="${h.url_for(controller='medium', action='image', id=item.id, page=None, type=None, tag=None, return_to=None, width=32, height=32)}">
##    % endif
##    <span>
##    ${item.title}<br>
##    % for subitem in item.tags:
##    <a href="${h.url_for(controller='medium', action='list', tag=subitem.name, page=None)}">
##        ${subitem.name}
##    </a>
##    % endfor
##    </span>
##</div>
</%def>

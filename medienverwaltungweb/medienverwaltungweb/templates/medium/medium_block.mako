<%def name="medium_block(item)">

<div style='overflow: auto;'>
    % if item.image_data:
    <div style="float:left;margin:5px;">
##        %if item.tags:
        <img src="${h.url_for(controller='image', action='thumbnail', id=item.id, page=None, type=None, tag=None, return_to=None, width=32, height=32)}">
##        % else:
##        <img src="${h.url_for(controller='medium', action='thumbnail', id=item.id, page=None, type=None, tag=None, return_to=None, width=16, height=16)}">
##        % endif
    </div>
    % endif
    <div style="float:left;margin:5px;">
    ##<a href="${h.url_for(controller='medium', action='edit', id=item.id, page=None, type=None, tag=None, return_to=c.return_to)}">
    <a href="${h.url_for(controller='medium', action='edit', id=item.id, return_to=c.return_to, mobile=c.mobile)}">
    ${item.title}</a><br>

    % if not c.mobile:
    % for subitem in item.tags:
    <a href="${h.url_for(controller='medium', action='list', tag=subitem.name, page=None)}">
        ${subitem.name}
    </a>
    % endfor
    % endif
    </div>
</div>

</%def>

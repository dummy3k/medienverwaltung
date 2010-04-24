<%inherit file="/layout-default.mako"/>\

<%def name="title()">${c.title}</%def>

<%def name="content()">
<%namespace name='js_pager' file='../js_pager.mako' />
${js_pager.js_pager(e)}

% if c.without_images:
<p>${ungettext("This medium is not shown, because it has no image:",
               "These media are not shown, because they have no image:",
               c.without_images_cnt)}
%   for index, item in enumerate(c.without_images):
%       if index > 0:
, <a href="${h.url_for(controller='medium', action='edit', id=item.id, type=None, tag=None, page=None)}">
${item.title}</a>\
%       else:
<a href="${h.url_for(controller='medium', action='edit', id=item.id, type=None, tag=None, page=None)}">
${item.title}</a>\
%       endif
%   endfor
</p>
% elif c.without_images_cnt > 0:
<p>${_("%d media are not shown, because they have no image.") % c.without_images_cnt}
   <a href="${h.url_for(controller='medium', action='list_no_image', page=None)}">
   ${_("Show a list of these media.")}
   </a>
</p>
% endif

<p>${c.page.pager(controller='medium', action='list_gallery')}</p>
<p>
% for item in c.page.items:
<a href="${h.url_for(controller='medium', action='index', id=item.id, page=None, type=None, tag=None)}">
<img class="plain" src="${h.url_for(action='image', id=item.id, width=100, height=140, type=None, tag=None, page=None)}" />
</a>
% endfor
</p>
<p>${c.page.pager(controller='medium', action='list_gallery')}</p>

</%def>

<%def name="side()">
	<div class="box">
        <h2>${_("Gallery")}:</h2>
        <ul>
        <li><a href="${h.url_for(action='list', id=None, page=None)}">${_("As List")}</a></li>
        </ul>
	</div>
    % if c.tags:
	<div class="box">
        <h2>${_("Tags")}:</h2>
        <span class="tags">
        % for item in c.tags[:10]:
        <a href="${h.url_for(tag=item[0], page=None)}">${item[0]}&nbsp;(${item[1]})</a>
        % endfor
        </span>
	</div>
    % endif
    % if c.page.page == 1 and c.page.item_count > 14:
	<div class="box">
        <h2>${_("View Options")}:</h2>
        <form id="signin-form" method="post" action="${h.url_for(action='set_view_options', page=None)}">
        <p>${_("Number of images:")} <input name="items_per_page" type="text" size="4" value="${c.page.items_per_page}" /></p>
        <input type="submit" value='${_("Apply")}' class="button"/>
        </form>
	</div>
    % endif
</%def>

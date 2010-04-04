<%inherit file="/layout-default.mako"/>\

<%def name="title()">${c.title}</%def>

<%def name="content()">
<%namespace name='js_pager' file='../js_pager.mako' />
${js_pager.js_pager(e)}

<p>${c.page.pager(controller='medium', action='list_gallery')}</p>

% for item in c.page.items:
<a href="${h.url_for(controller='medium', action='index', id=item.id, page=None, type=None, tag=None)}">
<img class="plain" src="${h.url_for(action='image', id=item.id, width=100, height=175, type=None, tag=None, page=None)}" />
</a>
% endfor

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
</%def>

## -*- coding: utf-8 -*-
<%inherit file="/layout-default.mako"/>\

<%def name="title()">${_("Top Ten Persons")}</%def>

<%def name="content()">

<div style="float:left; position:relative;">
<h2>${_("Actors")}</h2>
<ol>
    % for item in c.actors:
    <li><a href="${h.url_for(action='edit', id=item[0].id)}">${item[0].name}</a> ${item[1]}</li>
    % endfor
</ol>

<a href="${h.url_for(action='list', role='Actor')}">${_("All Actors...")}</a>
</div>

<div style="float:left; position:relative; margin-left: 10px;">
<h2>${_("Directors")}</h2>
<ol>
    % for item in c.directors:
    <li><a href="${h.url_for(action='edit', id=item[0].id)}">${item[0].name}</a> ${item[1]}</li>
    % endfor
</ol>
<a href="${h.url_for(action='list', role='Actor')}">${_("All Directors...")}</a>
</div>

</%def>

## -*- coding: utf-8 -*-
<%inherit file="/layout-default.mako"/>\

<%def name="title()">${_("Top Ten Persons")}</%def>

<%def name="content()">

% if c.actors:
<div class="contentbox">
<h2>${_("Actors")}</h2>
<ol>
    % for item in c.actors:
    <li><a href="${h.url_for(action='edit', id=item[0].id)}">${item[0].name}</a> ${item[1]}x</li>
    % endfor
</ol>

<a href="${h.url_for(action='list', role='Actor')}">${_("All Actors...")}</a>
</div>
% endif

% if c.directors:
<div class="contentbox">
<h2>${_("Directors")}</h2>
<ol>
    % for item in c.directors:
    <li><a href="${h.url_for(action='edit', id=item[0].id)}">${item[0].name}</a> ${item[1]}x</li>
    % endfor
</ol>
<a href="${h.url_for(action='list', role='Actor')}">${_("All Directors...")}</a>
</div>
% endif

% if c.authors:
<div class="contentbox">
<h2>${_("Authors")}</h2>
<ol>
    % for item in c.authors:
    <li><a href="${h.url_for(action='edit', id=item[0].id)}">${item[0].name}</a> ${item[1]}x</li>
    % endfor
</ol>
<a href="${h.url_for(action='list', role='Author')}">${_("All Authors...")}</a>
</div>
% endif

</%def>

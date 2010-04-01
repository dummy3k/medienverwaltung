<%inherit file="/layout-default.mako"/>\

<%def name="title()">Search</%def>

<%def name="content()">
<form id="signin-form" method="post" action="${h.url_for(action='search_post')}">
    <input type="text" name="query"/>
    <input type="submit" value="Find"/>
</form>
</%def>

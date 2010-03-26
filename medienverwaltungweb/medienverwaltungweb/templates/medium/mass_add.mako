<%inherit file="/layout-default.mako"/>\

<%def name="title()">Add Item to DB</%def>

<%def name="content()">
<h1>Add one</h1>

<form id="signin-form" method="post" action="${h.url_for(action='mass_add_post')}">
    <p>Type:
        <select name="media_type">
            <option value="1">DVD</option>
            <option value="2">Book</option>
        </select>
    </p>
    <input type="text" name="title"/>
    <input type="submit" value="Process"/>
</form>

<h1>Add many</h1>

<form id="signin-form" method="post" action="${h.url_for(action='mass_add_post')}">
    <textarea name="title" cols="50" rows="10"></textarea>
    ##<input type="text" name="openid" id="openid" class="openid-identifier" />
    <input type="submit" value="Process"/>
</form>

</%def>

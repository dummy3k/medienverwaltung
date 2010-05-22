<%inherit file="/layout-default.mako"/>\

<%def name="title()">${_("Checkin/checkout with barcode scanner")}</%def>

<%def name="content()">

<p>${_("Enter an isbn each line and press 'Process'.")}<p>

<form id="signin-form" method="post" action="${h.url_for(controller='borrow', action='scanner_post')}">
    <textarea name="isbns" cols="50" rows="10"></textarea>
    <p><input type="submit" value="${_("Process")}" class="button"/></p>
</form>

</%def>

<%inherit file="/layout-default.mako"/>\

<%def name="title()">${c.title}</%def>

<%def name="content()">

<script type="text/javascript">
$(document).ready(function() {
     $(window).keydown(function(event){
        //alert(event.keyCode);
        var current_page = ${c.page.page}
        if (current_page > 1 && event.keyCode == 37) {
            location.href = "${c.prev_link}"
        } else if (event.keyCode == 39) {
            location.href = "${c.next_link}"
##            location.href = 'http://127.0.0.1:5000/medium/list_gallery/page/' + (current_page + 1)
        }

    });
});

</script>

<p>

</p>

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
        <h2>Gallery:</h2>
        <ul>
        <li><a href="${h.url_for(action='list', id=None, page=None, tag=None)}">As List</a></li>
        </ul>
	</div>
</%def>

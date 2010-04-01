<%def name="js_pager(e)">
<script type="text/javascript">
$(document).ready(function() {
     $(window).keydown(function(event){
##        //alert(event.keyCode);
        var current_page = ${c.page.page}
        if (current_page > 1 && event.keyCode == 37) {
            location.href = "${h.url_for(action=c.pager_action, page=int(c.page.page)-1)}"
        } else if (event.keyCode == 39) {
            location.href = "${h.url_for(action=c.pager_action, page=int(c.page.page)+1)}"
        }
    });
});
</script>
</%def>

$(function(){
  // open external links in new window
  $("a[rel^=external]").live('click', function(event) {
    $(this).attr('target', '_blank');
    return event;
  });

  // where query autocomplete
  $('input[name="where"]').autocomplete('/api/autocomplete/where/', {
    dataType: 'json',
    width:  270,
    scrollHeight: 290,
    selectFirst:  false,
    minChars: 1,
    delay: 100,
        parse:  function(data) {
            return $.map(data.response.docs, function (row) {
                return {
                    data: 	row,
                    value: 	row.term,
                    result: row.term + ""
                }
            });
        },
        formatItem: function (row) {
            return row.term;
        }
    }).result(function (e, item) {
    	Site.home.submitForm();
    });

  // initialize routing & history
  window.SiteRoutes = new Routes();
  Backbone.history.start();
});

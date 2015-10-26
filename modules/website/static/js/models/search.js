$(function(){

  window.SearchModel = Backbone.Model.extend({
    url: '/api/search/',
    defaults: {
      query:   {
        page:    1,
        sorting: '_score'
      },
        facets: []
    },

    setParams: function(params) {
      var data = {};

      $.each(params, function(i, item) { 
        data[item.name] = item.value;
      });

      this.set(
        {query: $.extend({}, this.defaults.query, data)},
        {silent: true}
      );

      if (this.hasChanged()) {
        this.trigger('search');
      }
    },

    isEmpty: function() {
      if (this.has('results') && this.get('results').total > 0) {
        return false;
      }

      return true;
    },

    getUrl: function(query) {
      var query = $.extend({}, this.get('query'), query),
        params = '';

      $.each(query, function(name, value) {
        if ($.trim(value).length) {
          if (params.length) {
            params += '&';
          }

          params += name + '='
            + escapeRE(value);
        }
      });

      return params;
    },

    getSearchQuery: function() {
      var query = this.get('query');

      if (query.what && query.where) {
        return query.what + ' / ' + query.where;
      }

      return query.what || query.where;
    }
  });

});

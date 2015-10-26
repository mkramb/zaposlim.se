$(function() {

  window.Routes = Backbone.Router.extend({
    fromHome : true,

    routes : {
      '' : 'home',
      '!zaposlitev?*params' : 'search',
      '!search?*params' : 'searchRedirect',
      '!stats?*params' : 'statsSearches',
      '*default' : 'defaultRoute'
    },

    defaultRoute : function() {
      SiteRoutes.navigate('', true);
    },

    home : function() {
      Site.home.clearParams();
      Site.search.clearParams();
      Site.showHome();

      var document_title = document.title.split(' :: ');
      document.title = document_title[document_title.length - 1];
      this.fromHome = true;

      if (typeof (window['_gaq']) != "undefined") {
        _gaq.push([ '_trackPageview', '' ]);
      }
    },

    searchRedirect : function(params) {
      SiteRoutes.navigate('!zaposlitev?' + params, true);
    },

    search : function() {
      var href = window.location.href,
        hash = '#!zaposlitev?';

      var hasQuery = false,
        params = href.substring(href.indexOf(hash) + hash.length),
        gaurl = 'zaposlitev?' + params;

      params = params.split('&');
      params = $.map(params, function(val, i) {
        var param = decodeURIComponent(val).split('=');
        var validParams = [ 'what', 'where', 'page', 'sorting', 'company.facet' ];

        if (param[0] && param[0].length && param[1] && param[1].length) {
          if ($.inArray(param[0], validParams) >= 0) {
            hasQuery = true;

            return {
              'name' : param[0],
              'value' : $('<div/>').html(param[1]).text()
            };
          }
        }
      });

      if (hasQuery) {
        Site.showSearch();
        Site.search.initParams(params);

        if (typeof (window['_gaq']) != "undefined") {
          if (!this.fromHome)
            window.reloadBanners();
          _gaq.push([ '_trackPageview', gaurl ]);
        }

        this.fromHome = false;
      } else {
        SiteRoutes.navigate('', true);
      }
    },

    statsSearches : function(params) {
      Site.showStatsSearches();

      switch (params) {
        case 'popularna-iskanja': Site.statsSearches.showTop(); break;
        case 'zadnja-iskanja': Site.statsSearches.showLatest(); break;
        default:
          SiteRoutes.navigate('', true);
          break;
      }
    }

  });

});

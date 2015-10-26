$(function(){

  window.StatsQueryModel = Backbone.Model.extend({
    url: '/api/stats/queries/',
    defaults: {
        'top':    [],
        'latest': []
    }
  });

  window.StatsGeoModel = Backbone.Model.extend({
    url: '/api/stats/geo/',
    defaults: {}
  });
  
  window.StatsSearchesModel = Backbone.Model.extend({
    url: '/api/stats/searches/',
    defaults: {}
  });

});

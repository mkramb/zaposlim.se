$(function(){

  window.PagesModel = Backbone.Model.extend({
    url: '/api/pages/',
    defaults: {
      'slug':      null,
        'title':   null,
        'content': null
    }
  });

});

$(function(){

  window.ContactModel = Backbone.Model.extend({
    url: '/api/pages/contact/',
    defaults: {
      'data':    {},
      'success': false
    }
  });

});

$(function(){

  window.SiteView = Backbone.View.extend({
    el: $("#container"),

    initialize: function() {
      this.home = new HomeView().render();
      this.search = new SearchView().render();
      this.statsSearches = new StatsSearchesView().render();
    },

    showHome: function() {
      if (!$(this.home.el).is(":visible")) {
        this.$('footer').addClass('home');

        this.home.el.show();
        this.$('input:visible:first').focus();

        if (Site.home.map) {
          Site.home.map.reload();
        }

        Site.home.addStatsGeo();
      }

      if ($(this.search.el).is(":visible")) {
        this.search.el.hide();
      }

      if ($(this.statsSearches.el).is(":visible")) {
        this.statsSearches.el.hide();
      }
    },

    showSearch: function() {
      if (this.home.el.is(":visible")) {
        this.home.el.hide();
      }
      if (this.statsSearches.el.is(":visible")) {
        this.statsSearches.el.hide();
      }

      if (!$(this.search.el).is(":visible")) {
        this.$('footer').removeClass('home');
        this.search.el.show();
      }
    },

    showStatsSearches: function() {
      if (this.home.el.is(":visible")) {
        this.home.el.hide();
      }
      if (this.search.el.is(":visible")) {
        this.search.el.hide();
      }

      if (!$(this.statsSearches.el).is(":visible")) {
        this.$('footer').removeClass('home');
        this.statsSearches.el.show();
      }
    }
  });

  window.Site = new SiteView;

});

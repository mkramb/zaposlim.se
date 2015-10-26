$(function(){

  window.StatsSearchesView = Backbone.View.extend({
    el: $("#main .stats-searches"),
    template: $('#statsTemplate'),

    events: {
      'click input[type="submit"]': 'submitForm'
    },

    initialize: function() {
      this.model = new StatsSearchesModel();
    },

    render: function() {
      this.el.html($.mustache(this.template.html()));
      return this;
    },
    
    showTop: function() {
      this.model.fetch({
        data: { query: 'top' },
        success: _.bind(this.addDataTop, this)
      });
    },

    showLatest: function() {
      this.model.fetch({
        data: { query: 'latest' },
        success: _.bind(this.addDataLatest, this)
      });
    },

    addDataTop: function() {
      var top = new StatsSearchesItemView({
        model: this.model.toJSON()
      });

      this.$('.stats-title').html(gettext('Popularna iskanja'));
      this.$('#stats-searches').html(top.render().el);

      return this;
    },

    addDataLatest: function() {
      var latest = new StatsSearchesItemView({
        model: this.model.toJSON()
      });

      this.$('.stats-title').html(gettext('Zadnja iskanja'));
      this.$('#stats-searches').html(latest.render().el);

      return this;
    },

    submitForm: function() {
      Site.search.submitForm();
      SiteRoutes.search();
    }
  });

  window.StatsSearchesItemView = Backbone.View.extend({
    template: $('#statsItemTemplate'),

    render: function() {
      $(this.el).html($.mustache(
        this.template.html(), this.model
      ));

      return this;
    }
  });

});

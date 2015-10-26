$(function(){

  window.HomeView = Backbone.View.extend({
    el: $("#main .home"),

    template: $('#homeTemplate'),
    templateStats: $('#homeStatsTemplate'),

    events: {
      'click input[type="submit"]' : 'submitForm'
    },
    
    initialize: function() {
      this.statsGeo = new StatsGeoModel;
      this.statsQuery = new StatsQueryModel;

      this.statsGeo.bind('change', this.addStatsGeo, this);
      this.statsQuery.bind('change', this.addStatsQuery, this);

      this.statsGeo.fetch();
      this.statsQuery.fetch();

      // fetch new data every 2 minute
      window.StatsQuery = this.statsQuery;
      setInterval("StatsQuery.fetch()", (1000 * 60 * 2));
    },

    render: function() {
      this.el.html(this.template.html());
      this.initIntro();

      return this;
    },

    initIntro: function() {
      var intro = this.$('#intro-container');

      $('a', intro).hover(
        function(event) {
          intro.find('#intro div.description').hide();
          intro.find('.'+$(this).attr('class')+'-dsc').stop().fadeTo('normal',1);
        },
        function(event){
          intro.find('#intro div.description').hide();
          intro.find('.default-dsc').fadeTo('normal',1);
        }
      );
    },

    clearParams: function() {
      this.$('input[type="text"]').val('');
      this.$('input:visible:first').focus();
    },

    addStatsQuery: function() {
      var statsTop = new HomeStatsView({model: this.statsQuery.toJSON().top});
      this.$('#sub-search .top').html(statsTop.render().el);

      var statsLatest = new HomeStatsView({model: this.statsQuery.toJSON().latest});
      this.$('#sub-search .latest').html(statsLatest.render().el);

      return this;
    },

    addStatsGeo: function() {
      this.map = new HomeMapView();

      $.each(this.statsGeo.toJSON(), function(i, item) {
        var circle = new google.maps.Circle({
          // visual
          strokeColor:   '#FF0000',
          strokeOpacity: 0.8,
          strokeWeight:  2,
          fillColor:     '#FF0000',
          fillOpacity:   0.35,
          // map
          map:   Site.home.map.canvas,
          center: new google.maps.LatLng(item[3].lat,item[3].lon),
          radius: item[0],
          label:  item[1]
        });

        google.maps.event.addListener(circle, 'click', function(event) {
          SiteRoutes.navigate('!zaposlitev?where=' + circle.label, true);
        });
      });
    },

    submitForm: function() {
      var formData = $('form[name="search"]:visible').serializeArray(),
        hasParams = false,
        params = '';

      $.each(formData, function(i, item) {
        if ($.trim(item.value).length) {
          hasParams = true;

          if (params.length) {
            params += '&';
          }

          params += item.name + '='
            + escapeRE(item.value);
        }
      });

      if (hasParams) {
        SiteRoutes.navigate('!zaposlitev?' + params, true);
      }
    }

  });

  window.HomeStatsView = Backbone.View.extend({
    template: $('#homeStatsTemplate'),

    render: function() {
      $(this.el).html($.mustache(
        this.template.html(),
        { queries: this.model }
      ));

      return this;
    }
  });

  window.HomeMapView = Backbone.View.extend({
    settings : {
      zoom:         7,
      center:         new google.maps.LatLng(46.174125,15.073242),
      mapTypeId:       google.maps.MapTypeId.ROADMAP,
      disableDefaultUI: true
    },

    initialize: function() {
      this.render();
    },

    render: function() {
      this.el = $('#map_canvas');
      this.canvas = new google.maps.Map(this.el.get(0), this.settings);
      this.lock();
    },

    reload: function() {
      google.maps.event.trigger(this.canvas, 'resize');
      this.render();
    },

    lock: function() {
      this.canvas.setOptions({
        disableDoubleClickZoom : true,
        draggable         : false,
        scrollwheel          : false
      });
    },

    unlock: function() {
      this.canvas.setOptions({
        disableDoubleClickZoom : false,
        draggable         : true,
        scrollwheel          : true
      });
    }

  });

  window.HomePagesView = Backbone.View.extend({
    el: $("#pages"),

    events: {
      'click a.static-page': 'requestPage'
    },

    initialize: function() {
      this.model = new PagesModel();
      this.model.bind('change', this.openPage, this);
    },

    requestPage: function(element) {
      var slug = $(element.target).attr('rel');

      if (slug) {
        this.model.fetch({
          data: { slug: slug}
        });
      }

      return false;
    },

    openPage: function() {
      var title = this.model.get('title'),
        content = this.model.get('content');

      if (title && content) {
        $('<div class="modal">' +
          '<h1>' + title + '</h1>' +
          '<div class="modal-static">' + content + '</div>' +
        '</div>')
        .modal({
          overlayClose:true
        });
      }

      this.model.clear({'silent': true});
    }
  });

  window.HomeContactView = Backbone.View.extend({
    el: $("#pages"),

    template: $('#homeContactTemplate'),

    events: {
      'click a.contact-page': 'openContact'
    },

    initialize: function() {
      this.popup = $('<div></div>').html(this.template.html());
      this.model = new ContactModel();

      this.model.bind('change', this.processResult, this);
      this.model.bind('error', this.processError, this);
    },

    openContact: function() {
      $("#contact-form input[type=button]", this.popup).click(function() {
        $("#contact-form", this.popup).submit();
      });

        $("#contact-form", this.popup).validate({
              submitHandler: _.bind(this.submitHandler, this)
        });

        this.popup.modal({
          onClose: this.closePopup,
          overlayClose:true,
            containerCss: {
            height:520,
            width:500
          }
        });

        return false;
    },

    submitHandler: function(form) {
      this.model.set(
        {'data': $(form).serializeArray()},
        {'silent': true}
      );

      this.model.save();
      return false;
    },

    processResult: function() {
      if (this.model.get('success')) {
        $('#form-input', this.popup).hide();
        $('#form-success', this.popup).show();
      } else {
        this.processError();
      }
    },

    processError: function() {
      $('#form-input', this.popup).hide();
      $('#form-error', this.popup).show();
    },

    closePopup: function() {
      $('#form-input', this.popup).show();
      $('#form-success, #form-error', this.popup).hide();
      $('#contact-form', this.popup).clearForm();

      $.modal.close();
    }
  });

  window.pages = new HomePagesView();
  window.contact = new HomeContactView();

});

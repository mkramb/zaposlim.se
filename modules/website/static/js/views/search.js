$(function(){

  window.SearchView = Backbone.View.extend({
    el: $("#main .search"),
    template: $('#searchTemplate'),

    events: {
      'click input[type="submit"]': 'submitForm'
    },

    initialize: function() {
      this.model = new SearchModel;
      this.model.bind('search', this.doSearch, this);
      this.model.bind('change:results', this.addResults, this);
      this.model.bind('change:facets', this.addFacets, this);
    },

    render: function() {
      this.el.html($.mustache(this.template.html()));
      return this;
    },

    addResults: function() {
      this.$('#results .results-info').show();
      this.$('#results .search-term').show();

      if (this.model.isEmpty()) {
        this.$('#results .items').html('');
        this.$('#results .no-results').show();

        this.$('#results .search-term > h1 b').text('');
        this.$('#results .num-results').hide();
        this.$('#results .search-term').hide();

        this.$('#results .num-results > span').text(0);
        this.$('#results .pagination').html('');
        this.$('#results .sorting').hide();

        $('.search-term a.share', this.el).attr('href', '');
      }
      else {
        var results = this.model.get('results');
        var viewResults = new SearchResultsView({model: results.items}),
          viewPagination = new SearchPaginationView({model: results}),
          viewSorting = new SearchSortingView({model: this.model.get('query').sorting});

        this.$('#results .no-results').hide();
        this.$('#results .pagination').hide();

        var searchQuery = this.model.getSearchQuery(), document_title = document.title.split(' :: ');
        document.title = searchQuery + ' :: ' + document_title[document_title.length-1];

        this.addShareLinks();

        this.$('#results .search-term > h1 b').text(searchQuery);
        this.$('#results .num-results > span').text(results.total);

        this.$('#results .sorting span').html(viewSorting.render().el);
        this.$('#results .search-term').show();
        this.$('#results .num-results').show()
        this.$('#results .sorting').show();

        if (this.$('#results .items').text().length > 0) {
          var container = this;

          this.$('#results .items').fadeOut('fast', function() {
            $(this).html(viewResults.render().el).fadeIn('fast', function() {
              container.$('#results .pagination').html(viewPagination.render().el);
              container.$('#results .pagination').show();
            });
          });
        }
        else {
          this.$('#results .items').html(viewResults.render().el);
          this.$('#results .pagination').html(viewPagination.render().el);
          this.$('#results .pagination').show();
        }
      }
    },

    addFacets: function() {
      var view = new SearchFacetsCompanyView({model: this.model.get('facets')});
      this.$('#results-container .filter ul').html(view.render().el);
    },

    clearParams: function() {
      this.$('input[type="text"]').val('');
      this.$('#results-container .filter ul').html('');
      this.$('#results .num-results').hide()
      this.$('#results .pagination').hide();
      this.$('#results .items').html('');

      $('.search-term a.share', this.el).attr('href', '');
      this.model.set(this.model.defaults, {silent: true});
    },

    initParams: function(formData) {
      this.$('input:visible:first').focus();

      var element = this,
        hasParams = false;

      $.each(formData, function(i, item) {
        element.$('input[name="' + item.name + '"]').val(item.value);

        if ($.trim(item.value).length) {
          hasParams = true;
        }
      });

      if (hasParams) {
        this.model.setParams(formData);
      }
    },

    submitForm: function() {
      var formData  = $('form[name="search"]:visible').serializeArray(),
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
        this.model.setParams(formData);
        SiteRoutes.navigate('!zaposlitev?' + params);
      }
    },

    doSearch: function() {
      this.model.unset('facets',  {silent: true});
      this.model.unset('results', {silent: true});
      this.model.save();
    },

    addShareLinks: function() {
      var url_facebook = 'http://www.facebook.com/sharer.php', url_root = getBaseURL(),
        url = url_root + window.location.hash.replace('#', '%23');

      url_facebook += '?u=' + url + '&t=' + escapeRE(document.title);
      $('.search-term a.fb-share', this.el).attr('href', url_facebook);
    }
  });

  window.SearchResultsView = Backbone.View.extend({
    template: $('#searchItemsTemplate'),

    render: function() {
      $(this.el).html($.mustache(
        this.template.html(),
        { items: this.model }
      ));

      return this;
    }
  });

  window.SearchFacetsCompanyView = Backbone.View.extend({
    template: $('#searchFacetsTemplate'),

    render: function() {
      $(this.el).html($.mustache(
        this.template.html(), { facets: this.model['company.facet'] }
      ));

      return this;
    }
  });

  window.SearchPaginationView = Backbone.View.extend({
    template: $('#searchPaginationTemplate'),

    events: {
      'click a': 'scrollTop'
    },

    render: function() {
      if (this.model.total <= 10) {
        $(this.el).html('');
      }
      else {
        $(this.el).html($.mustache(
          this.template.html(), { pagination: this.model.pagination }
        ));
      }

      return this;
    },

    scrollTop: function() {
      $('html, body').animate({ scrollTop: 0}, 0);
    }
  });

  window.SearchSortingView = Backbone.View.extend({
        tagName: 'span',
    template: $('#searchSortingTemplate'),

    data : [
           { selected: true,  field: '_score',        label: gettext('ustreznosti') },
           { selected: false, field: 'published_date', label: gettext('datumu')      }
        ],

    render: function() {
      var selected = this.model;

      $.each(this.data, function(i, item) {
        item.selected = (selected == item.field) ? true : false;
      });

      $(this.el).html($.mustache(
        this.template.html(),{
          sorting:      this.data,
          generateLink: this.generateLink
        }
      ));

      return this;
    },

    generateLink: function() {
      return function(text, render) {
        var sorting = render(text).split('$'),
          url = Site.search.model.getUrl({sorting: sorting[0]});

        return '<a href="#!zaposlitev?' + url + '" class="active">' + sorting[1] + '</a>';
      }
    }
  });
});

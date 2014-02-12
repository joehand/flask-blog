/* ========================================================================
 * AdminView file
 * Author: JoeHand
 * ========================================================================
 */
 
define([
    'backbone',
    'underscore',
    'jquery',
    'views/PostView',
    'models/PostModel',
    's3upload'
], function (Backbone, _, $, PostView, PostModel, S3Upload) {

    DEFAULT_FILTER = flog.DEFAULT_FILTER || { 'kind' : ['article', 'note'], 'published' : [false] };

    var formactive;

    var AdminView = Backbone.View.extend({

        events: {
            'click .post-filter'            : '_filterPosts',
            'focusin .title-input input'    : '_showNewPostSettings',
        },

        _showNewPostSettings: function(e) {
            this.$el.find('.new-post-settings').slideDown().removeClass('hidden');
        },

        _filterPosts: function(e) {
            var $targ = $(e.target),
                newFilter, currentFilter,
                filterKey, filterVal;

            if ($targ.hasClass('button')) {
                newFilter = $targ.data('filter').split(':');
                filterKey = newFilter[0];
                filterVal = newFilter[1];

                currentFilter =  _.clone(this.model.get('filter')); //need to clone to get change event to fire. thanks! http://stackoverflow.com/questions/9909799/backbone-js-change-not-firing-on-model-change

                if (filterKey === 'published') {
                    // convert to boolean
                    filterVal = (filterVal.toLowerCase() === 'true');
                }  
                
                if (_.contains(currentFilter[filterKey], filterVal)) { 
                    currentFilter[filterKey] = _.without(currentFilter[filterKey], filterVal);
                } else {  
                    currentFilter[filterKey] = _.union(currentFilter[filterKey], filterVal);
                }

                $targ.toggleClass('active');
                this.model.set('filter', currentFilter);
            }
        },

        initialize: function(opts) {
            this.model.set('filter', DEFAULT_FILTER);

            this.model.on('change:filter', this.checkFilter, this);

            this.initPosts();
            this.render();
        },

        initPosts: function() {
            var postView, el;
            this.childViews = [];

            this.collection.each(function(model) {
                el = $('*[data-id="' + model.id + '"]').get(0);
                postView = new PostView({model:model, el:el})

                this.childViews.push(postView);
            }, this);

            this.checkFilter();
        },

        render: function() {
            console.log(this);
            return this;
        },

        checkFilter: function() {
            // TODO: if the filter is active make sure button has active class (or other way around?)
            console.log('checking filter');
            var postCount = 0; //TODO: need a better way to do this. maybe make a filtered collection?

            _.each(this.childViews, function(view) {
                if (view.checkFilter(this.model.get('filter'))) {
                    postCount += 1;
                }
            }, this);

            this.$el.find('.post-count .post-num').text(postCount);
        },

    });

    return AdminView;
});
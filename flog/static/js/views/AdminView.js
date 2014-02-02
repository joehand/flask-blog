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
    'models/PostModel'
], function (Backbone, _, $, PostView, PostModel) {

    var DEFAULT_FILTER = {
            'kind' : ['article', 'note'],
            'published' : [false]
        },
        RADIO_CHECK = '&#xe628;',
        RADIO_EMPTY = '&#xe627;';

    var formactive;

    var AdminView = Backbone.View.extend({

        events: {
            'click .post-filter'            : '_filterPosts',
            'focusin .title-input input'    : '_showPostSettings',
            'click .radio-button'           : '_toggleRadio',
        },

        _toggleRadio: function(e) {
            var $targ = $(e.currentTarget);

            if (!$targ.hasClass('active')) {
                $targ.parent().find('.radio-button.active')
                    .removeClass('active')
                    .find('.useicons')
                    .html(RADIO_EMPTY)
                    .parent()
                    .find('input')
                    .attr("checked", false);

                $targ.addClass('active')
                    .find('input')
                    .attr("checked", "checked")
                    .trigger("change") // needed to fire model update from stickit
                    .parent()
                    .find('.useicons')
                    .html(RADIO_CHECK);
            }
        },

        _showPostSettings: function(e) {
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
            this.checkFilter();
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
        },

        render: function() {
            console.log('Admin View rendered');
            console.log(this);
            return this;
        },

        checkFilter: function() {
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
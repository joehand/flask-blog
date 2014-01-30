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


    var PageView = Backbone.View.extend({

        events: {

        },

        initialize: function(options) {
            this.initPosts();
            this.render();
        },

        initPosts: function() {
            var postView, el;
            this.childViews = [];

            _.each(this.collection.models, function(model) {
                el = $('*[data-id="' + model.id + '"]').get(0);
                postView = new PostView({model:model,el:el})

                this.childViews.push(postView);
            }, this);
        },

        render: function() {
            console.log('Page View rendered');
            console.log(this);
            return this;
        },

    });

    return PageView;
});
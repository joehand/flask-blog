/* ========================================================================
 * AdminView file
 * Author: JoeHand
 * ========================================================================
 */
 
define([
    'backbone',
    'underscore',
    'jquery',
    //'medium',
    'views/PostView',
    'models/PostModel',
], function (Backbone, _, $, PostView, PostModel) {


    var PageView = Backbone.View.extend({

        events: {

        },

        initialize: function(options) {
            this.initPosts();
            //this.initMedium();
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

        initMedium: function() {
            new Medium({
                element: document.getElementById('content-editor'),
                debug: true,
                placeholder: "Start Writing!!",
                autofocus: true,
                mode: 'rich', 
            });
            /*
            new Medium({
                element: document.getElementById('title-editor'),
                debug: true,
                mode: 'inline', 
                placeholder: "Enter A Title...",
            });*/
        },

        render: function() {
            console.log('Page View rendered');
            console.log(this);
            return this;
        },

    });

    return PageView;
});
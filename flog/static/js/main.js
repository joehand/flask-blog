/*! =======================================================================
 * Main JS
 * Author: JoeHand
 * ======================================================================== */

define([
    'backbone',
    'jquery',
    'underscore',
    'views/AppView',
    'models/AppModel',
    'models/PostModel',
    'backboneStick',
], function (Backbone, $, _, AppView, AppModel, Posts) {

    var appView, appModel, postsCol, collection;

    appModel = new AppModel({ 
        'user': currentUser 
    });

    collection = _.union(postsBootstrap, pagesBootstrap);

    postsCol = new Posts(collection);

    appView = new AppView({
        model      : appModel,
        collection : postsCol,
        el         : $('#main').get(0),
        childView  : childView
    });
    
});
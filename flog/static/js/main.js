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
        'user': flog.currentUser 
    });

    collection = _.union(flog.postsBootstrap, flog.pagesBootstrap);

    postsCol = new Posts(collection, {url:flog.postURL});

    appView = new AppView({
        model      : appModel,
        collection : postsCol,
        el         : $('#main').get(0),
        childView  : flog.childView
    });
    
});
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

    var appView, appModel, postsCol, collection, NAMESPACE;

    NAMESPACE = flog //for now...

    appModel = new AppModel({ 
        'user': NAMESPACE.currentUser 
    });

    collection = _.union(NAMESPACE.postsBootstrap, NAMESPACE.pagesBootstrap);

    postsCol = new Posts(collection, {url:NAMESPACE.postURL});

    appView = new AppView({
        model      : appModel,
        collection : postsCol,
        el         : $('.document').get(0),
        childView  : NAMESPACE.childView
    });
    
});
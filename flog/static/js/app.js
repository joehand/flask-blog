requirejs.config({
    paths: {
        'jquery'             : 'libs/jquery-2.0.3',
        'underscore'         : 'libs/underscore',
        'backbone'           : 'libs/backbone',
        'backboneStick'      : 'libs/backbone.stickit',
        'backboneDual'       : 'libs/backbone.dualstorage.amd',
        'medium'             : 'libs/medium'
    },
    shim: {
        backbone: {
            deps: ['jquery', 'underscore'],
            exports: 'Backbone'
        },
        backboneStick: {
            deps: ['backbone'],
        },
        backboneDual: {
            deps: ['backbone'],
        },
        underscore: {
            exports: '_'
        },
        medium: {
            exports: 'Medium'
        },
    }
});

// Load the main app module to start the app
requirejs(["main"]);
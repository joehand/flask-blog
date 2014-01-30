requirejs.config({
    paths: {
        'jquery'             : 'libs/jquery-2.0.3',
        'underscore'         : 'libs/underscore',
        'backbone'           : 'libs/backbone',
        'backboneDual'      : 'libs/backbone.dualstorage.amd',
    },
    shim: {
        backbone: {
            deps: ['jquery', 'underscore'],
            exports: 'Backbone'
        },
        backboneDual: {
            deps: ['backbone'],
        },
        underscore: {
            exports: '_'
        }
    }
});

// Load the main app module to start the app
requirejs(["main"]);
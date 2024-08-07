/**
 * letsrolld API
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 *
 */

(function(root, factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD.
    define(['expect.js', process.cwd()+'/src/index'], factory);
  } else if (typeof module === 'object' && module.exports) {
    // CommonJS-like environments that support module.exports, like Node.
    factory(require('expect.js'), require(process.cwd()+'/src/index'));
  } else {
    // Browser globals (root is window)
    factory(root.expect, root.LetsrolldApi);
  }
}(this, function(expect, LetsrolldApi) {
  'use strict';

  var instance;

  beforeEach(function() {
    instance = new LetsrolldApi.Film();
  });

  var getProperty = function(object, getter, property) {
    // Use getter method if present; otherwise, get the property directly.
    if (typeof object[getter] === 'function')
      return object[getter]();
    else
      return object[property];
  }

  var setProperty = function(object, setter, property, value) {
    // Use setter method if present; otherwise, set the property directly.
    if (typeof object[setter] === 'function')
      object[setter](value);
    else
      object[property] = value;
  }

  describe('Film', function() {
    it('should create an instance of Film', function() {
      // uncomment below and update the code to test Film
      //var instance = new LetsrolldApi.Film();
      //expect(instance).to.be.a(LetsrolldApi.Film);
    });

    it('should have the property id (base name: "id")', function() {
      // uncomment below and update the code to test the property id
      //var instance = new LetsrolldApi.Film();
      //expect(instance).to.be();
    });

    it('should have the property title (base name: "title")', function() {
      // uncomment below and update the code to test the property title
      //var instance = new LetsrolldApi.Film();
      //expect(instance).to.be();
    });

    it('should have the property description (base name: "description")', function() {
      // uncomment below and update the code to test the property description
      //var instance = new LetsrolldApi.Film();
      //expect(instance).to.be();
    });

    it('should have the property year (base name: "year")', function() {
      // uncomment below and update the code to test the property year
      //var instance = new LetsrolldApi.Film();
      //expect(instance).to.be();
    });

    it('should have the property rating (base name: "rating")', function() {
      // uncomment below and update the code to test the property rating
      //var instance = new LetsrolldApi.Film();
      //expect(instance).to.be();
    });

    it('should have the property runtime (base name: "runtime")', function() {
      // uncomment below and update the code to test the property runtime
      //var instance = new LetsrolldApi.Film();
      //expect(instance).to.be();
    });

    it('should have the property lbUrl (base name: "lb_url")', function() {
      // uncomment below and update the code to test the property lbUrl
      //var instance = new LetsrolldApi.Film();
      //expect(instance).to.be();
    });

    it('should have the property jwUrl (base name: "jw_url")', function() {
      // uncomment below and update the code to test the property jwUrl
      //var instance = new LetsrolldApi.Film();
      //expect(instance).to.be();
    });

    it('should have the property trailerUrl (base name: "trailer_url")', function() {
      // uncomment below and update the code to test the property trailerUrl
      //var instance = new LetsrolldApi.Film();
      //expect(instance).to.be();
    });

    it('should have the property genres (base name: "genres")', function() {
      // uncomment below and update the code to test the property genres
      //var instance = new LetsrolldApi.Film();
      //expect(instance).to.be();
    });

    it('should have the property countries (base name: "countries")', function() {
      // uncomment below and update the code to test the property countries
      //var instance = new LetsrolldApi.Film();
      //expect(instance).to.be();
    });

    it('should have the property offers (base name: "offers")', function() {
      // uncomment below and update the code to test the property offers
      //var instance = new LetsrolldApi.Film();
      //expect(instance).to.be();
    });

    it('should have the property directors (base name: "directors")', function() {
      // uncomment below and update the code to test the property directors
      //var instance = new LetsrolldApi.Film();
      //expect(instance).to.be();
    });

  });

}));

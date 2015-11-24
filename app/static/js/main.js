/* jshint nomen:true, browser: true */
/* jshint strict: true */
/* global satOligos: true, $, _ */

var satOligos = satOligos || {}; // jshint ignore:line

(function (app) {
	'use strict';

	app.init = function(data) {
		var context = {
				// save the static values in the context
				family: _.sortBy(data.family, function(fam) {
						return fam.name;
					}),
				array: _.sortBy(data.array, function(arr) {
						return arr.name;
					}),
				oligoCount: data.oligoCount,
				population_total: _.sortBy(data.population_total, function(pop) {
						return pop.order;
					}),
				populationGrandTotal: _.reduce(data.population_total, function (sum, pop) {
					return pop.count + sum;
				}, 0)
			};
		app.search(context);
	};
	
	$(document).ready(function () {
		//$.preloadCssImages();
		$.ajax({
			type: 'GET',
			url: '/app/init/',
			dataType: "json",
			success: app.init,
			cache: true
		});
	});
})(satOligos);

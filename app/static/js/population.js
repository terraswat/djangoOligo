/* jshint nomen:true, browser: true */
/* jshint strict: true */
/* global satOligos: true, $, _ */

var satOligos = satOligos || {}; // jshint ignore:line

(function (app) {
	'use strict';

	var $headerRow = $('#populations tr:first-child'),
		$dataRow = $('#populations tr:last-child');

	app.population = function(context, primer) {

		var myData;

		function appendDetail(total) {
			var dataPop = _.find(myData, function (dataPop) {
					return (dataPop.name === total.name);
				}),
				count = dataPop ? dataPop.count : 0;
			$headerRow.append('<th title="' + total.descr + '">' + total.name + ' (' + total.count + ')');
			$dataRow.append('<td title="' + total.descr + '">' + count);
		}

		function receiveData(data) {
			var oligoSum = _.reduce(data, function (sum, pop) {
						return pop.count + sum;
					},
				0);
			myData = data;
			$headerRow.empty();
			$dataRow.empty();
			$headerRow.append('<th>Total (' + context.populationGrandTotal + ')');
			$dataRow.append('<td>' + oligoSum);

			_.each(context.population_total, appendDetail);
			$('#populations').show();
		}

		$.ajax({
			type: 'GET',
			url: '/app/populations/',
			data: {primer: primer},
			dataType: "json",
			success: receiveData,
			cache: true
		});
	};
})(satOligos);

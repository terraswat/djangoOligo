/* jshint nomen:true, browser: true */
/* jshint strict: true */
/* global satOligos: true, $, _ */

var satOligos = satOligos || {}; // jshint ignore:line

(function (app) {
	'use strict';

	var oligoDataTable,
		first = true;

	app.oligo = function(context, filter) {

		var $oligos = $('#oligos'),
			$stats = $('#oligos .stats');

		function addCommas(nStr) {
			var x, x1, x2, rgx;
			nStr += '';
			x = nStr.split('.');
			x1 = x[0];
			x2 = x.length > 1 ? '.' + x[1] : '';
			rgx = /(\d+)(\d{3})/;
			while (rgx.test(x1)) {
				x1 = x1.replace(rgx, '$1' + ',' + '$2');
			}
			return x1 + x2;
		}

		function rowClick(ev) {
			var $target = $(ev.currentTarget),
				primer = $target.children('td:first-child').text(),
				$gb = $('#genomeBrowser'),
				color = 'grey';
				// oligo = _.find(oligos, function (row) {
				//		return row.primer === primer;
				// });
				// color = oligo.url.length // TODO
				//	? 'black'
				//	: 'grey';
			$target.parent().children().removeClass('selected'),
			$target.addClass('selected');
			$gb.css('color', color);
			$gb.show();
			app.population(context, primer);
			app.comment(primer);
		}

		function receiveData(data) {
			var tableData = _.map(data, function (r) {
					return [
						r.primer,
						Array(r.rating + 1).join("*"),
						r.family,
						r.array,
						r.frequency,
						r.chr,
						addCommas(r.bestStart),
						addCommas(r.bestEnd),
						r.location
					];
				});
				/*
				statsText = '' + tableData.length + ' displayed of '
					+ tableData.length + ' matches of '
					+ context.oligoCount + ' in database';
				*/
			//context.oligos = data.oligos;
			//context.rowsMatched = data.rowsMatched; // needed?
			$stats.text(
				'' + tableData.length + ' displayed of '
				//+ data.rowsMatched + ' matches of ' // TODO use this instead
				+ tableData.length + ' matches of '
				+ context.oligoCount + ' in database'
			);

			if (first) {
				first = false;
				$oligos.show();
				oligoDataTable = $('#oligoTable').dataTable( {
					"data": tableData,
					"paging": false,
					"searching": false,
					"info": false,
					//"scrollY": "100px",
					"scrollY": "200px",
					"scrollCollapse": true,
					"columns": [
						{ "title": "Primer (5'-> 3')" },
						{ "title": "Rating" },
						{ "title": "Satellite Family" },
						{ "title": "Array Name" },
						{ "title": "Freq." },
						{ "title": "Chr." },
						{ "title": "Best Start" },
						{ "title": "Best End" },
						{ "title": "Location w/10% le..." }
					]
				} );
				$oligos.on('click', 'table.dataTable tbody tr', rowClick);
			} else {
				oligoDataTable.fnClearTable();
				oligoDataTable.fnAddData(tableData);
			}
		}

		// Request filtered oligos from server
		$.ajax({
			type: 'GET',
			url: '/app/oligos/',
			data: filter,
			dataType: "json",
			success: receiveData,
			cache: true
		});
	};
})(satOligos);

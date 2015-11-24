/* jshint nomen:true, browser: true */
/* jshint strict: true */
/* global satOligos: true, $, _ */

var satOligos = satOligos || {}; // jshint ignore:line

(function (app) {
	'use strict';

	var first = true,
		$thead = $('#comments .table thead'),
		$tbody = $('#comments .table tbody'),
		$createButton = $('#comments .createButton'),
		$addButton = $('#comments .addButton'),
		$addBlock = $('#comments .addBlock'),
		$ratingInput = $('#comments .ratingInput'),
		$textInput = $('#comments .textInput'),
		$error = $('#comments .error'),
		buildStars;

	buildStars = function (num) {
		var rating = '';
		for (var i = 0; i < num; i+=1) {
			rating += '*';
		}
		return rating;
	}

	app.comment = function(primer) {

		var noComments = true,
			returnPressed = false;

		function createClick(ev) {
			$ratingInput.val(3);
			$textInput.val('');
			$thead.show();
			$ratingInput.select2({
				minimumResultsForSearch: -1, // search never
				dropdownCssClass: 'ratingDropDown',
				dropdownAutoWidth: true,
			});
			$createButton.hide();
			$addBlock.show();
			$textInput.focus();
		}

		function ratingChange() {
			$textInput.focus();
		}

		function textKeyup(ev) {
			// two clicks on the return key will cause a click of the add button
			if (ev.keyCode === 13) {
				if (returnPressed) {
					$addButton.focus().click();
					returnPressed = false;
				} else {
					returnPressed = true;
				}
			} else {
				returnPressed = false;
			}
		}

		function appendDetail(comment) {
			var rating = buildStars(comment.rating);
			$tbody.append('<tr><th>' + rating + '<td>' + comment.text);
			noComments = false;
		}

		function receiveData(dataIn) {
			var data = dataIn.data,
				myPrimer = dataIn.primer,
				noCommentText = 'Be the First to Rate & Comment',
				commentText = 'Rate & Comment',
				currentPrimer = $('#oligoTable tr.selected td:first-child').text();
			$addBlock.hide();
			$tbody.empty();
			if (myPrimer !== currentPrimer) {
				$error.show();
				$createButton.hide();
				$('#comments').show();
			} else {
				$error.hide();
				_.each(data, appendDetail);
				if (first) {
					first = false;
					$createButton.button();
					$addButton.button();
					$('#comments')
						.show()
						.on('click', '.createButton', createClick)
						.on('change', '.ratingInput', ratingChange)
						.on('keyup', '.textInput', textKeyup)
						.on('click', '.addButton', { primer: myPrimer }, addClick);
				}
				$createButton.show();
			}
			$createButton.find('span').text(noComments ? noCommentText : commentText);
		}

		function addClick(ev) {
			$.ajax({
				type: 'GET',
				url: '/app/addComment/',
				data: {
						primer: ev.data.primer,
						rating: $ratingInput.val(),
						text: $textInput.val()
					},
				dataType: "json",
				success: receiveData,
				cache: true
			});
		}

		$.ajax({
			type: 'GET',
			url: '/app/comments/',
			data: {primer: primer},
			dataType: "json",
			success: receiveData,
			cache: true
		});
	}
})(satOligos);

/* jshint nomen:true, browser: true */
/* jshint strict: true */
/* global satOligos: true, $, _ */

var satOligos = satOligos || {}; // jshint ignore:line

(function (app) {
	'use strict';

	var $search,
		$family,
		$chr,
		$population,
		$array,
		$primer,
		$help,
		$button,
		filter = {};

	app.search = function(context) {

		function helpClick(ev) {
			window.open('./help');
		}

		function buttonClick(ev) {
			filter = {};
			/* todo, probably don't want this
			var chrVal = $chr.val();
			filter.chr = (chrVal.length > 0)
				?'chr' + $chr.val()
				: '';
			filter.family = $family.val();
			*/
			var val = $family.select2('val');
			if (val !== 'Any') {
				filter.family = val;
			}
			val = $chr.select2('val');
			if (val !== 'Any') {
				filter.chr = val;
			}
			val = $population.select2('val');
			if (val !== 'Any') {
				filter.population = val;
			}
			val = $array.select2('val');
			if (val !== 'Any') {
				filter.array = val;
			}
			val = $primer.val();
			if (val.length) {
				filter.primer = val;
			}
			app.oligo(context, filter);
			$button
				.blur()
				.removeClass('ui-state-focus')
				.removeClass('ui-state-hover')
				.addClass('ui-state-active');
		}

		function textKeyup(ev) {
			if (ev.keyCode === 13) { // return key pressed
				$button.focus().click();
			}
			// TODO only allow TCGAtcga in this field?
		}

		function familyChange() {
			$chr.find('.select2-focusser').focus();
		}

		function chrChange() {
			$population.find('.select2-focusser').focus();
		}

		function populationChange() {
			$array.find('.select2-focusser').focus();
		}

		function arrayChange() {
			$primer.focus();
		}

		function setSelect2height() {
			var results = $('#select2-drop .select2-results');
			results.css('max-height', $(window).height() - results.offset().top - 10);
		}

		function createSelect2(klass, data, placeholder) {
			var dropDown = $('#search .' + klass).select2({
				data: data,
				val: 'Any',
				placeholder: placeholder,
				minimumResultsForSearch: 7,
				dropdownAutoWidth: true,
				dropdownCssClass: klass + 'DropDown'
			});
			dropDown.select2('val', 'Any');
		}

		function createDropDowns() {
			var familyData = [{ id: 'Any', text: 'Any' }].concat(_.map(context.family, function (opt) {
					var text = opt.name;
					return { id: opt.name, text: opt.name };
				})),
				chrOpts = _.range(1, 22).concat('X', 'Y'),
				chrData = [{ id: 'Any', text: 'Any' }].concat(_.map(chrOpts, function (opt) {
					return { id: opt.toString(), text: 'chr' + opt };
				})),
				arrayData = [{ id: 'Any', text: 'Any' }].concat(_.map(context.array, function (opt) {
					var text = opt.name;
					return { id: opt.name, text: opt.name };
				})),
				populationData = [{ id: 'Any', text: 'Any' }],
				lastGroup = '',
				children = [],
				i = 0;
			_.each(context.population_total, function (opt) {
				if (opt.group !== lastGroup) {
					if (lastGroup !== '') {
						populationData.push({
							id: i,
							text: lastGroup,
							disabled: true,
							children: children
						});
						children = [];
						i += 1;
					}
					lastGroup = opt.group;
				}
				children.push({
					id: opt.name,
					text: opt.name + ' (' + opt.count + '): ' + opt.descr
				});
			});
			populationData.push({
				id: i,
				text: lastGroup,
				children: children
			});
			createSelect2('family', familyData, 'Any');
			createSelect2('chr', chrData, 'Any');
			createSelect2('population', populationData, 'Any');
			createSelect2('array', arrayData, 'Any');
		}

		function convenientVars() {
			$search = $('#search');
			$family = $('#search .family.select2-container');
			$chr = $('#search .chr.select2-container');
			$population = $('#search .select2-container.population');
			$array = $('#search .array.select2-container');
			$primer = $('#search .primer');
			$help = $('#help');
			$button = $('#search .button');
		}

		createDropDowns();
		convenientVars();
		$search
			.on('change', '.family', familyChange)
			.on('change', '.chr', chrChange)
			.on('change', '.population', populationChange)
			.on('change', '.array', arrayChange)
			.on('keyup', '.primer', textKeyup);
		$('.select2-container.family').parent().on('select2-open', setSelect2height);
		$('.select2-container.chr').parent().on('select2-open', setSelect2height);
		$('.select2-container.population').parent().on('select2-open', setSelect2height);
		$('.select2-container.array').parent().on('select2-open', setSelect2height);
		$help.button().on('click', helpClick);
		$button.button().on('click', buttonClick);
		$search.css('display', 'inline-block');
		$family.focus();
	};
})(satOligos);

/* global partial: true, connect: true, hasElementClass: true */

//////////////////
//////////////////
/// global scope:
var steps = {};
var game_state = {};
var nav_ready = false;

var observation_css_classes = [
    'observation_1', 'observation_2', 'observation_3', 'observation_4'];

var criteria_css_classes = [
    'criteria_1', 'criteria_2', 'criteria_3'];

var first_round_action_css_classes = [
    'first_round_action_1',
    'first_round_action_2',
    'first_round_action_3',
    'first_round_action_4'];

var second_round_action_css_classes = [
    'second_round_action_1',
    'second_round_action_2',
    'second_round_action_3',
    'second_round_action_4'];

//////////////////
//////////////////

function observation_checkbox_connect(c) {
    connect(c, 'onclick', observation_checkbox_clicked);
}

function criteria_checkbox_connect(c) {
    connect(c, 'onclick', criteria_checkbox_clicked);
}

function other_observations_textfield_connect(f) {
    connect(f, 'onchange', textfield_changed);
}

function textfield_changed(e) {
    var contents = e.src().value;
    map(partial(set_contents, contents), $$('.other_observations'));
}

function observation_checkbox_clicked(e) {
    var mirror_observation_checkboxes = partial(mirror_checkboxes,
        observation_css_classes);
    mirror_observation_checkboxes(e);
}

function criteria_checkbox_clicked(e) {
    var mirror_criteria_checkboxes = partial(mirror_checkboxes,
        criteria_css_classes);
    mirror_criteria_checkboxes(e);
}

// these functions form a mini-library that allows you to do the following:
// give matching css classes e.g. observation_css_classes to a set of checkboxes that reoccur several times
// on the page. whenever the user checks one of the set, the corresponding ones anywhere will be checked too.

function set_checked(checkedness, box) {
    box.checked = checkedness;
}

function set_contents(contents, textarea) {
    textarea.value = contents;
}

function mirror_checkboxes(relevant_css_classes, e) {
    var which_class = which_of_these_css_classes(e.src(), relevant_css_classes);
    var checkedness = e.src().checked;
    var set_to_same = partial(set_checked, checkedness);
    map(set_to_same, $$('.' + which_class));
}

function defined(x) {
    return x !== undefined;
}

function which_of_these_css_classes(the_div, classes_arr) {
    // classes_arr is a list of css_classes which this element might have.
    // return the first class that this element has..
    var temp = map(function(the_class) {
        if (hasElementClass(the_div, the_class)) {
            return the_class;
        }
    }, classes_arr);

    var temp2 = filter(defined, temp);
    if (temp2.length > 0) {
        return temp2[0];
    }
}

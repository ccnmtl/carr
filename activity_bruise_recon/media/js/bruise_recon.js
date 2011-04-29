function debug(string)
{
    if (false)
      log("DEBUG " + string)
}


function validate() {
    // make sure either yes or no is selected.
    return (
        hasElementClass($('answer_yes'), 'button_selected')
            || hasElementClass($('answer_no'), 'button_selected'));
}


function maybeEnableNext()
{
   gonext = false;

   if (validate()) {
    gonext = true;
   }
   
   if (gonext){
      if ($('next') != null) {
        setStyle('next', {'display': 'inline'});
      }
    }
    else  {
        if ($('next') != null ) {
             setStyle('next', {'display': 'none'});
        }
        disable_all_sidenav_items_after_current_one();
    }
    
}


function disable_all_sidenav_items_after_current_one() {
    all_sidenav_items =  $$('#sidebar_left ul li')
    selected_sidenav_item =  $$('#sidebar_left ul li.selected')[0]
    all_sidenav_items.slice(all_sidenav_items.indexOf(selected_sidenav_item) + 1)
    sidenav_items_to_disable = all_sidenav_items.slice(all_sidenav_items.indexOf(selected_sidenav_item) + 1)
    forEach (sidenav_items_to_disable, disable_sidenav_item);
}

function disable_sidenav_item (item) {
    forEach(getElementsByTagAndClassName('a', null, item), hideElement)
    forEach(getElementsByTagAndClassName('span', null, item), showElement)
}



function loadStateSuccess(doc)
{
   debug('loadStateSuccess')
   case_name =  $('case_name').innerHTML.trim();

   if (doc && doc[case_name])
   {
     state_for_this_page = doc[case_name];
     //logDebug (serializeJSON(state_for_this_page));
     // if state is already saved you can't change your answers.
     if ( typeof(state_for_this_page['answered']) != "undefined") {
       debug ("already answered");
       lock_down_answer_buttons();
     }
   }
   else {
     state_for_this_page = {}
   }
   if (state_for_this_page['answered']) {
        if (state_for_this_page['answered'] == 'yes') {
            addElementClass($('answer_yes'), 'button_selected');
        }
        else if (state_for_this_page['answered'] == 'no') {
            addElementClass($('answer_no'), 'button_selected');
        }
    }
   if (state_for_this_page['factors']) {
        factors_as_string = state_for_this_page['factors'].join (',');
        logDebug (factors_as_string);
   }
   if (typeof (factors_as_string)  != "undefined") {
     if (factors_as_string.match(/patterns/) != null) {
              addElementClass($('patterns'), 'button_selected');
     }
     if (factors_as_string.match(/severity/) != null) {
              addElementClass($('severity'), 'button_selected');
     }
     if (factors_as_string.match(/location/) != null) {
              addElementClass($('location'), 'button_selected');
     }
     if (factors_as_string.match(/explanation/) != null) {
              addElementClass($('explanation'), 'button_selected');
     }
   }
   /*
   if (state_for_this_page != null && keys(state_for_this_page).length > 0) {
   }
   */
   // adding this: show correct answer for completed quizzes.
   if (validate()) {
     show_answer();
   }
   maybeEnableNext();
}

function loadStateError(err)
{
   debug("loadStateError")
   // @todo: Find a spot to display an error or decide just to fail gracefully
   // $('errorMsg').innerHTML = "An error occurred loading your state (" + err + "). Please start again."
}

function loadState()
{
    if (typeof student_response != "undefined") {
        loadStateSuccess(student_response);
        if (validate()) {
          show_answer();
        }
        return;
    }

   url = 'http://' + location.hostname + ':' + location.port + "/activity/bruise_recon/load/"
   deferred = loadJSONDoc(url)
   deferred.addCallbacks(loadStateSuccess, loadStateError)

   hide_answer();

   //alert ("making buttons clickable.");

   //if (state_for_this_page != null && keys(state_for_this_page).length > 0) {
       //yes/no behaves like a set of radio buttons
      connect ('answer_yes', 'onclick', partial (like_radio, 'button_selected', 'answer_button', 'answer_yes'));
      connect ('answer_no',  'onclick', partial (like_radio, 'button_selected', 'answer_button', 'answer_no' ));


      // factors behaves like a set of checkboxes.
      connect ('patterns',     'onclick', partial (like_checkbox, 'button_selected', 'bruise_recon_checkbox_div', 'patterns'));
      connect ('severity',     'onclick', partial (like_checkbox, 'button_selected', 'bruise_recon_checkbox_div', 'severity'));
      connect ('location',     'onclick', partial (like_checkbox, 'button_selected', 'bruise_recon_checkbox_div', 'location'));
      connect ('explanation',  'onclick', partial (like_checkbox, 'button_selected', 'bruise_recon_checkbox_div', 'explanation'));

      connect('submit_div', 'onclick', show_answer);
  //}

  maybeEnableNext();

}


function like_radio(selected_class, all_button_class, the_element) {
    map (function(a) {removeElementClass( a,selected_class);}, $$('.' + all_button_class))
    addElementClass( $(the_element), selected_class);
}



function like_checkbox(selected_class, all_button_class, the_element) {
    toggleElementClass( selected_class, $(the_element));
}



function lock_down_answer_buttons() {
  debug ("locking down answer buttons");
  forEach ($$('.answer_button'), disconnectAll);
  forEach ($$('.bruise_recon_checkbox_div'), disconnectAll);
  forEach ($$('#submit_div'), disconnectAll);
}



function hide_answer()
{
    hideElement('feedback_div');
}


function numeric(field) {
    var regExpr = new RegExp("^[0-9]$");
    if (!regExpr.test(field.value))
    {
      // Case of error
      field.value = "";
    }
}


function answer_is_correct() {

    answer_is_yes = ($('correct_answer').innerHTML.toLowerCase().match(/yes/))
    factors_include_severity = ($('correct_factors').innerHTML.toLowerCase().match(/severity/))
    factors_include_location = ($('correct_factors').innerHTML.toLowerCase().match(/location/))
    factors_include_patterns = ($('correct_factors').innerHTML.toLowerCase().match(/patterns/))
    factors_include_explanation = ($('correct_factors').innerHTML.toLowerCase().match(/explanation/))

    if (answer_is_yes) {
        if (hasElementClass($('answer_no'), 'button_selected')) { return false };
    }
    else {
        if (hasElementClass($('answer_yes'), 'button_selected')) { return false };
    }

    logDebug ("yes no answer is correct");
    if (factors_include_severity) {
        if (! hasElementClass($('severity'), 'button_selected')) { return false };
    }
    if (factors_include_location) {
        if (! hasElementClass($('location'), 'button_selected')) { return false };
    }
    if (factors_include_patterns) {
        if (! hasElementClass($('patterns'), 'button_selected')) { return false };
    }
    if (factors_include_explanation) {
        if (! hasElementClass($('explanation'), 'button_selected')) { return false };
    }


    if (!factors_include_severity) {
        if (hasElementClass($('severity'), 'button_selected')) { return false };
    }
    if (!factors_include_location) {
        if (hasElementClass($('location'), 'button_selected')) { return false };
    }
    if (!factors_include_patterns) {
        if (hasElementClass($('patterns'), 'button_selected')) { return false };
    }
    if (!factors_include_explanation) {
        if (hasElementClass($('explanation'), 'button_selected')) { return false };
    }



    //patterns, severity, body location, explanation credibility
    logDebug ("ok factors are exactly correct too");
    return true;

}

function show_answer() {
    debug ("show answer");
    if (!validate()) {
        alert ("Please choose yes or no.");
        return;
    }
    hideElement ('submit_div');
    if (answer_is_correct()) {
        $("your_answer_was").innerHTML = "Your answer is correct.";
    }
    else {
        $("your_answer_was").innerHTML = "Your answer is incorrect.";

    }
    showElement ('feedback_div');
    lock_down_answer_buttons()
    maybeEnableNext();
}



MochiKit.Signal.connect(window, "onload", loadState)
//MochiKit.Signal.connect(window, "onload", setfocus)

function saveState()
{
   if (typeof student_response != "undefined") {
      return;
   }

   case_name =  $('case_name').innerHTML.trim();

   url = 'http://' + location.hostname + ':' + location.port + "/activity/bruise_recon/save/"

   debug("saveState");
   doc = {}

   if (hasElementClass($('answer_yes'), 'button_selected')) {
        doc ['answered'] = 'yes';
   }

   if (hasElementClass($('answer_no'), 'button_selected')){
        doc ['answered'] = 'no';
   }

   doc ['factors'] = []
   if (hasElementClass($('severity'),    'button_selected')) { doc ['factors'].push (   'severity') };
   if (hasElementClass($('location'),    'button_selected')) { doc ['factors'].push (   'location') };
   if (hasElementClass($('patterns'),    'button_selected')) { doc ['factors'].push (   'patterns') };
   if (hasElementClass($('explanation'), 'button_selected')) { doc ['factors'].push ('explanation') };

   if (answer_is_correct()) {
        doc['score'] = 1;
   }
   else {
        doc['score'] = 0;
   }

  var sync_req = new XMLHttpRequest();
  sync_req.onreadystatechange= function() { if (sync_req.readyState!=4) return false; }
  sync_req.open("POST", url, false);

  what_to_send = {}
  what_to_send [case_name ] = doc

  sync_req.send(queryString({'json':JSON.stringify(what_to_send , null)}));

}

// TODO fix this:
MochiKit.Signal.connect(window, "onbeforeunload", saveState)


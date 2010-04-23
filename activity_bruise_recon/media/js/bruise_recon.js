function debug(string)
{
    if (false)
      log("DEBUG " + string)
}


function maybeEnableNext()
{
   gonext = false
 
   if (validate()) {
    gonext = true;
   }
   
   
   
   if (gonext){
         setStyle('next', {'display': 'inline'}) 
   }
  else
  {
     setStyle('next', {'display': 'none'}) 
  }
}



/*
function connectCallouts()
{
   if (getElement("dosage_2"))
   {
      connectCalloutsDouble()
   }
   else
   {  
      connectCalloutsSingle()
   }
}

function connectCalloutsDouble()
{
   vertical_line(getElement('dosage_callout'), getElement('dosage'))
   vertical_line(getElement('disp_callout'), getElement('disp'))
   vertical_line(getElement('refills_callout'), getElement('refills'))
}

function connectCalloutsSingle()
{
   vertical_line(getElement('dosage_callout'), getElement('dosage'))
   vertical_line(getElement('disp_callout'), getElement('disp'))
   vertical_line(getElement('refills_callout'), getElement('refills'))
   
}

function horizontal_line(topElement, bottomElement)
{
   bottomPos = getElementPosition(bottomElement)
   bottomDim = getElementDimensions(bottomElement)
   
   topPos = getElementPosition(topElement)
   topDim = getElementDimensions(topElement)
   
   fromx = topPos.x + topDim.w/2
   fromy = topPos.y + topDim.h
   tox = bottomPos.x + bottomDim.w/2
   toy = bottomPos.y
   drawlines(fromx, fromy, tox, toy, fromx)

}

function vertical_line(leftElement, rightElement)
{
   x = getElementPosition(leftElement).x + getElementDimensions(leftElement).w
   x2 = getElementPosition(rightElement).x
   y = getElementPosition(rightElement).y + getElementDimensions(rightElement).h/2
   
   drawlines(x, y, x2, y, x2)
}

function drawlines (from_x, from_y, to_x, to_y, x_break) {
    // make the left hline go all the way to the right edge of the center vline. Add 2 pixels, if necessary.
    var extra = ( from_y > to_y )? 2 : 0; 
    hline (from_x, x_break + extra, from_y);
    vline (from_y, to_y, x_break);
    hline (x_break, to_x, to_y );
}

function hline (from, to, y) {
    if (from > to) { var temp = to; to = from; from = temp; }
    var newdiv = DIV ( {"class":"connecting_line" });
    appendChildNodes(currentDocument().body, newdiv);
    setStyle( newdiv , { "left": from + 'px', "top" : y + 'px' , "width" : (to - from) + "px", "height" : "2px"});
}

function vline (from, to, x) {
    if (from > to) { var temp = to; to = from; from = temp; }
    var newdiv = DIV ( {"class":"connecting_line" });
    appendChildNodes(currentDocument().body, newdiv);
    setStyle( newdiv , { "left": x + 'px', "top" : from + 'px' , "height" : (to - from) + "px", "width" : "2px"});
}

function setBackgroundColor(ctrl)
{
   if (ctrl.value.length > 0)
   {
      setStyle(ctrl.id, { 'background-color': 'white' })
   }
   else
   {
      setStyle(ctrl.id, { 'background-color': '#f8db9f' })
   }
}

function onEditChange(ctrl)
{
   setBackgroundColor(ctrl)
   maybeEnableNext()
}


function loadStateSuccess(doc)
{
   debug('loadStateSuccess')
   
   if (doc && doc[$('medication_name').value])
   {
      rx = doc[$('medication_name').value]
      $('dosage').value = rx['dosage']
      $('disp').value = rx['disp']
      $('sig').value = rx['sig']
      $('refills').value = rx['refills']
                              
      if ($('dosage_2'))
      {
         $('dosage_2').value = rx['dosage_2']
         
         $('disp_2').value = rx['disp_2']
         
         $('sig_2').value = rx['sig_2']
         
         $('refills_2').value = rx['refills_2']
      }
   }
                                                                                                                                                                       
   setBackgroundColor($('dosage'))
   setBackgroundColor($('disp'))
   setBackgroundColor($('sig'))
   setBackgroundColor($('refills'))
   
   if ($('dosage_2'))
   {
      setBackgroundColor($('dosage_2'))
      setBackgroundColor($('disp_2'))
      setBackgroundColor($('sig_2'))
      setBackgroundColor($('refills_2'))
   }
   
  if ($('dosage_correct'))
     connectCallouts()
     
  maybeEnableNext()
}

function loadStateError(err)
{
   debug("loadStateError")
   // @todo: Find a spot to display an error or decide just to fail gracefully
   // $('errorMsg').innerHTML = "An error occurred loading your state (" + err + "). Please start again."
}
*/

//aasd = partial (like_checkbox, 'button_selected', 'bruise_recon_checkbox_div', 'patterns'      )
  
  
  /* if (!$('dosage_correct'))
   {
      setStyle('next', {'display': 'none'})
   }
   url = 'http://' + location.hostname + ':' + location.port + "/activity/prescription/load/"
   deferred = loadJSONDoc(url)
   deferred.addCallbacks(loadStateSuccess, loadStateError)

}
*/

/*
.button_selected {
   background-color: #efc48d;
}

<div id="answer_yes" class="answer_button">Yes</div>
*/

  
  
  /*
  
  connect ('patterns',       'onclick', partial (like_checkbox, 'button_selected', 'bruise_recon_checkbox_div', 'patterns'      ))
  connect ('severity',       'onclick', partial (like_checkbox, 'button_selected', 'bruise_recon_checkbox_div', 'severity'      ))
  connect ('body_location',  'onclick', partial (like_checkbox, 'button_selected', 'bruise_recon_checkbox_div', 'body_location' ))
  connect ('credibility',    'onclick', partial (like_checkbox, 'button_selected', 'bruise_recon_checkbox_div', 'credibility'   ))
  */
  
  //connect ('patterns',  'onclick', partial (toggleElementClass, 'patterns',  'button_selected'));
  

function loadState()
{
   debug("loadState")
   hide_answer();
   
   
  connect ('answer_yes', 'onclick', partial (like_checkbox, 'button_selected', 'answer_button', 'answer_yes'))
  connect ('answer_no',  'onclick', partial (like_checkbox, 'button_selected', 'answer_button', 'answer_no'))
  
  
  connect ('patterns',      'onclick', partial (toggleElementClass,'button_selected',       'patterns' ));
  connect ('severity',      'onclick', partial (toggleElementClass,'button_selected',       'severity' ));
  connect ('location', 'onclick', partial (toggleElementClass,'button_selected',  'location' ));
  connect ('explanation',   'onclick', partial (toggleElementClass,'button_selected',    'explanation' ));

  connect('submit_div', 'onclick', show_answer);

  maybeEnableNext();
}


function like_checkbox(selected_class, all_button_class, the_element) {
    map (function(a) {removeElementClass( a,selected_class);}, $$('.' + all_button_class))
    addElementClass( $(the_element), selected_class);
}


//toggleElement
function hide_answer()
{
    hideElement('feedback_div');
/*
   if (!$('dosage_correct'))
      $("dosage").focus()
      */
}


function numeric(field) {
    var regExpr = new RegExp("^[0-9]$");
    if (!regExpr.test(field.value)) 
    {
      // Case of error
      field.value = "";
    }
}

function validate() {
    // make sure either yes or no is selected.
    return (
        hasElementClass($('answer_yes'), 'button_selected')
            || hasElementClass($('answer_no'), 'button_selected'));
}


function answer_is_correct() {
   
    answer_is_yes = ($('correct_answer').innerHTML.toLowerCase().match(/yes/).length > 0)
    factors_include_severity = ($('correct_factors').innerHTML.toLowerCase().match(/severity/).length > 0)
    factors_include_location = ($('correct_factors').innerHTML.toLowerCase().match(/location/).length > 0)
    factors_include_patterns = ($('correct_factors').innerHTML.toLowerCase().match(/patterns/).length > 0)
    factors_include_explanation = ($('correct_factors').innerHTML.toLowerCase().match(/explanation/).length > 0)
    
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
    
    //patterns, severity, body location, explanation credibility
    logDebug ("ok factors are correct too");
    return true;

}

function show_answer() {
    hideElement ('submit_div');
    if (!validate()) {
        alert ("Please choose yes or no.");
        return;
    }
    if (answer_is_correct()) {
        $("your_answer_was").innerHTML = "Your answer is correct.";
    }
    else {
        $("your_answer_was").innerHTML = "Your answer is incorrect.";
    
    }
    showElement ('feedback_div');
    
      maybeEnableNext();
}


MochiKit.Signal.connect(window, "onload", loadState)
//MochiKit.Signal.connect(window, "onload", setfocus)

function saveState()
{
/*
   if (!$('dosage_correct'))
   {
      debug("saveState")
      url = 'http://' + location.hostname + ':' + location.port + "/activity/prescription/save/"
    
      rx = {} 
      rx['dosage'] = $('dosage').value
      rx['disp'] = $('disp').value
      rx['sig'] = $('sig').value
      rx['refills'] = $('refills').value
      
      if ($('dosage_2'))
      {
         rx['dosage_2'] = $('dosage_2').value
         rx['disp_2'] = $('disp_2').value
         rx['sig_2'] = $('sig_2').value
         rx['refills_2'] = $('refills_2').value
      }
      
      doc = {}
      doc[$('medication_name').value] = rx
      
      // save state via a synchronous request. 
      var sync_req = new XMLHttpRequest();  
      sync_req.onreadystatechange= function() { if (sync_req.readyState!=4) return false; }         
      sync_req.open("POST", url, false);
      sync_req.send(queryString({'json':JSON.stringify(doc, null)}));
   }
   */
}

MochiKit.Signal.connect(window, "onbeforeunload", saveState)

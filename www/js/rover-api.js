/*----- HELPER FUNCTIONS -----*/
function roverResource(resource) {
	return roverDomain+roverApiPath+resource;
}

/*----- ROVER API FUNCTIONS -----*/
function sendMotorCommand(command, pin, speed) {
	$.post(roverResource('sendcommand'),
		{
			command: command,
			pin: pin,
			speed: Number(speed)
		}, function (response) {
			//writeToConsole(response);
		});
}

function saveDesign() {
	xml = Blockly.Xml.workspaceToDom(workspace);
	xmlString = Blockly.Xml.domToText(xml);
	$.post(roverResource('blockdiagrams'), {bdString: xmlString, designName: designName}, function(response){
	}).error(function(){
			writeToConsole("There was an error saving your design to the rover");
	});
}

function refreshSavedBds() {
	$.get(roverResource('blockdiagrams'), function(json){
		if (!json.result.length){
			$('#savedDesignsArea').text("There are no designs saved on this rover");
		} else {
			$('#savedDesignsArea').empty();
			json.result.forEach(function(entry) {
				$('#savedDesignsArea').append("<a href='#' class='button' style='margin:10px;' onclick='return loadDesign(\""+entry+"\")'>"+entry+"</a>");
			});
		}
	}
	);
}

function loadDesign(name) {
	$('#loadModal').foundation('reveal', 'close');
	$.get(roverResource('blockdiagrams')+'/'+name, function(response){
		workspace.clear();

		xmlDom = Blockly.Xml.textToDom(response.getElementsByTagName('bd')[0].childNodes[0].nodeValue);
		Blockly.Xml.domToWorkspace(workspace, xmlDom);
		if (name == 'event_handler_hidden')
			designName = "Unnamed_Design_" + (Math.floor(Math.random()*1000)).toString();
		else
			designName = name;
		$('a#downloadLink').attr("href", "saved-bds/"+designName+".xml");
		$('a#downloadLink').attr("download", designName+".xml");
		$('a#designNameArea').text(designName);

		hideBlockByComment("MAIN EVENT HANDLER LOOP");
		var hiddenBlock;
		var allBlocksHidden = true;
		for (hiddenBlock of blocksToHide) {
			if (!hideBlock(hiddenBlock))
				allBlocksHidden = false;
		}
		if (allBlocksHidden)
			showBlock('always');
	}).error(function(){
			alert("There was an error loading your design from the rover");
	});
	updateCode();
}

function acceptName() {
	designName = $('input[name=designName]').val();

	$.get(roverResource('blockdiagrams'), function(json){
		var duplicate = false;
		for (var i=0; i<json.length; i++){
			if (json[i] == designName)
				duplicate = true;
		}

		if (designName === ''){
			$('#nameErrorArea').text('Please enter a name for your design in the box');
		} else if (duplicate) {
			$('#nameErrorArea').text('This name has already been chosen. Please pick another one.');
		} else {
			saveDesign();
			$('#nameErrorArea').empty();
			$('a#designNameArea').text(designName);
			$('a#downloadLink').attr("href", "saved-bds/"+designName+".xml");
			$('a#downloadLink').attr("download", designName+".xml");
			$('#nameModal').foundation('reveal', 'close');
		}
	});
}

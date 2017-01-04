/**
 * @license
 * Visual Blocks Language
 *
 * Copyright 2012 Google Inc.
 * Copyright 2015 Brady L. Hurlburt.
 * https://developers.google.com/blockly/
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * @fileoverview Generating JavaScript for time blocks.
 * @author bradyhurlburt@gmail.com (Brady L. Hurlburt)
 */
'use strict';

goog.provide('Blockly.JavaScript.time');

goog.require('Blockly.JavaScript');

Blockly.JavaScript['continue'] = function(block) {
  var value_length = Blockly.JavaScript.valueToCode(block, 'LENGTH', Blockly.JavaScript.ORDER_ATOMIC);
  var dropdown_units = block.getFieldValue('UNITS');
	if (dropdown_units == "UNITS_seconds")
		value_length = value_length * 1000;
	/* From here on out, "continue" is known as "sleep" */
	var code = "sleep("+value_length+");";
  return code;
};

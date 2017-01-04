/**
 * @license
 * Visual Blocks Editor
 *
 * Copyright 2012 Google Inc.
 * Copyright 2016 Brady L. Hurlburt
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
 * @fileoverview Event blocks for Blockly.
 * @author bradyhurlburt@gmail.com (Brady L. Hurlburt)
 */
'use strict';

goog.provide('Blockly.Blocks.events');

goog.require('Blockly.Blocks');


/**
 * Common HSV hue for all blocks in this category.
 */
Blockly.Blocks.events.HUE = 230;

Blockly.Blocks['pop_event_queue'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("pop event queue");
    this.setOutput(true, "String");
    this.setColour(Blockly.Blocks.events.HUE);
    this.setTooltip('Get the end of the event queue');
    this.setHelpUrl('http://www.example.com/');
  }
};

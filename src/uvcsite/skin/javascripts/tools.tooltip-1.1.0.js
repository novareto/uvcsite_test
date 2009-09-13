/**
 * tools.tooltip 1.1.0 - Tooltips done right.
 * 
 * Copyright (c) 2009 Tero Piirainen
 * http://flowplayer.org/tools/tooltip.html
 *
 * Dual licensed under MIT and GPL 2+ licenses
 * http://www.opensource.org/licenses
 *
 * Launch  : November 2008
 * Date: ${date}
 * Revision: ${revision} 
 */
(function($) { 

	// static constructs
	$.tools = $.tools || {};
	
	$.tools.tooltip = {
		version: '1.1.0',
		
		conf: { 
			
			// default effect variables
			effect: 'slide',
			direction: 'up', // down, left, right 
			bounce: false,
			slideOffset: 10,
			slideInSpeed: 200,
			slideOutSpeed: 200, 
			slideFade: !$.browser.msie, 
			
			fadeOutSpeed: "fast",
			tip: null,
			
			predelay: 0,
			delay: 30,
			opacity: 1,			
			lazy: undefined,
			
			// 'top', 'bottom', 'right', 'left', 'center'
			position: ['top', 'center'], // or a string "top center" (since 1.1) 
			cancelDefault: true,
			offset: [0, 0], 
			api: false,
			
			// type to event mapping 
			events: {
				def: 			"mouseover,mouseout",
				input: 		"focus,blur",
				widget:		"focus mouseover,blur mouseout"
			}				
		},
		
		addEffect: function(name, loadFn, hideFn) {
			effects[name] = [loadFn, hideFn];	
		} 
	};
	
	
	var effects = { 
		toggle: [ 
			function(done) { 
				var conf = this.getConf();
				this.getTip().css({opacity: conf.opacity}).show();
				done.call();
			},
			
			function(done) { 
				this.getTip().hide();
				done.call();
			} 
		],
		
		fade: [
			function(done) { this.getTip().fadeIn(this.getConf().fadeInSpeed, done); },  
			function(done) { this.getTip().fadeOut(this.getConf().fadeOutSpeed, done); } 
		]		
	};   


	// directions for slide effect
	var dirs = {
		up: ['-', 'top'],
		down: ['+', 'top'],
		left: ['-', 'left'],
		right: ['+', 'left']
	};
	
	/* default effect: "slide"  */
	$.tools.tooltip.addEffect("slide", 
		
		// show effect
		function(done) { 
			
			// variables
			var conf = this.getConf(), 
				 tip = this.getTip(),
				 params = conf.slideFade ? {opacity: conf.opacity} : {}, 
				 dir = dirs[conf.direction] || dirs.up;

			// direction			
			params[dir[1]] = dir[0] +'='+ conf.slideOffset;
			
			// perform animation
			if (conf.slideFade) { tip.css({opacity:0}); }
			tip.show().animate(params, conf.slideInSpeed, done); 
		}, 
		
		// hide effect
		function(done) {
			
			// variables
			var conf = this.getConf(), 
				 offset = conf.slideOffset,
				 params = conf.slideFade ? {opacity: 0} : {}, 
				 dir = dirs[conf.direction] || dirs.up;
			
			// direction
			var sign = "" + dir[0];
			if (conf.bounce) { sign = sign == '+' ? '-' : '+'; }			
			params[dir[1]] = sign +'='+ offset;			
			
			// perform animation
			this.getTip().animate(params, conf.slideOutSpeed, function()  {
				$(this).hide();
				done.call();		
			});
		}
	); 

	function Tooltip(trigger, conf) {
		
		var self = this;
		
		trigger.data("tooltip", self);
		
		// find the tip
		var tip = trigger.next(); 
		
		if (conf.tip) {
			
			tip = $(conf.tip);
			
			// multiple tip elements
			if (tip.length > 1) {
				
				// find sibling
				tip = trigger.nextAll(conf.tip).eq(0);	
				
				// find sibling from the parent element
				if (!tip.length) {
					tip = trigger.parent().nextAll(conf.tip).eq(0);
				}
			} 
		} 		
		
		
		// generic binding function
		function bind(name, fn) {
			$(self).bind(name, function(e, args)  {
				if (fn && fn.call(this, args ? args.position : undefined) === false && args) {
					args.proceed = false;	
				}	
			});	
			
			return self;
		}
		
		
		/* calculate tip position relative to the trigger */  	
		function getPosition() { 
			 
			// vertical axis
			var top = trigger.position().top - tip.outerHeight();				
			var height = tip.outerHeight() + trigger.outerHeight();				
			var pos = conf.position[0];				
			if (pos == 'center') { top += height / 2; }
			if (pos == 'bottom') { top += height; }
			
			// horizontal axis
			var width = trigger.outerWidth() + tip.outerWidth();
			var left = trigger.position().left + trigger.outerWidth();									
			pos = conf.position[1]; 
			
			if (pos == 'center') { left -= width / 2; }
			if (pos == 'left')   { left -= width; }	
			
			// offset
			top += conf.offset[0];
			left += conf.offset[1];	
			
			return {top: top, left: left};
		}
		
		
		// bind all callbacks from configuration
		$.each(conf, function(name, fn) {                   
			if ($.isFunction(fn)) { bind(name, fn); }
		}); 		
		
		// event management
		var isInput = trigger.is(":input"), 
			 isWidget = isInput && trigger.is(":checkbox, :radio, select, :button"),			
			 type = trigger.attr("type"),
			 evt = conf.events[type] || conf.events[isInput ? (isWidget ? 'widget' : 'input') : 'def']; 
		
		evt = evt.split(/,\s*/); 
		
		trigger.bind(evt[0], function(e) {
			
			// see if the tip was launched by this trigger
			var t = tip.data("trigger");			
			if (t && t[0] != this) { tip.hide(); }
			
			e.target = this;
			self.show(e);
			tip.hover(self.show, function(e) { self.hide(); });
				
		});
		
		trigger.bind(evt[1], function() {
			self.hide(); 
		});
		
		// ensure that the tip really shows up. IE cannot catch up with this.
		if (!$.browser.msie && !isInput) {
			trigger.mousemove(function()  {					
				if (!self.isShown()) {
					trigger.triggerHandler("mouseover");	
				}
			});
		}

		// for PNG backgrounds opacity changes will generate a black border for IE
		if (conf.opacity < 1) {
			tip.css("opacity", conf.opacity);		
		}
	        console.log("HILLI");	
		var pretimer = 0, title = trigger.attr("title");
		
		if (title && conf.cancelDefault) { 
			trigger.removeAttr("title");
			trigger.data("title", title);
		}
		
		$.extend(self, {
				
			show: function(e) {
				
				if (e) { trigger = $(e.target); }				

				clearTimeout(tip.data("timer"));					
				
				if (tip.is(":animated") || tip.is(":visible")) { return self; }
				
				function show() {
					
					tip.data("trigger", trigger);
					
					// get position
					var pos = getPosition();					
					
					// title attribute					
					if (conf.tip && title) {
						tip.html(title);
					} 				
					
					// onBeforeShow
					var p = {proceed: true, position: pos};
					$(self).trigger("onBeforeShow", p);				
					if (p.proceed === false) { return self; }					
					
					// onBeforeShow may have altered the configuration
					pos = getPosition();
					
					// set position
					tip.css({position:'absolute', top: pos.top, left: pos.left});					
					
					// invoke effect
					effects[conf.effect][0].call(self, function()  {
						// onShow
						$(self).trigger("onShow");			
					});					
					
				}
				
				if (conf.predelay) {
					clearTimeout(pretimer);
					pretimer = setTimeout(show, conf.predelay);	
					
				} else {
					show();	
				}
				
				return self;
			},
			
			hide: function() {
				
				clearTimeout(tip.data("timer"));
				clearTimeout(pretimer);
				
				if (!tip.is(":visible")) { return; }
				
				function hide() {
					
					// onBeforeHide
					var p = {proceed: true};
					$(self).trigger("onBeforeHide", p);				
					if (p.proceed === false) { return; }
					
					effects[conf.effect][1].call(self, function() {
						$(self).trigger("onHide");		
					});
				}
				
				if (conf.delay) {
					tip.data("timer", setTimeout(hide, conf.delay));
					
				} else {
					hide();	
				}			
				
				return self;
			},
			
			isShown: function() {
				return tip.is(":visible, :animated");	
			},
				
			getConf: function() {
				return conf;	
			},
				
			getTip: function() {
				return tip;	
			},
			
			getTrigger: function() {
				return trigger;	
			},
			
			// callback functions
			onBeforeShow: function(fn) {
				return bind("onBeforeShow", fn); 		
			},
			
			onShow: function(fn) {
				return bind("onShow", fn); 		
			},
			
			onBeforeHide: function(fn) {
				return bind("onBeforeHide", fn); 		
			},
			 
			onHide: function(fn) {
				return bind("onHide", fn); 		
			} 		

		});
		
	}
		
	
	// jQuery plugin implementation
	$.prototype.tooltip = function(conf) {
		
		// return existing instance
		var api = this.eq(typeof conf == 'number' ? conf : 0).data("tooltip");
		if (api) { return api; }
		
		// setup options
		var opts = $.extend(true, {}, $.tools.tooltip.conf);		
		
		if ($.isFunction(conf)) {
			conf = {onBeforeShow: conf};
			
		} else if (typeof conf == 'string') {
			conf = {tip: conf};	
		}

		$.extend(true, opts, conf);
		
		// can also be given as string
		if (typeof opts.position == 'string') {
			opts.position = opts.position.split(/,?\s/);	
		}
		
		// assign tip's only when apiement is being mouseovered		
		if (opts.lazy !== false && (opts.lazy === true || this.length > 20)) {	
				
			this.one("mouseover", function() {	
				api = new Tooltip($(this), opts);
				api.show();
			}); 
			
		} else {
			
			// install tooltip for each entry in jQuery object
			this.each(function() {
				api = new Tooltip($(this), opts); 
			});
		} 

		return opts.api ? api: this;		
		
	};
		
}) (jQuery);

		


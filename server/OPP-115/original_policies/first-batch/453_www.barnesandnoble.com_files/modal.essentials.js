/*! BARNES-BUILDER 2015-06-29 */
BN.Modal=BN.Modal||{},BN.Modal.Base=BN.Modal.Base||Extend(function(){var a=function(){this.__originalArguments=Array.prototype.slice.call(arguments,0);consoleLog("Instantiating BN.Modal.Base"),this.on("display",function(){window.html5.shivDocument(document)}),$(document.body).addClass("pure-is-open"),this.closeEvents.all=this.closeEvents.all||[],this.closeEvents.all.push(function(){var a=!1;for(var b in Modal.openModals)if(Modal.openModals.hasOwnProperty(b)){a=!0;break}a||$(document.body).removeClass("pure-is-open")})};return a.prototype={defaultOptions:{tplDir:SITE_ROOT+"/modals/",tplExt:".jsp",overlayClose:"all",css:{position:"fixed"},modalIsScrollable:!0,useCache:!1},$spinner:null,invisibleOverlay:!1,__cycle:function(){var a=this.thisConstructor,b=a.prototype,c=Array.prototype.slice.call(this.__originalArguments,0),d=this;this.Close();for(var e in b)d[e]=b[e];a.apply(d,c)},initGenericView:function(){BN.Validate.Listen($(this.modal).find("form")),document.body.className.indexOf("lt-ie9")>-1&&!$(".tabgroup span[id]").length&&(consoleLog("IE8 Detected!"),consoleLog("Setting Timeout"),setTimeout(function(){consoleLog("Timeout Executing");var a=document.getElementById("selectivizrScript"),b=a.getAttribute("src");consoleLog("Executing selectivizr..."),consoleLog(jQuery.getScript(b))},500)),$("select").selectBox(),this.on("display",function(){consoleLog("Styling Select Boxes"),$("#state").length>0&&autofillStateFix()})},initFocus:function(){var a=($(this.modal),$(this.modal).find("form"));this.on("display",function(){var b=$(a).find("input[autofocus]");$(b).length&&$(b).focus()})},initOverlay:function(){var a=document.createElement("div");return 1==this.invisibleOverlay?(a.style.backgroundColor="#ffffff",a.style.opacity=0,a.style.filter="alpha(opacity=0);"):(a.style.backgroundColor="#000000",a.style.opacity=.5,a.style.filter="alpha(opacity=50);"),a.style.height="100%",a.style.width="100%",a.style.position="fixed",a.style.top="0px",a.style.left="0px",a},useInvisibleOverlay:function(){this.invisibleOverlay=!0},displaySpinner:function(){consoleLog("Displaying spinner...");var a=$(this.modal),b=a.find("header").first(),c={top:"0px"};return b.length>0&&(consoleLog("Adjusting top to compensate for header"),c.top=b.outerHeight()+"px"),consoleLog("Building spinner"),this.$spinner=$("<div/>").addClass("spinner").css(c),consoleLog("Appending spinner to modal DOM"),this.$spinner.appendTo(a),this.$spinner.focus(),this.$spinner},hideSpinner:function(){return $(this.modal).find(".spinner").remove()},initForm:function(a){var b=this,c=$(this.modal).find('form.uxhr,form[action*="xhr"]');consoleLog("Attaching uXHR to form",c),BN.uXHR.Form.apply(c),consoleLog("Listening for Errors"),c.on("amplifiFormError",function(a,c,d,e,f){var g=f.items;consoleError("Unsuccessful Form Submission: Server's response indicated errors occurred"),consoleLog(g),BN.Validate.DisplayErrors(this,g),b.$spinner.remove()}).on("amplifiFormBeforeSubmit",function(){consoleLog("Calling displaySpinner"),b.hideSpinner(),b.displaySpinner()}).on("amplifiFormSuccess",function(d,e){var f=b.data,g=window.location.toString().split("#")[0];if(a===!1||null!=f&&f.redirect===!1)return void consoleLog("Success!");null!=e&&void 0!=e&&e instanceof Object&&e.redirectSuccessUrl&&""!=e.redirectSuccessUrl?g=e.redirectSuccessUrl:null!=f&&void 0!=f&&f instanceof Object&&f.redirectSuccessUrl&&""!=f.redirectSuccessUrl&&(g=f.redirectSuccessUrl);var h=null,i=(h=c.find('input[name="modalRedirect"]')).length>0;if(i){consoleLog("Success! Redirecting modal to "+h.val());{var j=b.getContructorFromString(h.val());new j(null,null,null,b)}}else{consoleLog("Success! Redirecting page to "+g);var k=g;"undefined"!=typeof BN_EXTERNAL_DOMAIN_PREFIXED&&(k=BN_EXTERNAL_DOMAIN_PREFIXED+k),window.location=k}}).on("firstinvalid",function(){b.$spinner&&b.$spinner.remove()}),$(document).on("click","#guestCheckoutBtn",function(){$("#checkoutForm").submit()}),$(this.modal).find("select").selectBox()},clearForm:function(a){var b=$(a),c="input[type='text'],input[type='email'],input[type='tel'],input[type='password'],input[type='number'],input[type='file'],select,textarea";return b.find(c).val(""),b.find('input[type="radio"], input[type="checkbox"]').removeAttr("checked").removeAttr("selected"),b}},a}(),Modal,!0),BN.Modal=BN.Modal||{},BN.Modal.Confirm=BN.Modal.Confirm||Extend(function(){var a=function(a,b){this.data=b,consoleLog("Instantiating BN.Modal.Confirm"),consoleLog("Using "+(a||this.tplName)+" template")};return a.prototype={tplName:"confirm"},a}(),BN.Modal.Base,!0),BN.Modal.External=BN.Modal.External||{};var externalHref="";BN.Modal.External.Link=BN.Modal.External.Link||Extend(function(){var a=function(a,b){this.data=b,consoleLog("Instantiating BN.Modal.External.Link")};return a.prototype={tplName:"external-link",defaultOptions:{tplDir:SITE_ROOT+"/modals/",useCache:!1},initView:function(){var a=this.data,b=$(this.modal),c=$(a.target),d=c.attr("href")||"";this.on("display",function(){(""!=a["modal-title"]||"undefined"!=a["modal-title"])&&b.find("#dialog-title").text(a["modal-title"]),""!=a["modal-width"]&&"undefined"!=a["modal-width"]&&b.find("iframe").attr("width",a["modal-width"]),""!=a["modal-height"]&&"undefined"!=a["modal-height"]&&b.find("iframe").attr("height",a["modal-height"]),""!=a["modal-scrolling"]&&"undefined"!=a["modal-scrolling"]&&b.find("iframe").attr("scrolling",a["modal-scrolling"]),b.find("iframe").attr("src",d)})}},a}(),BN.Modal.Base,!0),BN.Modal=BN.Modal||{},BN.Modal.Success=BN.Modal.Success||Extend(function(){var a=function(a,b){this.data=b,consoleLog("Instantiating BN.Modal.Success")};return a.prototype={tplName:"success",initView:function(){var a=this.data,b=$(this.modal);if(a&&(a.title&&"string"==typeof a.title&&b.find("#dialog-title").text(a.title),a.messages)){var c=b.find("ul").first(),d=c.find("li").first().clone().html(""),e=$("<span/>").attr("data-icon","checkmark").html("Success!");c.find("li").remove(),c.addClass("modal-success-message");for(var f in a.messages)if(a.messages.hasOwnProperty(f)){var g=a.messages[f],h=d.clone();switch(g.type){case"success":h.append(e.clone())}0==f&&h.addClass("success-first"),h.append(g.message),c.append(h)}a.onclose&&this.closeEvents.all.push(a.onclose)}}},a}(),BN.Modal.Base,!0);
var P2_VIDIBLE=function(){function i(i){this._playerDiv=i}return i.prototype={_BASE_PIXEL_URL:"http://dco.springserve.com/s?",_playerDiv:null,_params:{},_playerReady:!1,_numImps:0,setDomain:function(i){this._params.url=i},addAdditionalParam:function(i,t){this._params[i]=encodeURI(t)},start:function(){var i=this;this._playerDiv.vdb_Player?this.onPlayerReady(this._playerDiv.vdb_Player):setTimeout(function(){i.start()},0)},onPlayerReady:function(i){this._playerReady=!0,this.fire(10,this._params);var t=this;"undefined"!=typeof vidible&&i.addEventListener(vidible.AD_START,function(){t._numImps+=1,t.fire(11,t._params)})},fire:function(i,t){var a=this.pixelURL(i,t);pix=document.createElement("img"),pix.style.height="1px",pix.style.width="1px",pix.src=a,document.body.appendChild(pix)},pixelURL:function(i,t){var a="yh_id="+i;for(param in t)a+="&"+param+"="+t[param];return a+="&num_imps="+this._numImps,this._BASE_PIXEL_URL+"cb="+this.randomNum(1e6)+"&"+a},randomNum:function(i){return Math.floor(Math.random()*i+1)}},_dat={tracker:function(t){var a=new i(t);return a}}}();
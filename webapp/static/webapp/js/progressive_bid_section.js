var progressiveBidSection = function (id){

	this.myId = id;

	this.sectionId = PROGRESSIVE_BID_SECTION_ID + this.myId;
	this.sliderParentId = PROGRESSIVE_BID_SLIDER_PARENT_ID + this.myId;
	this.sliderId = PROGRESSIVE_BID_SLIDER_ID + this.myId;
	this.priceInputId = PROGRESSIVE_BID_PRICE_INPUT_ID + this.myId;
	this.removeBtnId = PROGRESSIVE_BID_REMOVE_BTN_ID + this.myId;
	this.descriptionId = PROGRESSIVE_BID_DESCRIPTION_ID + this.myId;
	this.qtyDescriptionId = PROGRESSIVE_BID_QTY_DESCRIPTION_ID + this.myId;
	this.priceDescriptionId = PROGRESSIVE_BID_PRICE_DESCRIPTION_ID + this.myId;

	var openProgressiveBidWrapper = "";
	var bidInputElements = "";
	var bidDescriptor = "";
	var closeProgressiveBidWrapper = "";

	this.getId = function(){
		return this.myId;
	}

	this.buildHtmlElements = function(){
		openProgressiveBidWrapper = '<div class="progressive-bid-section" id="' + this.sectionId + '" >';

		bidInputElements = 	'<div class="col-xs-12">\
									<div class="col-xs-7 col-sm-7 col-md-7 col-lg-7 progressive-bid-qty-slider-parent" id="' + this.sliderParentId + '">\
										<div class="progressive-bid-qty-slider" id="' + this.sliderId + '"></div>\
									</div>\
									<div class="col-xs-4 col-sm-4 col-md-3 col-lg-4" style="margin-top: 2px;">\
										<input type="number" id="' + this.priceInputId + '" min="0.01" step="0.01" placeholder="Bid Value" value="0.00" class="form-control bid-price-input"/>\
									</div>\
									<div class="col-xs-1 pull-right">\
										<a class="btn btn-danger btn-lg remove-bid-btn" id="' + this.removeBtnId + '">\
											<span class="fa fa-times" ></span>\
										</a>\
									</div>\
								</div>';

		bidDescriptor = '<div class="col-xs-12 bid-description" id="' + this.descriptionId + '">\
								<span>For <span class="bid-description-value" id="' + this.qtyDescriptionId + '">0</span> kWh, I would pay up to a total of <span class="bid-description-value" id="' + this.priceDescriptionId + '">0</span>$.</span>\
							</div>';

		closeProgressiveBidWrapper = '</div>';
	};

	this.html = function html(){
		this.buildHtmlElements();
		return	openProgressiveBidWrapper + bidInputElements + bidDescriptor + closeProgressiveBidWrapper;	
	};
};
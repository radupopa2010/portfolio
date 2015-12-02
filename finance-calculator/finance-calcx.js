function TaycorCurrencyFormat(inp) {
	inp = parseFloat(inp).toFixed(2);
	inp += '';
	x = inp.split('.');
	x1 = x[0];
	x2 = x.length > 1 ? '.' + x[1] : '';
	var rgx = /(\d+)(\d{3})/;
	while (rgx.test(x1)) {
		x1 = x1.replace(rgx, '$1' + ',' + '$2');}
		var ret = x1 + x2;if((''+ret) == 'NaN') return '0.00';return ret;}

$(window).ready(function (){
				//' /*	[CL] Calculator Update Method 		*/ + '
				var TxnCLPaymentRefreshActive = false;
				var SREFoppo_cl_totalamtdue = false;
				function TxnCLPaymentRefresh(fromGMPts){
					if(TxnCLPaymentRefreshActive) return;
					TxnCLPaymentRefreshActive = true;
					
					var equipCost = parseFloat((""+$('#oppo_totalcost').val()).replace(/,/g, "")).toFixed(2);
					if(!equipCost) equipCost = 1.0; if(equipCost<1) equipCost = 1.0;
					if($('#oppo_totalcost:focus').length == 0){
						$('#oppo_totalcost').val(TaycorCurrencyFormat(equipCost));
					}
					
					var termMonths = parseInt($('#oppo_termlength').val());
					if(!termMonths) termMonths = 1; if(termMonths<1) termMonths = 1;
					
					var advRent = parseInt($('#oppo_advpmtcount').val());
					if(!advRent) advRent = 0;
					
					var buyRate = parseFloat($('#oppo_proposed_buyrate').val());
					if(!buyRate) buyRate = 0.01; if(Math.abs(buyRate)<0.01) buyRate = 0.01;
					if($('#oppo_proposed_buyrate:focus').length == 0){
						$('#oppo_proposed_buyrate').val(TaycorCurrencyFormat(buyRate));
					}
					
					var buyRateMonthly = buyRate/(100*12);
					if(fromGMPts){
						var gmPoints = parseFloat($('#oppo_proposed_gmpoints').val());
						var grossMargin = (equipCost * (gmPoints/100)).toFixed(2);
						
					}else{
						var grossMargin = parseFloat((""+$('#oppo_proposed_grossmargin').val()).replace(/,/g, "")).toFixed(2);
						var gmPoints = (100 * (parseFloat(grossMargin)/parseFloat(equipCost))).toFixed(2);
						//alert(gmPoints);
					}
					if($('#oppo_proposed_grossmargin:focus').length == 0){
						$('#oppo_proposed_grossmargin').val(TaycorCurrencyFormat(grossMargin));
					}
					
					if($('#oppo_proposed_gmpoints:focus').length == 0){
						$('#oppo_proposed_gmpoints').val(TaycorCurrencyFormat(gmPoints));
					}
					
					//	$('#oppo_proposed_gmpoints').val(gmPoints);
					//  $('#oppo_proposed_grossmargin').val(TaycorCurrencyFormat(grossMargin)).change();
					
					var principal = parseFloat(equipCost) + parseFloat(grossMargin);
					//alert(typeof advRent);
					var estMonthlyPmtFactor = 1/(advRent + (Math.pow(1+buyRateMonthly,termMonths-advRent)-1)/(buyRateMonthly*Math.pow(1+buyRateMonthly,termMonths-advRent)));
					if($('#oppo_monthlypayment:focus').length == 0){
						$('#oppo_monthlypayment').val(TaycorCurrencyFormat(estMonthlyPmtFactor*principal));
					}
					
					TxnCLPaymentRefreshActive = false;
				}
		
				setTimeout(function (){
					TxnCLPaymentRefresh();
				}, 1000);
		
				//' /*	[CL] Calculator Update Triggers 	*/ + '/
				$('\
					#oppo_totalcost\
					, #oppo_termlength\
					, #oppo_advpmtcount\
					, #oppo_proposed_buyrate\
					, #oppo_proposed_grossmargin\
					, #oppo_docfee\
					, #oppo_secdeposit'
				).bind("propertychange change blur input", function (e){
					TxnCLPaymentRefresh(false);
				});
				$('#oppo_proposed_gmpoints'
				).bind("propertychange change blur input", function (e){
					TxnCLPaymentRefresh(true);
				});
					
		
			//	' /*	[CL] Calculator Price Assigned Trigger	 	*/ + '
				$('#oppo_monthlypayment'
				).bind("propertychange change blur input", function (e){

					var inpMonthlyPmtIdeal = $(this).val();
					if(!inpMonthlyPmtIdeal) return;
					var inpAmt = parseFloat((""+inpMonthlyPmtIdeal).replace(/,/g, ""));
					var equipCost = parseFloat((""+$('#oppo_totalcost').val()).replace(/,/g, ""));
					var termMonths = parseInt($('#oppo_termlength').val());
					var advRent = parseInt($('#oppo_advpmtcount').val());
					if(!advRent) advRent = 0;
					var advRentTotal = advRent;
					//if(!$(inp_chk_lockgm).is(':checked')){
					if(true){
						var buyRate = parseFloat($('#oppo_proposed_buyrate').val());
						var buyRateMonthly = buyRate/(100*12);
						var estCommission = inpAmt*(advRentTotal+(1/buyRateMonthly)*(1-Math.pow(1+buyRateMonthly, advRentTotal-termMonths))) - (equipCost);
						$('#oppo_proposed_grossmargin').val(TaycorCurrencyFormat(estCommission));
					}else{
						//$('#oppo_proposed_grossmargin').val(0);
						//$('#oppo_proposed_grossmargin').val(0);
						$('#oppo_proposed_buyrate').val("0.0");
						var buyRateMonthly = 0.0001;
						var estCommission = inpAmt*(advRentTotal+(1/buyRateMonthly)*(1-Math.pow(1+buyRateMonthly, advRentTotal-termMonths))) - (equipCost);
						var est_points = (100 * (parseFloat(estCommission)/parseFloat(equipCost))).toFixed(2);
						alert(est_points);
						//$('#oppo_proposed_buyrate').val(TaycorCurrencyFormat((est_points).toFixed(2)));
					}
					TxnCLPaymentRefresh(false);
				});
	});	

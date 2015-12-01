// Helping funcions
function PaddZero(inpNumber){
	if(inpNumber < 10) return "0"+inpNumber;
	return ""+inpNumber;
}
function CloneObj(inpObject){
	var newObj = {};
	for(var eaAttr in inpObject){
		newObj[eaAttr] = inpObject[eaAttr];
	}
	return newObj;
}

 function commaSeparateNumber(val){
    while (/(\d+)(\d{3})/.test(val.toString())){
      val = val.toString().replace(/(\d+)(\d{3})/, '$1'+','+'$2');
    }
    return val;
  }
// Startup script
$(document).ready(function (){
	$(inpDateStart).datepicker({
		defaultDate: "-1w"
		, changeMonth: true
		, numberOfMonths: 1
		, onClose: function( selectedDate ) {
			$(inpDateEnd).datepicker( "option", "minDate", selectedDate );
			$(inpDateEnd).focus();
			RefreshMarkStats();
		}
		, onChangeMonthYear: function (y, n, i){
			$('.ui-datepicker-calendar td').each(function (){
				var thisDate = $(this).val();
				if(!thisDate) return;
				if(thisDate == " ") return;
				thisDate = PaddZero(parseInt(thisDate));
				thisDate = ""+$(this).data('year')+"-"+PaddZero($(this).data('month'))+"-"+thisDate;
				var docFound = MarkData.findOne(thisDate);
				if(docFound) return;
				$(this).css('text-decoration', 'line-through');
			});
		}
	});
	$(inpDateEnd).datepicker({
		defaultDate: "+1d"
		, changeMonth: true
		, numberOfMonths: 1
		, onClose: function( selectedDate ) {
			$(inpDateStart).datepicker( "option", "maxDate", selectedDate );
			RefreshMarkStats();
		}
	});
});

function RefreshMarkStats(){
	// Clear the display area
	$(tblApps).find('tbody').html('');
	$(tblTxns).find('tbody').html('');
	$(tblMark).find('td').text('');

	// Store default statistics values to summarize over the select date range
	var stats = {
		  '_id':0
		, 'mark_attempted': 0
		, 'money_spent': 0
		, 'mark_success': 0
		, 'mark_leads':0
		, 'mark_removes':0
		, 'users': {
			'proto': {
				  'leads_given': 0
				, 'leads_apps_produced': 0
				, 'leads_stalled': 0
				, 'leads_pending': 0
				, 'transactions_created': 0
				, 'transactions_funded': 0
				, 'transactions_margin': 0
				, 'transactions_pending': 0
				, 'transactions_stalled': 0
				,'transactions_ucompanies':0
			}
		}
	};
	var moneyBack = 0;
	// Capture the selected range (sart/end date values)
	var dtStart = $(inpDateStart).datepicker("getDate");
	var dtEnd = $(inpDateEnd).datepicker("getDate") || dtStart;
		dtEnd.setDate(dtEnd.getDate()+1);
	// Initialize the iterating date to the starting date
	var dtIter = dtStart || dtEnd;
	// Iterate through days until the iterater passes the end of the range
	while(dtIter < dtEnd){
		// Prepare a key to lookup data with
		var eaDayKey = (1900+dtIter.getYear()) + "-" + 
				PaddZero(1+dtIter.getMonth()) + "-" + PaddZero(dtIter.getDate());
		// Find documents matching this date (key)
		var docFound = MarkData.findOne(eaDayKey);
		// Only if the document is found...
		if(docFound){
			// Add all of the document statistics into the summary of statistics
			if('money_spent' in docFound) stats['money_spent'] += docFound['money_spent'];
			if('mark_attempted' in docFound) stats['mark_attempted'] += docFound['mark_attempted'];
			if('mark_success' in docFound) stats['mark_success'] += docFound['mark_success'];
			if('mark_leads' in docFound) stats['mark_leads'] += docFound['mark_leads'];
			if('mark_removes' in docFound) stats['mark_removes'] += docFound['mark_removes'];
			// ...

			// See if there are user statistics available too
			if('users' in docFound){
				// Iterate over each available user
				for(var eaUser in docFound['users']){
					var eaUserDoc = docFound['users'][eaUser];
					
					// Prevent the prototype user record from being overwritten
					if(eaUser == 'proto') continue;
					// If the user isn't already in the summary
					//	- create a new entry for them using the prototype
					if(!stats['users'][eaUser]) stats['users'][eaUser] = CloneObj(stats['users']['proto']);
					// Add all of the user's statistics into the summary of statistics
					if('leads_given' in eaUserDoc) stats['users'][eaUser]['leads_given'] += eaUserDoc['leads_given'];
					if('leads_apps_produced' in eaUserDoc) stats['users'][eaUser]['leads_apps_produced'] += eaUserDoc['leads_apps_produced'];
					if('leads_stalled' in eaUserDoc) stats['users'][eaUser]['leads_stalled'] += eaUserDoc['leads_stalled'];
					if('transactions_created' in eaUserDoc) stats['users'][eaUser]['transactions_created'] += eaUserDoc['transactions_created'];
					if('transactions_funded' in eaUserDoc) stats['users'][eaUser]['transactions_funded'] += eaUserDoc['transactions_funded'];
				if('transactions_margin' in eaUserDoc) {
						stats['users'][eaUser]['transactions_margin'] += eaUserDoc['transactions_margin'];
						moneyBack += eaUserDoc['transactions_margin']
					}
					if('transactions_pending' in eaUserDoc) stats['users'][eaUser]['transactions_pending'] += eaUserDoc['transactions_pending'];
					if('transactions_stalled' in eaUserDoc) stats['users'][eaUser]['transactions_stalled'] += eaUserDoc['transactions_stalled'];
					if('transactions_ucompanies' in eaUserDoc) {
						stats['users'][eaUser]['leads_pending'] += parseInt((eaUserDoc['leads_given'] - eaUserDoc['transactions_ucompanies']
																							 - eaUserDoc['transactions_created']));
					}
				
				// ...

				}
			 
			}
		}else{
			//console.log(["No Document Found for Date=", eaDayKey])
		}
		// Incriment the date by one day and loop
		dtIter.setDate(dtIter.getDate() + 1);
	}
	for (var eaUser in stats['users']){
		
	}
	console.log(stats)
	console.log(moneyBack)
	// render the stats
	
	var htmlForApps = '';
	var htmlForTxns = '';
	var htmlForMark = '';
	
		htmlForMark += '\
			<tr>\
				<td>'+stats['money_spent']+'</td>\
				<td>'+moneyBack+'</td>\
				<td>'+stats['mark_attempted']+'</td>\
				<td>'+stats['mark_success']+'</td>\
				<td>'+stats['mark_leads']+'</td>\
				<td>'+stats['mark_removes']+'</td>\
			</tr>\
		'

	for(var eaUser in stats['users']){
		if(eaUser == 'proto') continue;

		var eaUserStats = stats['users'][eaUser];
		htmlForApps += '\
			<tr>\
				<td>'+eaUser+'</td>\
				<td>'+eaUserStats['leads_given']+'</td>\
				<td>'+eaUserStats['leads_apps_produced']+'</td>\
				<td>'+eaUserStats['transactions_created']+'</td>\
				<td>'+eaUserStats['leads_stalled']+'</td>\
			</tr>\
		';
		htmlForTxns += '\
			<tr>\
				<td>'+eaUser+'</td>\
				<td>'+eaUserStats['transactions_created']+'</td>\
				<td>'+eaUserStats['transactions_funded']+'</td>\
				<td>'+eaUserStats['transactions_margin']+'</td>\
				<td>'+eaUserStats['transactions_pending']+'</td>\
				<td>'+eaUserStats['transactions_stalled']+'</td>\
			</tr>\
		';
	}


	$(tblApps).find('tbody').html(commaSeparateNumber(htmlForApps));
	$(tblTxns).find('tbody').html(commaSeparateNumber(htmlForTxns));
	$(tblMark).find('tbody').html(commaSeparateNumber(htmlForMark));
	

}

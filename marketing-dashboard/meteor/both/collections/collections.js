MarkData = new Mongo.Collection("markdata");

// ++++++++++ CREATE NEW COLLECTION ++++++
// db.[collectionName]

// example: 
// 	db.links
// 		it will create a new collection with this name if it dows not already exists

/*

Total sent
	- success
	- failed
Responding Companies
	
*/

// create 
// db.markdata.insert({ _id:"2015-01-02"
// 								   , 'mark-attempted': 10000
// 								   		-- number of marketing attempts
// 								   , 'mark-success': 7000
// 								   		-- number of marketing attempts with outcome == 'OK'
// 								   , 'mark-leads': 100
// 								   		-- number of companies with 'lead' responses to this marketing
// 								   , 'mark-leads-total': 105
// 								   		-- number of 'lead' responses from this marketing
// 							       , 'mark-removes': 14
// 								   		-- number of 'remove/reremove' responses
// 							       , 'booked-gm-total': 14000
// 								   		-- total gross margin from all transactions assoc. to this marketing
// 								   ,'users': {
// 									'andrew-test': { 
// 											'leads': 12
//		 								   		-- [user-context] number of companies with 'lead' responses to this marketing
// 											, 'leads-pending': 5
//		 								   		-- number of these leads which: 
//			 								   		... have an open communicaion for the next 10 days
//			 								   		... no other 'lead' responses from future marketing
// 											, 'leads-stalled': 2
//		 								   		-- number of these leads which: 
//			 								   		... ( company status = 'stalledlead'
//			 								   		... or have no open communicaion for the next 10 days
//			 								   		... or have another 'lead' responses from future marketing
//			 								   		... ) and are not linked to a transaction
// 											, 'transactions-created': 3
//		 								   		-- number of transactions associated to this marketing
// 											, 'transactions-pending': 1
//		 								   		-- ppo_status != 'stalled' and oppo_fund_expCommission is null
// 											, 'transactions-stalled': 1
//		 								   		-- oppo_status == 'stalled'
// 											, 'transactions-funded': 4
//		 								   		-- number of booked transactions (oppo_fund_expCommission is not null)
// 											, 'transactions-margin': 1000
//		 								   		-- total from this user's booked transactions
// 										} ,'shelly-test': { 
// 											'leads': 15
// 											, 'apps': 10
// 											, 'apps-active': 9
// 											, 'apps-stalled': 1
// 											, 'transactions-funded': 8
// 											, 'transactions-margin': 900
// 											, 'transactions-active': 8
// 											, 'transactions-stalled': 2 }
// 										,'dave-test': { 
// 											'leads': 23
// 											, 'apps': 15
// 											, 'apps-active': 14
// 											, 'apps-stalled': 1
// 											, 'transactions-funded': 10
// 											, 'transactions-margin': 9000
// 											, 'transactions-active': 13
// 											, 'transactions-stalled': 2 }
// 							  }  })

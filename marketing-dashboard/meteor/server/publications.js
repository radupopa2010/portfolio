
Meteor.publish("markdata", function(){
	return MarkData.find({});
});
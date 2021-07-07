<script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.7.5/angular.min.js"></script>

angular.module('speech', []);

angular.module('speech').controller('speechController', function($scope) {
  this.rec = new webkitSpeechRecognition();
  this.interim = '';
  this.final = '';
  var self = this;
  
  this.rec.continuous = false;
  this.rec.lang = 'en-US';
  this.rec.interimResults = true;
  this.rec.onerror = function(event) {
    console.log('error!');
  };

  this.start = function() {
    self.rec.start();
  };
  
  this.rec.onresult = function(event) {
    for(var i = event.resultIndex; i < event.results.length; i++) {
      if(event.results[i].isFinal) {
        self.final = self.final.concat(event.results[i][0].transcript);
        // clearing interim
        self.interim = '';
        $scope.$apply();
        console.log(event.results[i][0].transcript);
      } else {
        self.interim = '';
        $scope.$apply();
        self.interim = self.interim.concat(event.results[i][0].transcript);
        $scope.$apply();
      }
    }
  };
  
});
	var input = document.getElementById('text_filter');
	var filter = document.getElementById('filter');

	input.addEventListener( 'keyup', function(event)
	{
		if ( input.value == "" )
		{
			filter.setAttribute( 'uk-filter-control', '' );
		}

		else
		{
			filter.setAttribute( 'uk-filter-control', 'filter:[data-tags*=\'' + input.value + '\'i]' );
		}

		filter.click();
	});


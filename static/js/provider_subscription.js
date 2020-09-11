$(document).ready(function() {
   var subscription_count = undefined;
   var commission = data();
    $('#stripe').prop('hidden', true);

    $('#checkout').click(function (){
        subscription_count = Number($('#subscription').val());
        if (check_number(subscription_count) == false){
            alert('Please Enter Subscription...!');
            subscription_count = undefined;
        }
        else{
            if (confirm('You Enter For  Subscription :- "'+ subscription_count +'" \nPer Subscription Commission :- "' + commission + '" \nTotal :- "' + subscription_count*commission + '"')) {
            $('#form').prop('hidden', true);
            $('#stripe').prop('hidden', false);
            $('.stripe-button').attr('data-amount', subscription_count*commission);
            $('#data-subscription').attr('value', subscription_count);
            $('#info1').text('You Enter For Subscription :- '+ subscription_count);
            $('#info2').text('Per Subscription Commission :- ' + commission + '%');
            $('#info3').text('Total :- ' + subscription_count*commission);

            }
            else{
            $('#subscription').val('')
            subscription_count = undefined;
            }
        }

    });

    function check_number(number) {
        if (typeof number == 'number') {
            if(number == 0){
                return false;
            }
            else if(number <= 0){
                return false;
            }
        }
        else{
            return false;
        }
    }
  });
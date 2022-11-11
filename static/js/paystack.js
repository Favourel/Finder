var user = '{{ request.user }}'

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

const paymentForm = document.getElementById('make-payment');
paymentForm.addEventListener("click", payWithPaystack, false);
function payWithPaystack(e) {
  e.preventDefault();

  let handler = PaystackPop.setup({
    key: '{{paystack_public_key}}', // Replace with your public key
    email: '{{ request.user.email }}',
    currency: 'NGN',
    amount: '{{ get_cart_total }}' * 100,
    ref: '{{ payment.ref }}', // generates a pseudo-unique reference. Please replace with a reference you generated. Or remove the line entirely so our API will generate one for you
    //ref: ''+Math.floor((Math.random() * 1000000000) + 1), // generates a pseudo-unique reference. Please replace with a reference you generated. Or remove the line entirely so our API will generate one for you
    // label: "Optional string that replaces customer email"
    onClose: function(){
      alert('There was an error with processing payment. Kindly refresh page and run again');
    },
    callback: function(response){
      let message = 'Payment complete! Reference: ' + response.reference;
      //window.location.href = "{% url 'process_order' %}"

      var userData = {
                'reference':response.reference
            }
        var url = '{% url 'process_order' %}'
        //console.log(userData);

        fetch(url,
            {
                method: 'POST',
                headers: {'Content-Type': '/application/json', 'X-CSRFToken':csrftoken,},
                body:JSON.stringify({'ref': userData})
            }
        )

        .then((response) =>{
                return response.json()
            })

        .then((data) =>{
                console.log('Success:', data);
                window.location.href = '/market/'
            })

      //console.log(message);
    }
  });

  handler.openIframe();
}
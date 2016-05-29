var map;
function initMap(thing) {

    var address = thing;
    console.log("this is initMap address");
    console.log(address);

    var map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: 37.7749, lng: -122.4194},
      zoom: 9
    });

    var geocoder = new google.maps.Geocoder();

    geocodeAddress(geocoder, map, address);
  }

// test 9374889676090040179500
// This function gets information about the address to display

function geocodeAddress(geocoder, resultsMap, address) {

    var address = String(address.city) + String(address.state)

    geocoder.geocode({'address': address}, function(results, status) {
      if (status === google.maps.GeocoderStatus.OK) {
        resultsMap.setCenter(results[0].geometry.location);
        var marker = new google.maps.Marker({
          map: resultsMap,
          position: results[0].geometry.location
        });
      } else {
        alert('Geocode was not successful for the following reason: ' + status);
      }
    });
  }

function trackingInfo(results) {

    var address = results;
    console.log("this is address");
    console.log(address);

    initMap(address);

}

function updateAddress(evt) {
    evt.preventDefault();

    // When you have an event handler, the value of this is assigned by
    // JQuery to be whatever triggered the event
    console.log($(this));
    console.log($(this).data('trackingnum'));

    // this is the button
    // data is the data embedded in the button assigned in the HTML
    var trackingNum = $(this).data('trackingnum')

    $.post('/tracking/' + trackingNum, trackingInfo);
    console.log("Finished sending AJAX");
    }

$('.submit-tracking').click(updateAddress);
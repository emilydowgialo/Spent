var map;
function initMap(thing) {

    var address = thing;
    console.log("this is initMap address");
    console.log(address);

    var map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: 37.7749, lng: -122.4194},
      zoom: 12
    });

    var geocoder = new google.maps.Geocoder();

    geocodeAddress(geocoder, map, address);
  }

// test 9374889676090040179500
// This function gets information about the address to display

function geocodeAddress(geocoder, resultsMap, addressToUse) {

    var addressYay = String(addressToUse.city) + String(addressToUse.state);

    geocoder.geocode({'address': addressYay}, function(results, status) {
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

function appendTrackingInfo(address) {

  var trackingInfo = address;
  console.log("this is append tracking info trackingInfo");
  console.log(trackingInfo);

  var trackingStatus = String(trackingInfo.tracking_status);
  var trackingCity = trackingInfo.city;
  var trackingState = trackingInfo.state;
  var trackingZipcode = trackingInfo.zipcode;
  var trackingCountry = trackingInfo.country;

  console.log("this is tracking status");
  console.log(trackingStatus);

  console.log(trackingStatus);
  $('#tracking-status').html(trackingStatus);
  $('#tracking-city').html(trackingCity);
  $('#tracking-state').html(trackingState);
  $('#tracking-zipcode').html(trackingZipcode);
  $('#tracking-country').html(trackingCountry);
  console.log("finished with appendTrackingInfo");

}

function trackingInfo(results) {

    var address = results;
    console.log("this is address");
    console.log(address);

    initMap(address);
    appendTrackingInfo(address);

}

function updateAddress(evt) {
    evt.preventDefault();

    // When you have an event handler, the value of this is assigned by
    // JQuery to be whatever triggered the event
    console.log($(this));
    console.log($(this).data('trackingnum'));

    // this is the button
    // data is the data embedded in the button assigned in the HTML
    var trackingNum = $(this).data('trackingnum');

    $.post('/tracking/' + trackingNum, trackingInfo);
    console.log("Finished sending AJAX");
    }

$('.submit-tracking').click(updateAddress);
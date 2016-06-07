var map;
function initMap(thing) {

    var address = thing;
    console.log("this is initMap address");
    console.log(address);

    // Custom map styling
    var customMapType = new google.maps.StyledMapType([
      {
        stylers: [
          {hue: '#F68D5C'},
          {visibility: 'simplified'},
          {gamma: 0.5},
          {weight: 0.5}
        ]
      },
      {
        elementType: 'labels',
        stylers: [{visibility: 'on'}]
      },
      {
        featureType: 'water',
        stylers: [{color: '#AFC1CC'}]
      }
      ], {
        name: 'Custom Style'
    });

  var customMapTypeId = 'custom_style';

    var map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: 37.7749, lng: -122.4194},
      zoom: 12,
      mapTypeControlOptions: {
        mapTypeIds: [google.maps.MapTypeId.ROADMAP, customMapTypeId]
      }
    });

    map.mapTypes.set(customMapTypeId, customMapType);
    map.setMapTypeId(customMapTypeId);

    var geocoder = new google.maps.Geocoder();

    geocodeAddress(geocoder, map, address);
  }

// test 9374889676090040179500
// This function gets information about the address to display

function geocodeAddress(geocoder, resultsMap, addressToUse) {

    // if addressToUse exists statement would fix the error
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

function appendTrackingInfo(info) {

  // This is the tracking info object
  var trackingInfo = info;
  console.log("this is append tracking info trackingInfo");
  console.log(trackingInfo);

  // Define variables for info we need
  var trackingStatus = String(trackingInfo.tracking_status);
  var trackingCity = trackingInfo.city;
  var trackingState = trackingInfo.state;
  var trackingZipcode = trackingInfo.zipcode;
  var trackingCountry = trackingInfo.country;

  console.log("this is tracking status");
  console.log(trackingStatus);

  // Display the information on the front end
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

    // Call the map function and the tracking info function
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
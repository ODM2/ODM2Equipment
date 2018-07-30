/**
 * Created by Juan on 7/18/2018.
 */
window.initMap = () => {
    let defaultZoomLevel = 18;
    let latitude = parseFloat(document.querySelector('div.map-container input[id="site-latitude"]').value);
    let longitude = parseFloat(document.querySelector('div.map-container input[id="site-longitude"]').value);
    let sitePosition = {lat: latitude, lng: longitude};

    let map = new google.maps.Map(document.getElementById('map'), {
        center: sitePosition,
        gestureHandling: 'greedy',
        zoom: defaultZoomLevel,
        mapTypeId: google.maps.MapTypeId.HYBRID
    });

    map.setOptions({minZoom: 3, maxZoom: 18});

    let marker = new google.maps.Marker({
        position: sitePosition,
        map: map
    });
};